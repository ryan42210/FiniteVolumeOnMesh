lc = 0.2;
lc2 = 0.3;
r1 = 0.2;

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


Point(6) = {-5,-2,0,lc2};
Point(7) = {-5,2,0,lc2};
Point(8) = {5,2,0,lc2};
Point(9) = {5,-2,0,lc2};


c_pts1[] = Translate {0, 0.8, 0} { Duplicata{ Point {1,2,3,4,5}; } };
Circle(11) = {c_pts1[2], c_pts1[0], c_pts1[3]};
Circle(12) = {c_pts1[3], c_pts1[0], c_pts1[4]};
Circle(13) = {c_pts1[4], c_pts1[0], c_pts1[1]};
Circle(14) = {c_pts1[1], c_pts1[0], c_pts1[2]};
Curve Loop(15) = {11,12,13,14};


c_pts2[] = Translate {0, 1.6, 0} { Duplicata{ Point {1,2,3,4,5}; } };
Circle(21) = {c_pts2[2], c_pts2[0], c_pts2[3]};
Circle(22) = {c_pts2[3], c_pts2[0], c_pts2[4]};
Circle(23) = {c_pts2[4], c_pts2[0], c_pts2[1]};
Circle(24) = {c_pts2[1], c_pts2[0], c_pts2[2]};
Curve Loop(25) = {21,22,23,24};


c_pts3[] = Translate {0, -0.8, 0} { Duplicata{ Point {1,2,3,4,5}; } };
Circle(31) = {c_pts3[2], c_pts3[0], c_pts3[3]};
Circle(32) = {c_pts3[3], c_pts3[0], c_pts3[4]};
Circle(33) = {c_pts3[4], c_pts3[0], c_pts3[1]};
Circle(34) = {c_pts3[1], c_pts3[0], c_pts3[2]};
Curve Loop(35) = {31,32,33,34};

c_pts4[] = Translate {0, -1.6, 0} { Duplicata{ Point {1,2,3,4,5}; } };
Circle(41) = {c_pts4[2], c_pts4[0], c_pts4[3]};
Circle(42) = {c_pts4[3], c_pts4[0], c_pts4[4]};
Circle(43) = {c_pts4[4], c_pts4[0], c_pts4[1]};
Circle(44) = {c_pts4[1], c_pts4[0], c_pts4[2]};
Curve Loop(45) = {41,42,43,44};


c_pts5[] = Translate {-0.5, 1.2, 0} { Duplicata{ Point {1,2,3,4,5}; } };
Circle(51) = {c_pts5[2], c_pts5[0], c_pts5[3]};
Circle(52) = {c_pts5[3], c_pts5[0], c_pts5[4]};
Circle(53) = {c_pts5[4], c_pts5[0], c_pts5[1]};
Circle(54) = {c_pts5[1], c_pts5[0], c_pts5[2]};
Curve Loop(55) = {51,52,53,54};

c_pts6[] = Translate {-0.5, 0.4, 0} { Duplicata{ Point {1,2,3,4,5}; } };
Circle(61) = {c_pts6[2], c_pts6[0], c_pts6[3]};
Circle(62) = {c_pts6[3], c_pts6[0], c_pts6[4]};
Circle(63) = {c_pts6[4], c_pts6[0], c_pts6[1]};
Circle(64) = {c_pts6[1], c_pts6[0], c_pts6[2]};
Curve Loop(65) = {61,62,63,64};


c_pts7[] = Translate {-0.5, -0.4, 0} { Duplicata{ Point {1,2,3,4,5}; } };
Circle(71) = {c_pts7[2], c_pts7[0], c_pts7[3]};
Circle(72) = {c_pts7[3], c_pts7[0], c_pts7[4]};
Circle(73) = {c_pts7[4], c_pts7[0], c_pts7[1]};
Circle(74) = {c_pts7[1], c_pts7[0], c_pts7[2]};
Curve Loop(75) = {71,72,73,74};


c_pts8[] = Translate {-0.5, -1.2, 0} { Duplicata{ Point {1,2,3,4,5}; } };
Circle(81) = {c_pts8[2], c_pts8[0], c_pts8[3]};
Circle(82) = {c_pts8[3], c_pts8[0], c_pts8[4]};
Circle(83) = {c_pts8[4], c_pts8[0], c_pts8[1]};
Circle(84) = {c_pts8[1], c_pts8[0], c_pts8[2]};
Curve Loop(85) = {81,82,83,84};


// c_pts9[] = Translate {-0.5, -2, 0} { Duplicata{ Point {1,2,3,4}; } };
// Circle(11) = {c_pts1[2], c_pts1[0], c_pts1[3]};
// Circle(12) = {c_pts1[3], c_pts1[0], c_pts1[4]};
// Circle(13) = {c_pts1[4], c_pts1[0], c_pts1[1]};
// Circle(14) = {c_pts1[1], c_pts1[0], c_pts1[2]};
// Curve Loop(15) = {11,12,13,14};

c_pts0[] = Translate {-0.5, 2, 0} { Duplicata{ Point {1,2,4,5}; } };
Circle(16) = {c_pts0[1], c_pts0[0], c_pts0[3]};
Circle(17) = {c_pts0[3], c_pts0[0], c_pts0[2]};

c_pts9[] = Translate {-0.5, -2, 0} { Duplicata{ Point {1,2,3,4}; } };
Circle(26) = {c_pts9[1], c_pts9[0], c_pts9[2]};
Circle(27) = {c_pts9[2], c_pts9[0], c_pts9[3]};

Line(91) = {6,7};
Line(92) = {7,c_pts0[1]};
Line(93) = {c_pts0[2],8};
Line(94) = {8,9};
Line(95) = {9,c_pts9[3]};
Line(96) = {c_pts9[1],6};
Curve Loop(100) = {91,92,16,17,93,94,95,-27,-26,96};

// Plane Surface(12) = {my_new_surfs[0]};

// Plane Surface(12) = {5}
Plane Surface(11) = {5,15,25,35,45,55,65,75,85,100};

Mesh 2;
// Save "breakwater.ply2";