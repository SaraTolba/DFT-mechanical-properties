# DFT Mechanical Properties
Extracts elastic tensor and calculate the various mechanical properties from VASP finite difference results.

This script reads an OUTCAR file and extracts the elastic tensor data from it. The elastic tensor is then used to calculate the various bulk and shear moduli, as well as the Poisson ratio of the material.

## How To Use 
To use the script, the OUTCAR file must be in the same directory as the script and the file path must be updated in the open function.

`python vasp-mech.py`

A file named Mechanical_data.txt will be created in the same directory as the OUTCAR file after running the code.

## Contributions
If you have any suggestions or find any errors in the code, please do not hesitate to contact me at [sarahtolba1@gmail.com] or open an issue in the repository. Any contributions or feedback is greatly appreciated.

### References 
- ELASTIC CONSTANTS AND THERMAL EXPANSION AVERAGES OF A NONTEXTURED POLYCRYSTAL By ROLAND DEWIT. JOURNAL OF MECHANICS OF MATERIALS AND STRUCTURES Vol. 3, No. 2, 2008.

Enjoy :) 
