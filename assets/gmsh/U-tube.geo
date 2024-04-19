// A U-shape domain with 2D mesh inside

lc = 0.05;

// left rectangle
Point(1) = {-2, 0, 0, lc};
Point(2) = {-2, 3, 0, lc};
Point(3) = {-1, 3, 0, lc};
Point(4) = {-1, 0, 0, lc};

// origin point
Point(5) = {0, 0, 0, lc};

// right rectangle
Point(6) = {1, 0, 0, lc};
Point(7) = {1, 3, 0, lc};
Point(8) = {2, 3, 0, lc};
Point(9) = {2, 0, 0, lc};

// circle apex
Point(10) = {0, -1, 0, lc};
Point(11) = {0, -2, 0, lc};


Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};

Circle(4) = {4, 5, 10};
Circle(5) = {10, 5, 6};

Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 9};

Circle(9) = {9, 5, 11};
Circle(10) = {11, 5, 1};

// Line(11) = {1, 4};

Curve Loop(12) = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
Plane Surface(13) = {12};

