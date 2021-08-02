MINC Model 1
============

This model is run in Brynhild using the TOUGH2 compatiblity mode (T2Fafnir).

- Use generateT2.py to generate the TOUGH2 input file in the T2 and Brynhild subfolders
- Note that two versions, for fracture spacings 300m and 50m, are created
- Run the TOUGH2 model and rename the output file to FSxxx/T2/TOUGH2.out (for your convenience this file already exists)
- Run the Brynhild 3D models
- Use plotResults.py for comparing the Brynhild to the TOUGH2 output
