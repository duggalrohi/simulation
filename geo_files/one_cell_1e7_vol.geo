// Gmsh project created on Tue Feb 23 11:35:41 2021
//SetFactory("OpenCASCADE");

Nx = 2; //number of mesh divisions
Rx = 1; //growth rate of the mesh divisions
xdim = 100; //dimension x-dirn
ydim = 100; //dimension y-dirn
zdim = 1000; //dimension z-dirn
mshdim = 1; //point mesh size

//points for the reservoir boundary
Point(1) = {0, 0, 0, mshdim};
Point(2) = {xdim, 0, 0, mshdim};
Point(3) = {xdim, ydim, 0, mshdim};
Point(4) = {0, ydim, 0, mshdim};

//lines for the reservoir boundary
Line(1) = {1, 2}; 
Line(2) = {2, 3}; 
Line(3) = {3, 4}; 
Line(4) = {4, 1}; 

//dividing lines into elements
Transfinite Curve {1} = Nx Using Progression Rx;
Transfinite Curve {2} = Nx Using Progression Rx;
Transfinite Curve {3} = Nx Using Progression Rx;
Transfinite Curve {4} = Nx Using Progression Rx;

//surface for the reservoir
Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1}; 

//quadrangle elements for the surface
Transfinite Surface {1}; 

//mapped mesh of the surface
Recombine Surface {1};

//Physical Surface("reservoir surface", 1) = {1};
//depth of the reservoir
//Extrude {0, 0, zdim} {Surface{1}; Curve{8}; Curve{5}; Curve{6}; Curve{7}; Point{1}; Point{2}; Point{3}; Point{4}; Layers{1}; Recombine;}

Extrude {0, 0, zdim} {Surface{1}; Layers{1}; Recombine;}
Physical Volume("reservoir", 31) = {1};
