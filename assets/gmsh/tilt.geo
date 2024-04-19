// Gmsh project created on Sat Apr  6 21:19:28 2024
lc = 0.15;

Point(1) = {-3, 2, 0, lc};
Point(2) = {-2, 3, 0, lc};
Point(3) = {3, -2, 0, lc};
Point(4) = {2, -3, 0, lc};



Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};


Curve Loop(5) = {1,2,3,4};
Plane Surface(6) = {5};
