import os
from math import *
import time

import matplotlib.pyplot as plt

# Input Variables
vel_i = float(0) # Initial Speed
ang_i = float(0) # Initial angle
CofDrag = float(0) # CD
AirDen = float(0) # Air Density
acc_g = float(0) # Acc of G
proj_mass = float(0) # mass of projectile
ref_area = float(0) # reference area
Input_Pos_y = float(0) # Initial height

# Internal Variables 
del_t = float(.001) # Time step
Vel_x = float(0) # vel x in m/s
Vel_y = float(0) # vel y in m/s
Pos_x = float(0) # position x in meters
Pos_y = float(0) # position y in meters
g_time = float(0) # time (s)
Wind = float(0) # wind
mode = 0 #operation mode
output = "hi"
xval = []
yval = []

#open output file
out = open('data.txt','w')

def get_input():
	print "Input initial values"
	global vel_i
	global ang_i
	global CofDrag
	global AirDen
	global proj_mass
	global acc_g
	global ref_area
	global mode
	global Input_Pos_y
	global Wind
	mode = raw_input("Operation mode (0 max range; 1 single value)[1]: ") # Get operation mode
	if not mode:
		mode = 1
	Input_Pos_y = raw_input("Initial height feet (0 for ground): ") # Set initial height
	Wind = raw_input("Tail wind speed (ft/s) [0]: ")
	if not Wind:
		Wind = 0
	vel_i = float(raw_input("Launch Velocity (ft/s): ")) # Get initial velocity  
	ang_i = float(raw_input("Launch Angle: ")) # Get initial angle
	CofDrag = float(raw_input("Enter the CD: ")) # Get CD
	proj_mass = float(raw_input("Projectile Mass (grams): ")) # Get projectile mass
	AirDen = raw_input("Air Density [1.225(kg/m3)]: ") # Get and suggest a value for the Density of Air
	if not AirDen:
		AirDen = 1.225
	acc_g = raw_input("Acceleration of G [9.8066(m/s)]: ") # Get and suggest a value for the acc of G
	if not acc_g:
		acc_g = 9.8066
	ref_area = raw_input("Reference area in^2 [3.659(in^2)]: ") # Get and suggest a value for the acc of G
	if not ref_area:
		ref_area = 3.659569
	print "Done getting initial values"

def phrase_input():
	global vel_i
	global Vel_x
	global Vel_y
	global Pos_y
	global ang_i
	global ref_area
	global proj_mass
	global AirDen
	global acc_g
	global ref_area
	global Input_Pos_y
	global Wind
	vel_i = (float(vel_i)*.3048) # Convert (ft/s) to (m/s)
	ang_i = radians(float(ang_i))
	Vel_x = (cos(ang_i)*vel_i)
	Vel_y = (sin(ang_i)*vel_i)
	ref_area = 0.00064516*float(ref_area)
	proj_mass = float(proj_mass)*0.001
	Pos_y = float(Input_Pos_y)*0.3048
	Wind = float(Wind)*0.3048
	#convert to floats
	AirDen = float(AirDen)
	acc_g = float(acc_g)
	ref_area = float(ref_area)


