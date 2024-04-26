import numpy as np
import numpy.linalg as la

from scipy import sparse

from matplotlib import tri
import matplotlib.pyplot as plt

class TriMesh:
    def __init__(self, filename, filetype, refine=0):
        V, E = self.read_mesh(filename, filetype)
        t = tri.Triangulation(V[:, 0], V[:, 1], E)

        if refine > 0:
            refiner = tri.UniformTriRefiner(t)
            t = refiner.refine_triangulation(subdiv=refine)
            V = np.vstack((t.x, t.y)).T
            E = t.triangles

        ncell = E.shape[0]
        cells = np.mean(V[E], axis = 1)
        areas = np.zeros(ncell)
        faces = t.edges
        nface = faces.shape[0]
        normals = np.zeros((nface, 2))
        fid2cid = np.zeros((nface, 2), dtype=np.int32)
        face_type = np.zeros(nface, dtype=np.int8)
        l = np.zeros(nface)

        vid_to_fid = {}

        # map vertex pair to face id
        for fid in range(nface):
            vid0, vid1 = faces[fid]
            v_key = (vid0, vid1) if vid0 < vid1 else (vid1, vid0)
            vid_to_fid[v_key] = fid

        for cid, vids in enumerate(t.triangles):
            # link cell id with face id
            # boundary face has two identical cell id
            for i, j in zip([0, 1, 2], [1, 2, 0]):
                v_key = (vids[i], vids[j]) if vids[i] < vids[j] else (vids[j], vids[i])
                fid = vid_to_fid[v_key]
                if face_type[fid] == 0:
                    fid2cid[fid] = np.array([cid, cid])
                    face_type[fid] = 1
                else:
                    old_cid = fid2cid[fid]
                    if cid < old_cid[0]:
                        fid2cid[fid, 0] = cid
                    else:
                        fid2cid[fid, 1] = cid

                    face_type[fid] = 2

            # compute cell volume (area)
            areas[cid] = 0.5 * np.abs(la.det(np.vstack((np.ones(3), V[vids].T))))


        for i, face in enumerate(faces):
            v0, v1 = V[face[0]], V[face[1]]
            tan = v0 - v1
            l[i] = la.norm(tan)
            n = np.array([-tan[1], tan[0]])

            # TODO: double check normal direction
            # normal point from c0 to c1
            c0 = cells[fid2cid[i, 0]]
            if n.dot((v0+v1)/2 - c0) < 0:
                normals[i] = -n / la.norm(n)
            else:
                normals[i] = n / la.norm(n)


        self.t = t
        self.cells = cells
        self.normals = normals
        self.fid2cid = fid2cid
        self.face_len = l
        self.areas = areas
        self.bndf_mask = (face_type == 1)
        self.ncell = ncell
        self.nface = nface

    def read_mesh(self, name, type='.'):
        if type == '.ply2':
            with open(name+type) as f:
                vnum = int(next(f))
                enum = int(next(f))
                v = [[float(x) for x in next(f).split()] for i in range(vnum)]
                e = [[int(x) for x in next(f).split()] for i in range(enum)]

            vertices = np.array(v)[:, :2]
            triangles = np.array(e, dtype=int)[:, 1:]
            # save file

        elif type == '.':
            vertices = np.loadtxt('mesh.v')
            triangles = np.loadtxt('mesh.e', dtype=int)

        else:
            raise "Unknown mesh file type."

        return vertices, triangles

    def plot(self, show_one_edge=False):
        fig, ax = plt.subplots()
        ax.set_aspect(1)
        ax.triplot(self.t.x, self.t.y, self.t.triangles, color='gray')
        print("Total cell number in triangle mesh: ", self.ncell)
        if show_one_edge:
            fid = 0
            vtx = np.vstack((self.t.x, self.t.y)).T
            v0 = vtx[self.t.edges[fid, 0]]
            v1 = vtx[self.t.edges[fid, 1]]
            c0 = self.cells[self.fid2cid[fid, 0]]
            c1 = self.cells[self.fid2cid[fid, 1]]
            ax.scatter(c0[0], c0[1], color='green', label='c0')
            ax.scatter(c1[0], c1[1], color='blue', label='c1')
            ax.scatter(v0[0], v0[1], color='red', marker='.')
            ax.scatter(v1[0], v1[1], color='red', marker='.')
            ax.quiver(*((v0 + v1) / 2), self.normals[fid, 0], self.normals[fid, 1], headaxislength=2, headlength=3, width=0.003, label='normal')
        
        plt.show()



