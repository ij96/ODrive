#!/usr/bin/env python3

from __future__ import print_function

import odrive.core
import time
import math
from openpyxl import load_workbook
from openpyxl import Workbook
import csv

#################### ODrive discovery ##########################################
print("Finding ODrives...")

ODriveSet = []

for drive in odrive.core.find_all(consider_usb=True, consider_serial=False):
    print("ODrive found, serial number: {}".format(drive.serial_number))
    ODriveSet.append(drive)

if len(ODriveSet) == 0:
    print("No ODrives found!")
    exit()
else:
    print("Found {} ODrives\n".format(len(ODriveSet)))
    my_drive = ODriveSet[1]

#################### read-in trajectory from file ##############################

right_hip_pitch_position   = []
right_hip_slide_position   = []
right_ankle_pitch_position = []
left_hip_pitch_position    = []
left_hip_slide_position    = []
left_ankle_pitch_position  = []

j = -1
filePath = '***REMOVED***'

with open(filePath + 'traj_test.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	for row in readCSV:
		if j > -1:
			right_hip_pitch_position.append(float(row[0]))
			right_hip_slide_position.append(float(row[1]))
			right_ankle_pitch_position.append(float(row[2]))
			left_hip_pitch_position.append(float(row[3]))
			left_hip_slide_position.append(float(row[4]))
			left_ankle_pitch_position.append(float(row[5]))
		j = j + 1

print("Trajectory size: {}\n".format(j))

#################### zero position #############################################

print("Returning to zero position...\n")
# my_drive.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
# my_drive.motor1.set_pos_setpoint(0.0, 0.0, 0.0)

ODriveSet[0].motor0.set_pos_setpoint(0.0, 0.0, 0.0)
ODriveSet[0].motor1.set_pos_setpoint(0.0, 0.0, 0.0)
ODriveSet[1].motor0.set_pos_setpoint(0.0, 0.0, 0.0)
ODriveSet[1].motor1.set_pos_setpoint(0.0, 0.0, 0.0)

#################### begin trajectory ##########################################

print("Running trajectory... (press Ctrl+C to stop)")

i = 0   # counter

# speed multiplier, for faster movement
speed_multiplier = 8                  # speed multiplier
i_max = int(j / speed_multiplier) - 1 # max value of i, calculated based on j
                                      #   and speed multiplier
print("Speed multiplier: {}".format(speed_multiplier))

while True:
    if i > i_max:
        i = 0
        # ODriveSet[0].motor0.set_pos_setpoint(0.0, 0.0, 0.0)
        # ODriveSet[0].motor1.set_pos_setpoint(0.0, 0.0, 0.0)
        # ODriveSet[1].motor0.set_pos_setpoint(0.0, 0.0, 0.0)
        # ODriveSet[1].motor1.set_pos_setpoint(0.0, 0.0, 0.0)

    setpoint_left_pitch = 30558.0 * left_hip_pitch_position[i*speed_multiplier+1] # gear ratio: 1:24, 1/3.1415*24*4000
    setpoint_left_slide = -400000.0 * left_hip_slide_position[i*speed_multiplier+1] # gear ratio: 1:4, 4*4000*4, problem with encoder
    setpoint_right_pitch = -30558.0 * right_hip_pitch_position[i*speed_multiplier+1] # gear ratio: 1:24, 1/3.1415*24*4000
    setpoint_right_slide = 400000.0 * right_hip_slide_position[i*speed_multiplier+1] # gear ratio: 1:4, 4*4000*4, problem with encoder
    # setpoint_right_anklePitch = 64000.0 * right_ankle_pitch_position[i+1]

    # my_drive.motor1.set_pos_setpoint(setpoint_left_slide, 0.0, 0.0)
    # my_drive.motor0.set_pos_setpoint(setpoint_left_pitch, 0.0, 0.0)

    ODriveSet[0].motor1.set_pos_setpoint(setpoint_left_slide, 0.0, 0.0)
    ODriveSet[0].motor0.set_pos_setpoint(setpoint_left_pitch, 0.0, 0.0)
    ODriveSet[1].motor1.set_pos_setpoint(setpoint_right_slide, 0.0, 0.0)
    ODriveSet[1].motor0.set_pos_setpoint(setpoint_right_pitch, 0.0, 0.0)

    #print("{}\t{:.5f}\t{:.5f}".format(i,setpoint_left_slide,setpoint_left_pitch))
    i = i + 1

    time.sleep(0.001)
