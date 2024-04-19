# Solve SWE with the FV on Unstructured Grid

Solving Shallow Water Equation (SWE) with cell-centered Finite Volume Method on unstructured grid.

Shallow water equation:

$$\frac{\partial}{\partial t} 
\begin{bmatrix}
    h\\
    hv_x\\
    hv_y
\end{bmatrix}
+ \frac{\partial}{\partial t} 
\begin{bmatrix}
    hv_x\\
    hv_x^2 + gh^2/2\\
    hv_xv_y
\end{bmatrix}
+ \frac{\partial}{\partial t} 
\begin{bmatrix}
    hv_y\\
    hv_xv_y\\
    hv_y^2 + gh^2/2
\end{bmatrix}
=0$$

Solving SWE using a FV method of Lax-Friedrichs type in 2D. Use perfect wall boundary condition.