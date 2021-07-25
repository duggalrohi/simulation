//+
SetFactory("Built-in");
//+
x=500;
y=500;
z=-305;
a=x/6; //distance along x and y
b=(x*Sqrt(2))/11; 
d=b/2; //half increment of the distance along x and y
lc=1;

Point(1)={0,0,0,lc};
Point(2)={0,a/2,0,lc};
Point(3)={0,3*a/2,0,lc};
Point(4)={0,5*a/2,0,lc};
Point(5)={0,7*a/2,0,lc};
Point(6)={0,9*a/2,0,lc};
Point(7)={0,11*a/2,0,lc};
Point(8)={0,12*a/2,0,lc};

Point(9)={a/4,a/4,0,lc};
Point(10)={3*a/4,3*a/4,0,lc};
Point(11)={5*a/4,5*a/4,0,lc};
Point(12)={7/4*a,7/4*a,0,lc};
Point(13)={9/4*a,9/4*a,0,lc};
Point(14)={11/4*a,11/4*a,0,lc};
Point(15)={13/4*a,13/4*a,0,lc};
Point(16)={15/4*a,15/4*a,0,lc};
Point(17)={17/4*a,17/4*a,0,lc};
Point(18)={19/4*a,19/4*a,0,lc};
Point(19)={21/4*a,21/4*a,0,lc};
Point(20)={23/4*a,23/4*a,0,lc};
Point(21)={24/4*a,24/4*a,0,lc};

Point(22)={a/2,12/2*a,0,lc};
Point(23)={3*a/2,12/2*a,0,lc};
Point(24)={5*a/2,12/2*a,0,lc};
Point(25)={7*a/2,12/2*a,0,lc};
Point(26)={9*a/2,12/2*a,0,lc};
Point(27)={11*a/2,12/2*a,0,lc};
Point(28)={12*a/2,12/2*a,0,lc};

Point(29)={a/2,a,0,lc};
Point(30)={a/2,2*a,0,lc};
Point(31)={a/2,3*a,0,lc};
Point(32)={a/2,4*a,0,lc};
Point(33)={a/2,5*a,0,lc};


Point(34)={3/2*a,2*a,0,lc};
Point(35)={5/2*a,3*a,0,lc};
Point(36)={7/2*a,4*a,0,lc};
Point(37)={9/2*a,5*a,0,lc};
Point(38)={a,3/2*a,0,lc};
Point(39)={a,5/2*a,0,lc};
Point(40)={a,7/2*a,0,lc};
Point(41)={a,9/2*a,0,lc};
Point(42)={a,11/2*a,0,lc};

Point(43)={3/2*a,3*a,0,lc};
Point(44)={3/2*a,4*a,0,lc};
Point(45)={3/2*a,5*a,0,lc};
Point(46)={2*a,5/2*a,0,lc};
Point(47)={3*a,7/2*a,0,lc};
Point(48)={4*a,9/2*a,0,lc};
Point(49)={5*a,11/2*a,0,lc};

Point(50)={2*a,7/2*a,0,lc};
Point(51)={3*a,9/2*a,0,lc};
Point(52)={5/2*a,4*a,0,lc};
Point(53)={2*a,9/2*a,0,lc};
Point(54)={2*a,11/2*a,0,lc};
Point(55)={5/2*a,5*a,0,lc};
Point(56)={3*a,11/2*a,0,lc};
Point(57)={7/2*a,5*a,0,lc};
Point(58)={4*a,11/2*a,0,lc};

