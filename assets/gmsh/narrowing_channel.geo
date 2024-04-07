// Gmsh project created on Sat Apr  6 18:52:22 2024

lc = 0.3;

Point(1) = {-4.5, -2, 0, lc};
Point(2) = {-4.5, 2, 0, lc};
Point(3) = {-3, 2, 0, lc};
Point(4) = {-3, -2, 0, lc};

Point(5) = {-1, 1, 0, lc/2};
Point(6) = {0, 3, 0, lc/2};
Point(7) = {1, 1, 0, lc/2};


Point(8) = {-1, -1, 0, lc/2};
Point(9) = {0, -3, 0, lc/2};
Point(10) = {1, -1, 0, lc/2};


Point(11) = {3, 2, 0, lc};
Point(12) = {4.5, 2, 0, lc};
Point(13) = {4.5, -2, 0, lc};
Point(14) = {3, -2, 0, lc};

Point(15) = {-6, 2, 0, lc};
Point(16) = {-6, -2, 0, lc};

Line(1) = {4, 1};
Line(2) = {1, 2};
Line(3) = {2, 3};
Line(4) = {3, 5};
Line(5) = {8, 4};

Line(6) = {7, 11};
Line(7) = {11, 12};
Line(8) = {12, 13};
Line(9) = {13, 14};
Line(10) = {14, 10};

Circle(11) = {5, 6, 7};
Circle(12) = {8, 9, 10};

Curve Loop(13) = {1,2,3,4,11,6,7,8,9,10,-12,5};
Plane Surface(14) = {13};

Line(15) = {16, 15};
Line(16) = {15, 2};
Line(17) = {1, 16};

Curve Loop(18) = {15,16,-2,17};
Plane Surface(19) = {18};
// interor boundary