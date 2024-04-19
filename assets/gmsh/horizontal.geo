
lc = 0.15;
y = Sqrt(2);
x = 5*Sqrt(2);

Point(1) = {0, 0, 0, lc};
Point(2) = {0, y, 0, lc};
Point(3) = {x, y, 0, lc};
Point(4) = {x, 0, 0, lc};



Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};


Curve Loop(5) = {1,2,3,4};
Plane Surface(6) = {5};
