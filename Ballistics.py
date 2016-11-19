from Projectile import BallisticObject
import math


def get_input():
	print "Input initial values"
	ret = dict()
	# Get operation mode
	ret["mode"] = raw_input("Operation mode (0 max range; 1 single value)[1]: ")
	if not ret["mode"]:
		ret["mode"] = 1
	# Set initial height
	ret["Pos_y"] = float(raw_input("Initial height feet (0 for ground): ")) * 0.3048
	# Get initial velocity in m/s
	ret["vel_i"] = float(raw_input("Launch Velocity (ft/s): ")) * .3048
	# Get initial angle
	ret["ang_i"] = math.radians(float(raw_input("Launch Angle: ")))
	# Get CD
	ret["Cd"] = float(raw_input("Enter the CD: "))
	# Get projectile mass
	ret["mass"] = float(raw_input("Projectile Mass (grams): "))*0.001
	# Get and suggest a value for the Density of Air
	ret["AirDen"] = raw_input("Air Density [1.225(kg/m3)]: ")
	if not ret["AirDen"]:
		ret["AirDen"] = 1.225
	# Get and suggest a value for the acc of G
	ret["acc_g"] = raw_input("Acceleration of G [9.8066(m/s/s)]: ")
	if not ret["acc_g"]:
		ret["acc_g"] = 9.8066
	# Get and suggest a value for the acc of G
	ret["ref_area"] = raw_input("Reference area in^2 [3.659(in^2)]: ")
	if not ret["ref_area"]:
		ret["ref_area"] = 0.00064516 * 3.659569
	else:
		ret["ref_area"] = 0.00064516 * float(ret["ref_area"])
	print "Done getting initial values"

	return ret

if __name__ == "__main__":
	input = get_input()
	proj1 = BallisticObject(posY=input["Pos_y"], velI=input["vel_i"], angI=input["ang_i"], Cd=input["Cd"],
							projMass=input["mass"], airDen=input["AirDen"], accG=input["acc_g"],
							refArea=input["ref_area"])

	if int(input["mode"]) == 0:
		ang = 0
		proj1.set_angle(ang)
		range = []

		#run fro every angle
		while ang < 89:
			ang = ang + 1
			print "ang:", ang
			proj1.set_angle(math.radians(ang))
			res = proj1.run_sim()
			range.append(max(zip(*res)[0]))
			print "range:", max(zip(*res)[0]), "meters"
		print "max range is", max(range), "at", range.index(max(range)) + 1, "degrees"
		proj1.set_angle(math.radians(range.index(max(range)) + 1))

	elif int(input["mode"]) == 1:
		pass
	else:
		print "Invalid Mode"
		exit()
	# plot the data
	proj1.run_and_dispaly()
