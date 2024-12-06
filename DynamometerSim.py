"""
Course Number: ENGR 13300
Semester: e.g. Fall 2024

Description:
    Simulation of a dynamometer using a function of Cubic Spline, which takes plotted data and converts it to a single line. 
    This data is then interpreted to calculate a torque for the engine and then graphed the same way.
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

""" Write any import statements here (and delete this line)."""

def enginemapsim(displacement, CR, enginemap):
    #Import all functions
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.interpolate import CubicSpline
    import random

    # Initialize variables
    topTorque = 0
    topInj = 0
    topHP = (displacement/10)*CR*1.1
    topRPM = 0
    RM = 0
    # Find topInjection value   
    for val in enginemap[11]:
        try:
            inj = float(val)
            if inj < 10 and inj > topInj:
                topInj = inj
                topRPM = RM
        except ValueError:
            continue
        RM += 1
    scale = topHP/topInj

    # Prepare figure and axis
    fig, ax1 = plt.subplots()

    # Generate Xvals and Yvals with two extra to end function
    Xvals = np.array([float(x) for x in enginemap[1][1:]])
    Xvals = np.append(Xvals, Xvals[-1]+100)
    Xvals = np.append(Xvals, Xvals[-1]+100)
    #Append all Ys to Yvals with scale
    Yvals = np.array([float(y)*scale for y in enginemap[11][1:len(Xvals)-1]])
    #Add realism scaling to program
    for i in range(0, len(Xvals)-2):
        Yvals[i] = Yvals[i]*(0.5+0.009803*i)
    #Append half the end value and 0 for realism
    Yvals = np.append(Yvals, Yvals[-1]/2)
    Yvals = np.append(Yvals, 0)

    addition = 0
    #Iterate throughout Yvals to add realism scaling
    for i in range(0, len(Yvals)):
        addition += random.randint(-2, 2)
        Yvals[i] = Yvals[i] + addition

    torques = []
    #CubicSpline to calculate a line
    spline = CubicSpline(Xvals, Yvals)
    #Linespace to calculate X Line
    Xinterp = np.linspace(min(Xvals), max(Xvals), 1000)
    Yinterp = spline(Xinterp)
    differential = 0.2
    n = 0
    for num in range(0, len(Xvals)-1):
        try:
            #Iterate throughout num in range of Xvals to find Torque values
            torque = (spline(float(Xvals[num]))*525.2)/float(Xvals[num])*differential
            #Append to torques
            torques = np.append(torques, torque)
            if torque > topTorque:
                topTorque = torque
                gRPM = Xvals[num]
            if n<14:            
                differential += 0.96**(n+1)
            n += 1
        except ValueError:
            continue
    
    torques = np.append(torques, 0)
    #Output legends
    maxt = f"Max Torque={round(topTorque,2)}(lb•ft)@{gRPM}(RPM)"
    maxh = f"Max Power={round(topHP, 2)}(HP)@{enginemap[1][topRPM]}(RPM)"
    ax1.plot(Xinterp, Yinterp, 'r-', label=maxh)
    ax1.set_xlabel('Engine RPMs')
    ax1.set_ylabel('Horsepower')
    ax1.tick_params(axis='y')

    #Format Labels
    ax2 = ax1.twinx()
    ax2.plot(Xvals, torques, '--', label=maxt, color='#eb4d8f')
    ax2.set_ylabel('Torques (ft•lb)')
    ax2.tick_params(axis='y')

    handles, labels = ax1.get_legend_handles_labels()  
    handles2, labels2 = ax2.get_legend_handles_labels() 
    ax1.legend(handles + handles2, labels + labels2, loc='upper left')

    #Title Plot
    plt.title('Simulated Dynamometer')

    plt.show()
