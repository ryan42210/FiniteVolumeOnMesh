// Gmsh project created on Sat Apr 13 18:38:18 2024

lc = 0.1;
r1 = 1;
r2 = 0.3;

Point(1) = {0,0,0,lc};
Point(2) = {-r1,0,0,lc};
Point(3) = {0,r1,0,lc};
Point(4) = {r1,0,0,lc};
Point(5) = {0,-r1,0,lc};

Circle(1) = {2,1,3};
Circle(2) = {3,1,4};
Circle(3) = {4,1,5};
Circle(4) = {5,1,2};
Curve Loop(5) = {1,2,3,4};

Point(6) = {-r2,0,0,lc};
Point(7) = {0,r2,0,lc};
Point(8) = {r2,0,0,lc};
Point(9) = {0,-r2,0,lc};

Circle(7) = {6,1,7};
Circle(8) = {7,1,8};
Circle(9) = {8,1,9};
Circle(10) = {9,1,6};
Curve Loop(11) = {7,8,9,10};


Plane Surface(6) = {5,11};
Plane Surface(7) = {11};