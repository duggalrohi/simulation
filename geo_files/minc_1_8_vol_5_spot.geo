// Gmsh project created on Tue Feb 23 11:35:41 2021
//SetFactory("OpenCASCADE");

Nx = 7; //number of mesh divisions
Bx=12;
Rx = 1; //growth rate of the mesh divisions
xdim = 10; //dimension x-dirn
ydim = 10; //dimension y-dirn
zdim = -10; //dimension z-dirn
mshdim = 1; //point mesh size

//points for the reservoir boundary
Point(1) = {0, 0, 0, mshdim};
// Point(2) = {xdim, 0, 0, mshdim};
Point(2) = {xdim, ydim, 0, mshdim};

Point(3) = {0, ydim, 0, mshdim};

//lines for the reservoir boundary
Line(1) = {1, 2}; 
Line(2) = {2, 3}; 
Line(3) = {3, 1}; 


// Line(3) = {3, 4}; 
// Line(4) = {4, 1}; 

//dividing lines into elements
Transfinite Curve {1} = Nx Using Progression Rx;
Transfinite Curve {2} = Nx Using Progression Rx;
Transfinite Curve {3} = Bx Using Progression Rx;

// Transfinite Curve {4} = Nx Using Progression Rx;

//surface for the reservoir
Curve Loop(1) = {1, 2, 3}; Plane Surface(1) = {1}; 
// Curve Loop(1) = {1, 2, 3,4}; Plane Surface(1) = {1}; 

// Compound Curve {3, 1};
// Compound Curve {3, 2};
// Compound Curve {1, 2};

//quadrangle elements for the surface
// Transfinite Surface {1}; 

// //mapped mesh of the surface
// Recombine Surface {1};

//depth of the reservoir
// Extrude {0, 0, zdim} {Surface{1}; Layers{1}; Recombine;}

// Physical Volume("reservoir", 1) = {1};


