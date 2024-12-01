"""
Course Number: ENGR 13300
Semester: e.g. Fall 2024

Description:
    Project asks the user for engine information such as bore width, stroke length, piston type, desired comrpession ratio and cylinder amount. 
    The program then takes this and returns a calculated milliliter value for injectors at a certain RPM and engine load. This will be color coded based on magnitude. 
    Then, a graph representing a simulation dynamometer with torque is returned as well.
Assignment Information:
    Assignment:     Individual Project
    Team ID:        020 - 02 (e.g. LC1 - 01; for section LC1, team 01)
    Author:         Hayden Supple, hsupple@purdue.edu
    Date:           12/04/24

Contributors:
    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

from DynamometerSim import enginemapsim
import math
import numpy as np
import xlsxwriter as excel
import random

def exsheet(gasinj):
    colors = ['#bdeb34','#d9fa05','#fafa05','#ffec1c','#ffca1c','#eda011', '#ed7f11', '#ed4c11', '#c94210', '#fc5603', '#a31212','#820c0c', '#7d0b02']
    thresholds = []
    min = 0
    max = 0
    compmax = 0 
    compmin = 100
    workbook = excel.Workbook("/Users/haydensupple/Downloads/GasInjValues.xlsx")
    worksheet = workbook.add_worksheet()
    for i in range(2,len(gasinj)):
        for j in range(1,len(gasinj[i])):
            if float(gasinj[i][j]) < compmin:
                min = float(gasinj[i][j])
                compmin = float(gasinj[i][j])
            elif float(gasinj[i][j]) > compmax:
                max = float(gasinj[i][j])
                compmax = float(gasinj[i][j])
    
    val = (max-min)/13
    thresholds.append(0)

    for i in range(1,14):
        thresholds.append(min+(i*val))

    for i in range(len(gasinj)):
        for j in range(len(gasinj[i])):
            value = gasinj[i][j]
            if i != 0 and i != 1 and j != 0: 
                color = None
                for o in range(1, 14): 
                    if thresholds[o-1] <= float(value) <= thresholds[o]:
                        color = colors[o-1]
                        break 
                if color: 
                    cf = workbook.add_format({'bg_color': color})
                    worksheet.write(i, j, value, cf)
                else: 
                    worksheet.write(i, j, value)
            else: 
                worksheet.write(i, j, value)
    workbook.close()

def ratio2gram(enginemap, gasinj, vol, cyl, max):
    vol = cyl*vol
    RPMS = [1000]
    RPMS.extend(range(1100, max+100, 100))
    
    line = []


    for i in range(2, len(enginemap)):
        pressure = int(enginemap[i][0])
        intvol = vol*(pressure/101.325)*0.8

        grams = intvol*1.225
        line = []
        for j in range(1, len(enginemap[i])):
            ratio = float(enginemap[i][j])
            gfuel = grams/ratio
            line = np.append(line, str(round(gfuel,4)))

        for num in line:
            gasinj[i] = np.append(gasinj[i], num)
    for i in range(1, len(gasinj)):
        gasinj[i] = gasinj[i][:len(gasinj[1])]

    with open("B:\\Downloads\\Gasinj.txt", "w") as writefile:
        for row in gasinj:
            writefile.write(','.join(map(str, row)) + '\n')

def main():


    heatingval = 46.7
    bore = 300
    stroke = 350
    piston = ""
    ph = 0
    cr = 0
    cyl = 0
    
    cylinders = [4,6,8,10,12]
    octane = [5,72,6,81,7,87,8,92,9,96,10,100,11,104,12,108,13,112,14,114,15,116]
    pstyles = ["flat", "flat-top with reliefs", "dish", "hemi"]
    print("**Warning: Values displayed in simulation follow optimal conditions of a 14.7:1 AFR with no consideration of airflow to engine. Assume optimal boost pressures and forced induction**")
    #bore = 92                                                 ## DELETE THIS LINE WHEN FINISHED
    while bore > 200 or bore < 60:
        bore = float(input("Enter Bore Width (mm): "))
        if bore > 200:
            print("Bore must be below 200 millimeters!")
        if bore < 60:
            print("Bore must be higher than 60 millimeters!")
    #stroke = 82.7                                                ## DELETE THIS LINE WHEN FINISHED
    while bore/stroke <= 0.5 or bore/stroke >= 1.5:
        stroke = float(input("Enter Stroke Length (mm): "))
        if bore/stroke <= 0.5:
            print("Warning: Stroke:Bore Ratio is too high oversquare!")
        if bore/stroke >= 1.5:
            print("Warning: Stroke:Bore Ratio is too low undersquare!")
    #piston = "flat-top with reliefs"                                       ## DELETE THIS LINE WHEN FINISHED
    while piston not in pstyles:
        piston = input("Enter Piston Type (flat, flat-top with reliefs, hemi): ").lower()

    vdiam = math.sqrt((6000*stroke*(bore**2))/(2286000))
    if piston == "flat":
        ph = 0
    elif piston == "flat-top with reliefs":
        ph = -0.25*((vdiam**2)*math.pi)*4

    elif piston == "hemi":
        ph = -0.25*vdiam
    vol = ((math.pi*((0.5*bore)**2)*stroke)-ph)*(10**(-6))
    #cr = (vol+cv)/cv                                            ## DELETE THIS LINE WHEN FINISHED
    while cr < 5 or cr > 15:
        cr = float(input(f"Enter Your Desired Compression Ratio (Format as X in X:1) "))

        if cr < 5:
            print("Warning: Compression Ratio too low for combustion!")
        if cr > 15:
            print("Warning: Compression Ratio too high! Engine will detonate!")

    print(f"**Engine will use {octane[octane.index(math.floor(cr))+1]} octane gasoline**\n**Engine has a Compression Ratio of {cr:.1f}:1**")
    #cyl = 8                                            ## DELETE THIS LINE WHEN FINISHED
    while cyl not in cylinders:
        cyl = int(input("Enter the amount of Cylinders: "))
    if cyl == 4:
        rpm = 8000
        print(f"**Maximum engine speed determined to be {rpm} RPM**")

    if cyl == 6:
        rpm = 6800
        print(f"**Maximum engine speed determined to be {rpm} RPM**")
    if cyl == 8:
        rpm = 6200
        print(f"**Maximum engine speed determined to be {rpm} RPM**")
    if cyl == 10:
        rpm = 8500
        print(f"**Maximum engine speed determined to be {rpm} RPM**")
    if cyl == 12:
        rpm = 10000
        print(f"**Maximum engine speed determined to be {rpm} RPM**")
    
    enginemap = []
    gasinj = []

    with open("/Users/haydensupple/Downloads/EngineMapping.txt", "r") as file:
        for line in file:
            line_values = line.strip().split(',')
            enginemap.append(line_values)

        for i in range(0, len(enginemap)-1):
            enginemap[i] = enginemap[i][:int(rpm/100)-8]
    with open("/Users/haydensupple/Downloads/GasINJ2.txt", "r") as gasfile:
        for line in gasfile:
            line_values = line.strip().split(',')
            gasinj.append(line_values)
    while int(gasinj[1][-1]) < rpm:
        gasinj[1].append(int(gasinj[1][-1])+100)

    ratio2gram(enginemap, gasinj, vol, cyl, int(gasinj[1][-1]))
    exsheet(gasinj)
    
    aat = 308
    print("**Simulation will Report Base Horsepower (Hp) and Torque (Ft-Lbs)**")
#########################################################################################
##Simulation Below##
    vol = vol*cyl*61.0237
    enginemapsim(vol, cr, gasinj)
    
if __name__ == "__main__":
    main()
