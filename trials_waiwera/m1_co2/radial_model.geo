//+
SetFactory("OpenCASCADE");
//+
Rectangle(1) = {0, 0, 0, 1000, 100, 0};
//+
Physical Surface("res", 5) = {1};
//+
Transfinite Curve {3, 1} = 41 Using Progression 1;
//+
Transfinite Curve {4, 2} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