def step_sim():
	global vel_i
	global ang_i
	global CofDrag
	global AirDen
	global proj_mass
	global acc_g
	global Vel_x
	global Vel_y
	global Pos_x
	global Pos_y
	global del_t
	global ref_area
	global g_time
	global output
	#print "ref arrea ", ref_area
	#print "CD ",CofDrag
	#print "air den ", AirDen
	g_time = g_time + del_t # Increment Time
	
	loc_ang = atan(abs(Vel_y)/Vel_x) # calculate current angle
	
	loc_vel = sqrt( pow(Vel_y, 2)+pow( Vel_x, 2) ) # calculate current total vel
	#						Drag Equation 							f=md
	loc_a = (.5 * AirDen * pow(loc_vel, 2) * CofDrag * ref_area) / proj_mass
	
	loc_a_x = (cos(loc_ang)*loc_a)
	loc_a_y = (sin(loc_ang)*loc_a)
	
	#if vel_y was negative it shall be again
	if Vel_y < 0:
		Vel_y = Vel_y- ( (acc_g-loc_a_y) * del_t) # Apply G  and locF to y vel
	else:
		Vel_y = Vel_y+ ( ((acc_g+loc_a_y)*(-1)) * del_t)   *(1) # Apply G  and locF to y vel
	
	Vel_x = Vel_x+( (loc_a_x*(-1)) * del_t ) # Apply locF to x vel
	
	Pos_x = Pos_x+(float(Vel_x)*float(del_t))+Wind*del_t # calculate x pos based on last vel
	Pos_y = Pos_y+(float(Vel_y)*float(del_t)) # calculate y pos based on last vel
	output = g_time ,'|',loc_ang ,'|',loc_vel ,'|',loc_a ,'|',loc_a_x ,'|',loc_a_y ,'|',Vel_x ,'|',Vel_y ,'|',Pos_x ,'|',Pos_y
	output = str(output).replace(", '|', ", "|").replace("(","").replace(")","")
	#Write all data to file!
	
	
def print_results():
	global g_time
	global Pos_x
	print "all done!"
	print "time", g_time, "seconds"
	print "pos x",'{0:,.2f}'.format(Pos_x), "meters or",'{0:,.2f}'.format(Pos_x*3.280839),"feet"

def reset(ang):
	global Pos_x
	global Pos_y
	global g_time
	global ang_i
	global Vel_x
	global Vel_y
	Pos_y = float(0)
	Pos_x = float(0)
	g_time = float(0)
	ang_i = radians(float(ang))
	Vel_x = (cos(ang_i)*vel_i)
	Vel_y = (sin(ang_i)*vel_i)

def cleanup():
	out.close()


get_input()
phrase_input()
step_sim() # run first iteration
if int(mode) == 0:
	out.write("global time (s) | loc_ang (radians) | loc_vel (m/s) | loc_a (m/s/s) | loc_a_x (m/s/s) | loc_a_y (m/s/s) | Vel_x (m/s) | Vel_y (m/s) | Pos_x (m) | Pos_y (m)\n")
	ang = 0
	rainge = []
	
	#run fro every angle
	while ang < 89:
		ang = ang + 1
		print "ang:", ang
		reset(ang)
		step_sim()
		while Pos_y > 0:
			step_sim()
		rainge.append(Pos_x)
		print "range:", Pos_x, "meters"
	print "max range is", max(rainge), "at", rainge.index(max(rainge))+1, "degrees"
	reset((rainge.index(max(rainge))+1))
	
	print " "
	#run again for data
	step_sim()
	while Pos_y > 0:
		step_sim()
		out.write(output)
		out.write("\n")
		xval.append(Pos_x)
		yval.append(Pos_y)
	print_results()
elif int(mode) == 1:
	out.write("global time (s) | loc_ang (radians) | loc_vel (m/s) | loc_a (m/s/s) | loc_a_x (m/s/s) | loc_a_y (m/s/s) | Vel_x (m/s) | Vel_y (m/s) | Pos_x (m) | Pos_y (m)\n")
	while Pos_y > 0:
		step_sim()
		out.write(output)
		out.write("\n")
		xval.append(Pos_x)
		yval.append(Pos_y)
	print_results()
else:
	print "Invalid Mode"
	exit()
# plot the data

plt.plot(xval, yval, '-', linewidth=2)
# plt.plot(, yval, '-', linewidth=2)
plt.xlim([0,Pos_x])
plt.ylim([0,(max(yval)*1.1)])
plt.xlabel('x pos (m)')
plt.ylabel('y pos (m)')
plt.suptitle('Projecile Position Graph', fontsize=14, fontweight='bold')
plt.savefig('data.png')
plt.show()
cleanup()


#print output