class MeshSolver:
    def __init__(self, mesh: TriMesh, dt=5e-3, g = 1):
        self.mesh = mesh
        self.u = np.zeros((3, mesh.ncell))
        self.time = 0
        self.dt = dt
        self.g = g


    def init_height(self, func):
        cells = self.mesh.cells
        self.u[0] = func(cells[:, 0], cells[:, 1])


    def wall_bc(self):
        u_by_face = self.u[:,self.mesh.fid2cid[:, 0]]
        g = self.g
        mask = self.mesh.bndf_mask
        ub = u_by_face[:, mask]
        hb = ub[0]
        vxb = ub[1] / hb
        vyb = ub[2] / hb

        normalsb = self.mesh.normals[mask]
        proj_len = vxb * normalsb[:,0] + vyb * normalsb[:,1]
        vx_inv = vxb - 2 * proj_len * normalsb[:,0]
        vy_inv = vyb - 2 * proj_len * normalsb[:,1]
        ub_inv = np.array([hb, hb*vx_inv, hb*vy_inv])
        Fxb_inv = np.array([hb*vx_inv, hb*vx_inv**2 + g/2 * hb**2, hb*vx_inv*vy_inv])
        Fyb_inv = np.array([hb*vy_inv, hb*vx_inv*vy_inv, hb*vy_inv**2 + g/2 * hb**2])

        F_bnd = Fxb_inv * normalsb[:,0] + Fyb_inv * normalsb[:,1]
        jmp_bnd = ub_inv - ub

        return F_bnd, jmp_bnd


    def solve_step(self):
        dt = self.dt
        u = self.u
        nface = self.mesh.nface
        g = self.g
        h = u[0]
        vx = u[1] / h
        vy = u[2] / h

        Fx = np.array([h*vx, h*vx**2 + g/2 * h**2, h*vx*vy])
        Fy = np.array([h*vy, h*vx*vy, h*vy**2 + g/2 * h**2])

        c0 = self.mesh.fid2cid[:, 0]
        c1 = self.mesh.fid2cid[:, 1]
        normals = self.mesh.normals
        l = self.mesh.face_len
        areas = self.mesh.areas
        mask = self.mesh.bndf_mask


        F0 = Fx[:, c0] * normals[:,0] + Fy[:, c0] * normals[:, 1]
        F1 = Fx[:, c1] * normals[:,0] + Fy[:, c1] * normals[:, 1]

        spd0 = np.abs([vx[c0] * normals[:, 0] + vy[c0] * normals[:,1]]) + np.sqrt(g * h[c0])
        spd1 = np.abs([vx[c1] * normals[:, 0] + vy[c1] * normals[:,1]]) + np.sqrt(g * h[c1])
        spd = np.maximum(spd0, spd1)

        jmp = u[:,c1] - u[:,c0]

        F_bnd, jmp_bnd = self.wall_bc()
        F1[:, mask] = F_bnd
        jmp[:, mask] = jmp_bnd
        F = (F0+F1)/ 2 - spd * jmp / 2

        flux0 = - dt * F * l / areas[c0]
        flux1 = np.zeros_like(flux0)
        flux1[:, ~mask] = (dt * F * l / areas[c1])[:, ~mask]


        row_idx = np.tile(np.repeat(np.arange(3), nface), 2) #[0 0...0 1 1...1 2 2...2 0 0...0 1 1...1 2 2...2 ]
        col_idx = np.concatenate((np.tile(c0, 3), np.tile(c1, 3))) # [-c0- -c0- -c0- -c1- -c1- -c1-]
        delta = np.concatenate((flux0.ravel(), flux1.ravel()))

        self.u += sparse.coo_matrix((delta, (row_idx, col_idx))).toarray()
        self.time += dt
        return self.time
