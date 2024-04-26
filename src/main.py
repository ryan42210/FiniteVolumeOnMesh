import numpy as np

from matplotlib import rcParams
import matplotlib.pyplot as plt
from  matplotlib import animation
from matplotlib.colors import Normalize
from matplotlib import cm
from tqdm import tqdm

from uniform_grid import *
from unstructured import *


def simulate_and_plot(m_solver: MeshSolver, g_solver: GridSolver, target_time, dt, fps, speed_up, norm_h, norm_v):
    frames = []
    frame_timer = 0
    total_steps = int(target_time / dt)

    if g_solver != None:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        for ax in axes.ravel():
            ax.set_aspect(1)

        axes[0,0].set_title("Water height (mesh)")
        axes[0,1].set_title("velocity magnitude (mesh)")
        axes[1,0].set_title("Water height (uniform gird)")
        axes[1,1].set_title("velocity magnitude (uniform grid)")
        fig.colorbar(cm.ScalarMappable(norm=norm_h), ax=axes[0,0], location='bottom')
        fig.colorbar(cm.ScalarMappable(norm=norm_v), ax=axes[0,1], location='bottom')
        fig.colorbar(cm.ScalarMappable(norm=norm_h), ax=axes[1,0], location='bottom')
        fig.colorbar(cm.ScalarMappable(norm=norm_v), ax=axes[1,1], location='bottom')

    else:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        for ax in axes:
            ax.set_aspect(1)

        axes[0].set_title("Water height (mesh)")
        axes[1].set_title("velocity magnitude (mesh)")

        fig.colorbar(cm.ScalarMappable(norm=norm_h), ax=axes[0], location='bottom')
        fig.colorbar(cm.ScalarMappable(norm=norm_v), ax=axes[1], location='bottom')



    for i in tqdm(range(total_steps)):
        if m_solver.time >= frame_timer:
            frame_timer += speed_up/fps
            vx = m_solver.u[1] / m_solver.u[0]
            vy = m_solver.u[2] / m_solver.u[0]

            if g_solver != None:
                im_h_m = axes[0,0].tripcolor(m_solver.mesh.t, m_solver.u[0], animated=True, norm=norm_h)
                im_v_m = axes[0,1].tripcolor(m_solver.mesh.t, np.sqrt(vx**2 + vy**2), animated=True, norm=norm_v)
                vx_g = g_solver.u[1] / g_solver.u[0]
                vy_g = g_solver.u[2] / g_solver.u[0]
                im_h_g = axes[1,0].pcolormesh(g_solver.grid.xx, g_solver.grid.yy, np.where(g_solver.grid.mask, g_solver.u[0], np.nan), animated=True, norm=norm_h)
                im_v_g = axes[1,1].pcolormesh(g_solver.grid.xx, g_solver.grid.yy, np.where(g_solver.grid.mask, np.sqrt(vx_g**2 + vy_g**2), np.nan), animated=True, norm=norm_v)
                frames.append([im_h_m, im_v_m, im_h_g, im_v_g])
            else:
                im_h = axes[0].tripcolor(m_solver.mesh.t, m_solver.u[0], animated=True, norm=norm_h)
                im_v = axes[1].tripcolor(m_solver.mesh.t, np.sqrt(vx**2 + vy**2), animated=True, norm=norm_v)
                frames.append([im_h, im_v])

        m_solver.solve_step()
        if g_solver != None:
            g_solver.solve_step()


    print("start creating animation...")
    rcParams['animation.embed_limit'] = 64
    plt.close()
    return animation.ArtistAnimation(fig, frames, interval=1e3/fps, blit=True)

