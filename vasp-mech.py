import numpy as np


#this file reads the elastic tensor from the OUTCAR.

# open the file and read all lines
with open('/path/to/OUTCAR', 'r') as f:
    lines = f.readlines()

# initialize variables
copy = False
elastic_tensor = []
for line in lines:
    # split the line by whitespace and get the input list
    inp = line.split()
    
    # skip empty lines 
    if inp == []:
        continue
    
    # skip lines with less than 4 or more than 7 items
    if len(inp) < 4 or len(inp) > 7:
        continue
    
    # check if we are at the start of the elastic tensor data
    if len(inp) == 4 and inp[0] == 'TOTAL':
        copy = True
    
    # if we are at the right place, extract the elastic tensor data
    if copy:
        if len(inp) == 7 and len(inp[0]) == 2:
            elastic_tensor.append(inp[1:])
        # if the elastic tensor list has 6 items, stop the loop
if len(elastic_tensor) == 6:
    # convert the list of elastic tensor data to a numpy array and return it
    elastic_tensor = np.asarray(elastic_tensor).astype(float)


#----convert kBar to GPa
Cij = elastic_tensor/10

# #----Calculate compliance tensor 
Sij = np.linalg.inv(Cij)		#inverse of a matrix.

# #----calculate Voigt bulk modulus  #9Kv = (c11 + c22 + c33) + 2(c12 + c23 + c13)
Kv = ((Cij[0,0] + Cij[1,1] + Cij[2,2]) + 2 * (Cij[0,1] + Cij[1,2] + Cij[0,2]))/9

# #----Reuss bulk modulus $K_R$ $(GPa)$ #1/Kr = (s11 + s22 + s33) + 2(s12 + s23 + s13 )
Kr = 1/((Sij[0,0] + Sij[1,1] + Sij[2,2]) + 2 * (Sij[0,1] + Sij[1,2] + Sij[0,2]))

# #----Voigt-Reuss-Hill bulk modulus
Kvrh = (Kv+Kr)/2

#----Voigt shear modulus Gv (GPa)  #15Gv = (c11 + c22 + c33) − (c12 + c23 + c13 ) + 3(c44 + c55 + c66)
# NOTE: vasp generate XX YY ZZ	XY	YZ	ZX
#                   = 00 11 22  33  44  55
# while it should be  XX YY	ZZ	YZ	ZX	XY
#                   = 00 11 22  33  44  55
Gv = ((Cij[0,0] + Cij[1,1] + Cij[2,2]) - (4*(Cij[0,1] + Cij[1,2] + Cij[0,2])) + (3*(Cij[4,4] + Cij[5,5] + Cij[3,3]))/15)

#----Reuss shear modulus Gv (GPa) #15/Gr = = 4(s11 + s22 + s33) − 4(s12 + s23 + s13 ) + 3(s44 + s55 + s66).
Gr = 15/(4*(Sij[0,0] + Sij[1,1] + Sij[2,2]) - (4*(Sij[0,1] + Sij[1,2] + Sij[0,2])) + (3*(Sij[4,4] + Sij[5,5] + Sij[3,3])))

#----Voigt-Reuss-Hill shear modulus 
Gvrh = (Gv+Gr)/2

#----Isotropic Poisson ratio 
mu = ((3 * Kvrh) - (2 * Gvrh))/((6 * Kvrh) + (2 * Gvrh) )

#---- Young’s modulus E
E = (9*Kvrh*Gvrh)/((3*Kvrh) +  Gvrh )


### You may change the output file name here: 

with open('Mechanical_data.txt', 'w') as f:
	
    #----write the array to a file as comma-separated values
    f.write("The Total Elastic Tensor in KBar\n")
    # np.savetxt(f, np.asarray(elastic_tensor).astype(float), fmt='%.2f,%.2f,%.2f,%.2f,%.2f,%.2f', newline='\n', delimiter=' ',  header='XX YY ZZ XY YZ ZX')
    np.savetxt(f, elastic_tensor, newline='\n', delimiter=' '
                ,fmt='%f', header='XX YY ZZ XY YZ ZX'
                ,footer ='-----------------------------------------------')  
    # write a newline character to separate the data
    f.write('\n')
#     
    f.write("The Total Elastic Tensor in GPa\n")
    np.savetxt(f, Cij, newline='\n', delimiter=' '
                ,fmt='%f', header='XX YY ZZ XY YZ ZX'
                ,footer ='-----------------------------------------------')
#     # write a newline character to separate the data
#     f.write(b'\n')
#     
    f.write("The compliance tensor in GPa^-1\n")
    np.savetxt(f, Sij, newline='\n', delimiter=' '
                ,fmt='%f', header='XX YY ZZ XY YZ ZX'
                ,footer ='-----------------------------------------------') 
    # write a newline character to separate the data
    f.write('\n')
    
    f.write("The value of Voigt bulk modulus (Kv) (GPa) is = {}\n".format(Kv))
    
    # write a newline character to separate the data
    f.write('\n')
    
    f.write("The value of Reuss bulk modulus (Kr) (GPa) is = {}\n".format(Kr))
    
    # write a newline character to separate the data
    f.write('\n')
    
    f.write("The value of Voigt shear modulus (Gv) (GPa) is = {}\n".format(Gv))
    
    # write a newline character to separate the data
    f.write('\n')
    
    f.write("The value of Reuss shear modulus (Gr) (GPa) is = {}\n".format(Gr))
    
    # write a newline character to separate the data
    f.write('\n')
    
    f.write("The value of Voigt-Reuss-Hill bulk modulus (Kvrh) (GPa) is = {}\n".format(Kvrh))
    
    # write a newline character to separate the data
    f.write('\n')
    
    f.write("The value of Voigt-Reuss-Hill shear modulus (Gvrh) (GPa) is = {}\n".format(Gvrh))
    
    # write a newline character to separate the data
    f.write('\n')
    
    f.write("The value of Isotropic Poisson ratio (mu) is = {}\n".format(mu))
    
    # write a newline character to separate the data
    f.write('\n')
    
        
    f.write("The value of Young’s modulus E is = {}\n".format(E))
    
    # write a newline character to separate the data
    f.write('\n')
    
    f.write('ALL DONE ^_^')
    
    
