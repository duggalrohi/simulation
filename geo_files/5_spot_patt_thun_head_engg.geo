// Inputs
x=500; //m
y=500;
z=-305; 
ElementSize=1;
MeshLayers = 1;
nodes = 21; //required number of elements - 1, i.e., it is number of nodes
inc = 1; //increment factor of mesh divisions
 
// Geometry
Point(1) = {0, 0, 0, x};
Point(2) = {x, 0, 0, x};
Point(3) = {x, y, 0, x};
Point(4) = {0, y, 0, x};
Line(1) = {1, 2};				// bottom line
Line(2) = {2, 3};				// right line
Line(3) = {3, 4};				// top line
Line(4) = {4, 1};				// left line
Line Loop(1) = {1, 2, 3, 4}; 	
Plane Surface(1) = {1};
 
//Transfinite surface:
Transfinite Curve {1,2,3,4} = nodes Using Progression inc;
Transfinite Surface {1};
Recombine Surface {1};
//Physical Surface("r", 5) = {1};
 
Extrude {0, 0, z} {Surface{1};Layers{MeshLayers};Recombine;}
Physical Volume("vol") = 1;

