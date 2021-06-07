//+
SetFactory("OpenCASCADE");
//+
Rectangle(1) = {0, 0, 0, 1.0, -1.0, 0};
//+
Transfinite Curve {1, 3} = 2 Using Progression 1;
//+
Transfinite Curve {4, 2} = 2 Using Progression 1;
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
//zdim = 1000.0;
//Extrude {0, 0, zdim} {Surface{1}; Layers{21}; Recombine;}
//Physical Volume("reservoir", 13) = {1};
Physical Surface("reservoir", 1) = {1};
Coherence Mesh;
RenumberMeshNodes;
RenumberMeshElements;

