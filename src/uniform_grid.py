import numpy as np
import matplotlib.pyplot as plt


class UniformGrid:
    def __init__(self, xrange, yrange, mask_func):
        x_lo, x_hi, nx = xrange
        y_lo, y_hi, ny = yrange
        x, hx = np.linspace(x_lo, x_hi, nx, endpoint=False, retstep=True)
        y, hy = np.linspace(y_lo, y_hi, ny, endpoint=False, retstep=True)
        # Shift x and y by half cell size. store value at the cell center.
        x += hx / 2
        y += hy / 2

        Kx = np.arange(0, nx)
        Kxm1 = np.roll(Kx, 1)
        Kxp1 = np.roll(Kx, -1)
        Ky = np.arange(0, ny)
        Kym1 = np.roll(Ky, 1)
        Kyp1 = np.roll(Ky, -1)

        u = np.zeros((3, ny, nx))

        xx, yy = np.meshgrid(x,y)
        # print(xx.shape)
        ic = lambda X, Y: np.where(xx**2 + yy**2 < 0.09, 3, 1)
        u[0] = ic(xx, yy)

        mask= mask_func(xx, yy)

        self.xx = xx
        self.yy = yy
        self.hx = hx
        self.hy = hy
        self.nx = nx
        self.ny = ny
        self.Kxp1 = Kxp1
        self.Kxm1 = Kxm1
        self.Kyp1 = Kyp1
        self.Kym1 = Kym1
        self.mask = mask
        self.x_bnd_idx = mask.astype(np.int32) - mask[:,Kxp1].astype(np.int32)
        self.y_bnd_idx = mask.astype(np.int32) - mask[Kyp1].astype(np.int32)

    def plot(self):
        print("Total active cell number in uniform grid: ", self.mask.sum())

class GridSolver:
    def __init__(self, grid: UniformGrid, dt = 5e-3, g = 1):
        self.dt = dt
        self.grid = grid
        self.time = 0
        self.g = g
        self.u = np.zeros((3, grid.ny, grid.nx))
        

    def init_height(self, func):
        self.u[0] = func(self.grid.xx, self.grid.yy)


    def solve_step(self):
        u = self.u
        g = self.g

        x_bnd_idx = self.grid.x_bnd_idx
        y_bnd_idx = self.grid.y_bnd_idx

        Kxp1 = self.grid.Kxp1
        Kyp1 = self.grid.Kyp1
        Kxm1 = self.grid.Kxm1
        Kym1 = self.grid.Kym1

        mask = self.grid.mask

        h, mx, my = u[0], u[1], u[2]
        vx = mx / h
        vy = my / h

        # x normal direction points towards right

        Fx = np.array([h*vx, h*vx**2 + g/2 * h**2, h*vx*vy])
        Fy = np.array([h*vy, h*vx*vy, h*vy**2 + g/2 * h**2])
        F_avgx = (Fx + Fx[:,:,Kxp1])/2
        F_avgy = (Fy + Fy[:,Kyp1,:])/2
        
        Fx_inv = np.array([-h*vx, h*vx**2 + g/2 * h**2, -h*vx*vy])
        Fy_inv = np.array([-h*vy, -h*vx*vy, h*vy**2 + g/2 * h**2])
        F_avgx[:,x_bnd_idx == 1] = ((Fx + Fx_inv)/2)[:,x_bnd_idx == 1]
        F_avgx[:,x_bnd_idx == -1] = ((Fx + Fx_inv)/2)[:,:,Kxp1][:,x_bnd_idx == -1]
        F_avgy[:,y_bnd_idx == 1] = ((Fy + Fy_inv)/2)[:,y_bnd_idx == 1]
        F_avgy[:,y_bnd_idx == -1] = ((Fy + Fy_inv)/2)[:,Kyp1,:][:,y_bnd_idx == -1]


        max_eigval_x = np.abs(vx) + np.sqrt(g * h)
        max_eigval_y = np.abs(vy) + np.sqrt(g * h)
        spd_x = np.maximum(max_eigval_x, max_eigval_x[:, Kxp1])
        spd_y = np.maximum(max_eigval_y, max_eigval_y[Kyp1,:])
        spd_x[x_bnd_idx == 1] = max_eigval_x[x_bnd_idx == 1]
        spd_x[x_bnd_idx == -1] = max_eigval_x[:,Kxp1][x_bnd_idx == -1]
        spd_y[y_bnd_idx == 1] = max_eigval_y[y_bnd_idx == 1]
        spd_y[y_bnd_idx == -1] = max_eigval_y[Kyp1,:][y_bnd_idx == -1]


        jmp_x = u[:,:,Kxp1] - u
        jmp_y = u[:,Kyp1,:] - u

        jmp_x[:,x_bnd_idx == 1] = np.array([h-h, -2*mx, my-my])[:,x_bnd_idx == 1]
        jmp_x[:,x_bnd_idx == -1] = np.array([h-h, 2*mx[:,Kxp1], my-my])[:,x_bnd_idx == -1]
        jmp_y[:,y_bnd_idx == 1] = np.array([h-h, mx-mx, -2*my])[:,y_bnd_idx == 1]
        jmp_y[:,y_bnd_idx == -1] = np.array([h-h, mx-mx, 2*my[Kyp1,:]])[:,y_bnd_idx == -1]

        flux_x = F_avgx - spd_x * jmp_x / 2
        flux_y = F_avgy - spd_y * jmp_y / 2

        u[:,mask] -= (self.dt/self.grid.hx * (flux_x - flux_x[:, :, Kxm1]) + self.dt/self.grid.hy * (flux_y - flux_y[:, Kym1]))[:,mask]
        self.time += self.dt
        return self.time
