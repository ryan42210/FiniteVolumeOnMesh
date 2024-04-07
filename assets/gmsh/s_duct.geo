// Gmsh project created on Sat Apr  6 21:19:28 2024
lc = 0.2;
Point(1) = {-2.5, 2, 0, 0.15};
Point(2) = {-2, 3, 0, 0.2};
Point(3) = {2.5, -2, 0, 0.15};
Point(4) = {2, -3, 0, 0.2};

Point(5) = {-4, 2, 0, 0.3};
Point(6) = {-3, 2, 0, 0.3};
Point(7) = {-4, 3, 0, 0.3};
Point(8) = {-3, 3, 0, 0.3};

Point(9) = {4, -2, 0, 0.3};
Point(10) = {4, -3, 0, 0.3};

Line(1) = {1,6};
Line(2) = {6,8};
Line(3) = {8,2};
Line(4) = {2,3};
Line(5) = {3,9};
Line(6) = {9,10};
Line(7) = {10,4};
Line(8) = {4,1};

Line(9) = {6,5};
Line(10) = {5,7};
Line(11) = {7,8};

Curve Loop(12) = {1,2,3,4,5,6,7,8};
Plane Surface(13) = {12};

Curve Loop(14) = {9,10,11,-2};
Plane Surface(15) = {14};