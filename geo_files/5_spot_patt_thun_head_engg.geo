// Inputs
x=500; //m
y=500;
z=-305; 
lc=50; //element size or characteristic length for mesh
MeshLayers = 1;
n = 40; //required number of elements
inc = 1; //increment factor of mesh divisions
 
// Geometry
Point(1) = {0, 0, 0, lc};
Point(2) = {x, 0, 0, lc};
Point(3) = {x, y, 0, lc};
Point(4) = {0, y, 0, lc};
Line(1) = {1, 2};				// bottom line
Line(2) = {2, 3};				// right line
Line(3) = {3, 4};				// top line
Line(4) = {4, 1};				// left line
Line Loop(1) = {1, 2, 3, 4}; 	
Plane Surface(1) = {1};
 
//Transfinite surface:
Transfinite Curve {1} = n+1 Using Bump inc/10;
Transfinite Curve {2} = n+1 Using Bump inc/10;
Transfinite Curve {3} = n+1 Using Bump inc/10;
Transfinite Curve {4} = n+1 Using Bump inc/10;
Transfinite Surface {1};
Recombine Surface {1};

Extrude {0, 0, z} {Surface{1};Layers{MeshLayers};Recombine;}
Physical Volume("vol") = 1;
