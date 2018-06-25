#!/usr/bin/env python3

# Trajectory

from __future__ import print_function

import odrive.core
import time
import math


#################### adjustable parameters #####################################
# trajectory_file_path = 'traj_test.csv' # trajectory CSV file
speed_multiplier = 4                     # speed multiplier, for faster movement
amplitude_multiplier=2                   # amplitude multiplier for faster movement
# print("\nRunning trajectory from {}".format(trajectory_file_path))
print("Trajectory speed multiplier: {}".format(speed_multiplier))
print("Trajectory amplifier multiplier: {}".format(amplitude_multiplier))

#################### ODrive discovery ##########################################
print("\nFinding ODrives...")

ODriveSet = []

for drive in odrive.core.find_all(consider_usb=True, consider_serial=False):
    print("ODrive found, serial number: {}".format(drive.serial_number))
    ODriveSet.append(drive)

if len(ODriveSet) == 0:
    print("No ODrives found!")
    exit()
else:
    print("Found {} ODrives".format(len(ODriveSet)))

#################### PID tuning ################################################
for drive in ODriveSet:
    # M0
    drive.motor0.config.pos_gain = 5.0             # [(counts/s) / counts]
    drive.motor0.config.vel_gain = 3.0 / 10000.0   # [A/(counts/s)]
    drive.motor0.config.vel_integrator_gain = 10.0 / 10000.0
    # M1
    drive.motor1.config.pos_gain = 5.0            # [(counts/s) / counts]
    drive.motor1.config.vel_gain = 3.0 / 10000.0   # [A/(counts/s)]
    drive.motor1.config.vel_integrator_gain = 10.0 / 10000.0

#################### assign ODrives ############################################
for drive in ODriveSet:
    if drive.serial_number == ###:
        ODrive1=drive
    if drive.serial_number == ##:
        ODrive2=drive
    else:
        print("Serial Number: "+str(drive.serial_number)+"\n")

################################### ODrive1 Setup   ###########################
# To read a value, simply read the property
print("Bus voltage is " + str(ODrive1.vbus_voltage) + "V")
print("Bus voltage is " + str(ODrive2.vbus_voltage) + "V")

# Or to change a value, just assign to the property
ODrive1.motor1.pos_setpoint = 3.14
ODrive1.motor0.pos_setpoint = 3.14
ODrive2.motor1.pos_setpoint = 3.14
ODrive2.motor0.pos_setpoint = 3.14

print("Position setpoint is " + str(ODrive1.motor0.pos_setpoint))
print("Position setpoint is " + str(ODrive2.motor0.pos_setpoint))


# And this is how function calls are done:
ODrive1.motor1.set_pos_setpoint(0.0, 0.0, 0.0)
ODrive1.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
ODrive2.motor1.set_pos_setpoint(0.0, 0.0, 0.0)
ODrive2.motor0.set_pos_setpoint(0.0, 0.0, 0.0)

# A little sine wave to test
t0 = time.monotonic()
while True:
    setpoint = 4000.0 * math.sin((time.monotonic() - t0)*2) * amplitude_multiplier
    print("goto " + str(int(setpoint)))
    ODrive1.motor1.set_pos_setpoint(setpoint, 0.0, 0.0)
    ODrive1.motor0.set_pos_setpoint(setpoint, 0.0, 0.0)

    ODrive2.motor1.set_pos_setpoint(setpoint, 0.0, 0.0)
    ODrive2.motor0.set_pos_setpoint(setpoint, 0.0, 0.0)

    time.sleep(0.01/speed_multiplier)

# Write to a read-only property:
ODrive1.vbus_voltage = 11.0  # fails with `AttributeError: can't set attribute`
ODrive2.vbus_voltage = 11.0  # fails with `AttributeError: can't set attribute`
