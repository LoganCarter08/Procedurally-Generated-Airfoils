import os
import numpy as np
import matplotlib.pyplot as plt

# read in the orignal foil and parse it into arrays
# increment across the arrays and move the y value up and down, 
    # write the .dat file and the input file
    # call xfoil
    
# format of name, lift, drag, angle
first = ["name", -1000, 0, 0]
second = ["name", -1000, 0, 0]
third = ["name", -1000, 0, 0]
fourth = ["name", -1000, 0, 0]
fifth = ["name", -1000, 0, 0]


for x in range(1, 10): #10           # first digit. Skip 0 because of weird rules
    for y in range(0, 10): #10      # second digit 
        for z in range(1, 41): #41  # third digit
            # need to create a folder if doesn't exist
            folder = str(x) + str(y) + "{:0>2d}".format(z);
            try:
                os.mkdir('foils/' + folder)
            except:
                print('broked foils/' + folder)
        
            # Create the airfoil .dat file
            #dat = open('foils/' + folder + '/foil.dat', "w")
            #for q in range(0, 51):
                #dat.write("")
        
            fid = open('foils/' + folder + '/input.txt',"w")
            fid.write("plop\n")
            fid.write("g\n")
            fid.write("\n")
            #fid.write("load foil.dat\n")
            fid.write("naca " + str(x) + str(y) + "{:0>2d}".format(z) + "\n")
            fid.write("ppar\n")
            fid.write("N\n")
            fid.write("100\n")
            fid.write("\n")
            fid.write("\n")
            fid.write("PSAV " + "foils/" + folder + "/foil.dat\n")
            fid.write("OPER\n")
            fid.write("vpar\n")
            fid.write("n\n")
            fid.write("9\n\n") # set to 9 for wind tunnel. Lower would be more realistic
            fid.write("ITER 50\n") # this value is... odd. 
            fid.write("visc 452361\n") # 9.5" chord at 65mph
            fid.write("seqp\n")
            fid.write("pacc\n")
            fid.write("foils/" + folder + "/analysis.txt\n")
            fid.write("\n")
            fid.write("aseq -25 25 0.5\n")
            fid.write("\n\n\n")
            fid.write("quit\n")
            fid.close() 
            # Run the XFoil calling command
            os.system("xfoil.exe < foils/" + folder + "/input.txt")
            
            # need to read the file and rank it
            file1 = open("foils/" + folder + "/analysis.txt", 'r')
            Lines = file1.readlines()
             
            # angle, lift, drag
            best = [0, -1000, 0]
            start = False
            # get the best for this foil
            for line in Lines:
                vals = line.split()
                if len(vals) > 0:
                    if start:
                        if float(vals[1]) > best[1]:
                            best[1] = float(vals[1])
                            best[0] = float(vals[0])
                            best[2] = float(vals[2])
                if "-----" in line:
                    start = True 
            file1.close()

            # ugly things follow
            if best[1] > first[1]:
                fifth = fourth
                fourth = third
                third = second 
                second = first
                first = [folder, best[1], best[2], best[0]]
            elif best[1] > second[1]:
                fifth = fourth
                fourth = third
                third = second 
                second = [folder, best[1], best[2], best[0]]
            elif best[1] > third[1]:
                fifth = fourth
                fourth = third
                third = [folder, best[1], best[2], best[0]]
            elif best[1] > fourth[1]:
                fifth = fourth
                fourth = [folder, best[1], best[2], best[0]]
            elif best[1] > fifth[1]:
                fifth = [folder, best[1], best[2], best[0]]
                
print("name\tlift\t\tdrag\t\tangle")
print(str(first[0]) + "\t" + str(first[1]) + "\t\t" + str(first[2]) + "\t\t\t" + str(first[3]))
print(str(second[0]) + "\t" + str(second[1]) + "\t\t" + str(second[2]) + "\t\t\t" + str(second[3]))
print(str(third[0]) + "\t" + str(third[1]) + "\t\t" + str(third[2]) + "\t\t\t" + str(third[3]))
print(str(fourth[0]) + "\t" + str(fourth[1]) + "\t\t" + str(fourth[2]) + "\t\t\t" + str(fourth[3]))
print(str(fifth[0]) + "\t" + str(fifth[1]) + "\t\t" + str(fifth[2]) + "\t\t\t" + str(fifth[3]))
                
                    