//+
Line(1) = {1, 9};
//+
Line(2) = {9, 10};
//+
Line(3) = {10, 11};
//+
Line(4) = {11, 12};
//+
Line(5) = {12, 13};
//+
Line(6) = {13, 14};
//+
Line(7) = {14, 15};
//+
Line(8) = {15, 16};
//+
Line(9) = {16, 17};
//+
Line(10) = {17, 18};
//+
Line(11) = {18, 19};
//+
Line(12) = {19, 20};
//+
Line(13) = {20, 21};
//+
Line(14) = {21, 27};
//+
Line(15) = {27, 26};
//+
Line(16) = {26, 25};
//+
Line(17) = {25, 24};
//+
Line(18) = {24, 23};
//+
Line(19) = {23, 22};
//+
Line(20) = {22, 8};
//+
Line(21) = {8, 7};
//+
Line(22) = {7, 6};
//+
Line(23) = {6, 5};
//+
Line(24) = {5, 4};
//+
Line(25) = {4, 3};
//+
Line(26) = {3, 2};
//+
Line(27) = {2, 1};
//+
Line(28) = {2, 29};
//+
Line(29) = {29, 38};
//+
Line(30) = {38, 34};
//+
Line(31) = {34, 46};
//+
Line(32) = {46, 35};
//+
Line(33) = {35, 47};
//+
Line(34) = {47, 36};
//+
Line(35) = {36, 48};
//+
Line(36) = {48, 37};
//+
Line(37) = {37, 49};
//+
Line(38) = {49, 27};
//+
Line(39) = {3, 30};
//+
Line(40) = {30, 39};
//+
Line(41) = {39, 43};
//+
Line(42) = {43, 50};
//+
Line(43) = {50, 52};
//+
Line(44) = {52, 51};
//+
Line(45) = {51, 57};
//+
Line(46) = {57, 58};
//+
Line(47) = {58, 26};
//+
Line(48) = {4, 31};
//+
Line(49) = {31, 40};
//+
Line(50) = {40, 44};
//+
Line(51) = {44, 53};
//+
Line(52) = {53, 55};
//+
Line(53) = {55, 56};
//+
Line(54) = {56, 25};
//+
Line(55) = {5, 32};
//+
Line(56) = {32, 41};
//+
Line(57) = {41, 45};
//+
Line(58) = {45, 54};
//+
Line(59) = {54, 24};
//+
Line(60) = {6, 33};
//+
Line(61) = {33, 42};
//+
Line(62) = {42, 23};
//+
Line(63) = {7, 22};
//+
Line(64) = {9, 2};
//+
Line(65) = {10, 29};
//+
Line(66) = {29, 3};
//+
Line(67) = {11, 38};
//+
Line(68) = {38, 30};
//+
Line(69) = {30, 4};
//+
Line(70) = {12, 34};
//+
Line(71) = {34, 39};
//+
Line(72) = {39, 31};
//+
Line(73) = {31, 5};
//+
Line(74) = {13, 46};
//+
Line(75) = {46, 43};
//+
Line(76) = {43, 40};
//+
Line(77) = {40, 32};
//+
Line(78) = {32, 6};
//+
Line(79) = {14, 35};
//+
Line(80) = {35, 50};
//+
Line(81) = {50, 44};
//+
Line(82) = {44, 41};
//+
Line(83) = {41, 33};
//+
Line(84) = {33, 7};
//+
Line(85) = {15, 47};
//+
Line(86) = {47, 52};
//+
Line(87) = {52, 53};
//+
Line(88) = {53, 45};
//+
Line(89) = {45, 42};
//+
Line(90) = {42, 22};
//+
Line(91) = {16, 36};
//+
Line(92) = {36, 51};
//+
Line(93) = {51, 55};
//+
Line(94) = {55, 54};
//+
Line(95) = {54, 23};
//+
Line(96) = {17, 48};
//+
Line(97) = {48, 57};
//+
Line(98) = {57, 56};
//+
Line(99) = {56, 24};
//+
Line(100) = {18, 37};
//+
Line(101) = {37, 58};
//+
Line(102) = {58, 25};
//+
Line(103) = {19, 49};
//+
Line(104) = {49, 26};
//+
Line(105) = {20, 27};
//+
Curve Loop(1) = {1, 64, 27};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {26, 28, 66};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {25, 39, 69};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {24, 48, 73};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {23, 55, 78};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {22, 60, 84};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {21, 63, 20};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {2, 65, -28, -64};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {29, 68, -39, -66};
//+
Plane Surface(9) = {9};
//+
Curve Loop(10) = {40, 72, -48, -69};
//+
Plane Surface(10) = {10};
//+
Curve Loop(11) = {49, 77, -55, -73};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {56, 83, -60, -78};
//+
Plane Surface(12) = {12};
//+
Curve Loop(13) = {61, 90, -63, -84};
//+
Plane Surface(13) = {13};
//+
Curve Loop(14) = {3, 67, -29, -65};
//+
Plane Surface(14) = {14};
//+
Curve Loop(15) = {30, 71, -40, -68};
//+
Plane Surface(15) = {15};
//+
Curve Loop(16) = {41, 76, -49, -72};
//+
Plane Surface(16) = {16};
//+
Curve Loop(17) = {50, 82, -56, -77};
//+
Plane Surface(17) = {17};
//+
Curve Loop(18) = {57, 89, -61, -83};
//+
Plane Surface(18) = {18};
//+
Curve Loop(19) = {62, 19, -90};
//+
Plane Surface(19) = {19};
//+
Curve Loop(20) = {4, 70, -30, -67};
//+
Plane Surface(20) = {20};
//+
Curve Loop(21) = {31, 75, -41, -71};
//+
Plane Surface(21) = {21};
//+
Curve Loop(22) = {42, 81, -50, -76};
//+
Plane Surface(22) = {22};
//+
Curve Loop(23) = {51, 88, -57, -82};
//+
Plane Surface(23) = {23};
//+
Curve Loop(24) = {58, 95, -62, -89};
//+
Plane Surface(24) = {24};
//+
Curve Loop(25) = {5, 74, -31, -70};
//+
Plane Surface(25) = {25};
//+
Curve Loop(26) = {32, 80, -42, -75};
//+
Plane Surface(26) = {26};
//+
Curve Loop(27) = {43, 87, -51, -81};
//+
Plane Surface(27) = {27};
//+
Curve Loop(28) = {52, 94, -58, -88};
//+
Plane Surface(28) = {28};
//+
Curve Loop(29) = {59, 18, -95};
//+
Plane Surface(29) = {29};
//+
Curve Loop(30) = {6, 79, -32, -74};
//+
Plane Surface(30) = {30};
//+
Curve Loop(31) = {33, 86, -43, -80};
//+
Plane Surface(31) = {31};
//+
Curve Loop(32) = {44, 93, -52, -87};
//+
Plane Surface(32) = {32};
//+
Curve Loop(33) = {53, 99, -59, -94};
//+
Plane Surface(33) = {33};
//+
Curve Loop(34) = {7, 85, -33, -79};
//+
Plane Surface(34) = {34};
//+
Curve Loop(35) = {34, 92, -44, -86};
//+
Plane Surface(35) = {35};
//+
Curve Loop(36) = {45, 98, -53, -93};
//+
Plane Surface(36) = {36};
//+
Curve Loop(37) = {54, 17, -99};
//+
Plane Surface(37) = {37};
//+
Curve Loop(38) = {8, 91, -34, -85};
//+
Plane Surface(38) = {38};
//+
Curve Loop(39) = {35, 97, -45, -92};
//+
Plane Surface(39) = {39};
//+
Curve Loop(40) = {46, 102, -54, -98};
//+
Plane Surface(40) = {40};
//+
Curve Loop(41) = {9, 96, -35, -91};
//+
Plane Surface(41) = {41};
//+
Curve Loop(42) = {36, 101, -46, -97};
//+
Plane Surface(42) = {42};
//+
Curve Loop(43) = {47, 16, -102};
//+
Plane Surface(43) = {43};
//+
Curve Loop(44) = {10, 100, -36, -96};
//+
Plane Surface(44) = {44};
//+
Curve Loop(45) = {37, 104, -47, -101};
//+
Plane Surface(45) = {45};
//+
Curve Loop(46) = {11, 103, -37, -100};
//+
Plane Surface(46) = {46};
//+
Curve Loop(47) = {38, 15, -104};
//+
Plane Surface(47) = {47};
//+
Curve Loop(48) = {12, 105, -38, -103};
//+
Plane Surface(48) = {48};
//+
Curve Loop(49) = {13, 14, -105};
//+
Plane Surface(49) = {49};
//+
Transfinite Curve {27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 105, 103, 100, 96, 91, 85, 79, 74, 70, 67, 65, 64, 66, 68, 71, 75, 80, 86, 92, 97, 101, 104, 39, 40, 41, 42, 43, 44, 45, 46, 47, 69, 72, 76, 81, 87, 93, 98, 102, 48, 49, 50, 51, 52, 53, 54, 73, 77, 82, 88, 94, 99, 55, 56, 57, 58, 59, 78, 83, 89, 95, 60, 61, 62, 84, 90, 63} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Transfinite Surface {6};
//+
Transfinite Surface {7};
//+
Transfinite Surface {8};
//+
Transfinite Surface {9};
//+
Transfinite Surface {10};
//+
Transfinite Surface {11};
//+
Transfinite Surface {12};
//+
Transfinite Surface {13};
//+
Transfinite Surface {14};
//+
Transfinite Surface {15};
//+
Transfinite Surface {16};
//+
Transfinite Surface {17};
//+
Transfinite Surface {18};
//+
Transfinite Surface {19};
//+
Transfinite Surface {20};
//+
Transfinite Surface {21};
//+
Transfinite Surface {22};
//+
Transfinite Surface {23};
//+
Transfinite Surface {24};
//+
Transfinite Surface {25};
//+
Transfinite Surface {26};
//+
Transfinite Surface {27};
//+
Transfinite Surface {28};
//+
Transfinite Surface {29};
//+
Transfinite Surface {30};
//+
Transfinite Surface {31};
//+
Transfinite Surface {32};
//+
Transfinite Surface {33};
//+
Transfinite Surface {34};
//+
Transfinite Surface {35};
//+
Transfinite Surface {36};
//+
Transfinite Surface {37};
//+
Transfinite Surface {38};
//+
Transfinite Surface {39};
//+
Transfinite Surface {40};
//+
Transfinite Surface {41};
//+
Transfinite Surface {42};
//+
Transfinite Surface {43};
//+
Transfinite Surface {44};
//+
Transfinite Surface {45};
//+
Transfinite Surface {46};
//+
Transfinite Surface {47};
//+
Transfinite Surface {48};
//+
Transfinite Surface {49};
//+
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49};
//+
Extrude {0, 0, -305} {
  Surface{1}; Surface{2}; Surface{3}; Surface{4}; Surface{5}; Surface{6}; Surface{7}; Surface{8}; Surface{9}; Surface{10}; Surface{11}; Surface{12}; Surface{13}; Surface{14}; Surface{15}; Surface{16}; Surface{17}; Surface{18}; Surface{19}; Surface{20}; Surface{21}; Surface{22}; Surface{23}; Surface{24}; Surface{25}; Surface{26}; Surface{27}; Surface{28}; Surface{29}; Surface{30}; Surface{31}; Surface{32}; Surface{33}; Surface{34}; Surface{35}; Surface{36}; Surface{37}; Surface{38}; Surface{39}; Surface{40}; Surface{41}; Surface{42}; Surface{43}; Surface{44}; Surface{45}; Surface{46}; Surface{47}; Surface{48}; Surface{49}; Layers {1}; Recombine;
}
//+
Physical Volume("r", 1119) = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49};
