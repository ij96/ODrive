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

#################### parameter configuration ###################################
for drive in ODriveSet:
    # M0
    drive.motor0.encoder.config.cpr = ENCODER_CPR
    drive.motor0.config.pole_pairs = 7
    drive.motor0.config.calibration_current = 20.0
    # M1
    drive.motor1.encoder.config.cpr = ENCODER_CPR
    drive.motor1.config.pole_pairs = 7
    drive.motor1.config.calibration_current = 20.0

#################### PID tuning ################################################
for drive in ODriveSet:
    # M0
    drive.motor0.config.pos_gain = 5.0             # [(counts/s) / counts]
    drive.motor0.config.vel_gain = 3.0 / 10000.0   # [A/(counts/s)]
    drive.motor0.config.vel_integrator_gain = 10.0 / 10000.0
    # M1
    drive.motor1.config.pos_gain = 20.0            # [(counts/s) / counts]
    drive.motor1.config.vel_gain = 5.0 / 10000.0   # [A/(counts/s)]
    drive.motor1.config.vel_integrator_gain = 10.0 / 10000.0

#################### assign ODrives #########################################
for drive in ODriveSet:
    if drive.serial_number == 53232789697077:
        ankle_drive     = drive
    if drive.serial_number == 61977222983735:
        right_hip_drive = drive
    if drive.serial_number == 61977223245879:
        left_hip_drive  = drive

#################### read-in trajectory from file ##############################
right_hip_pitch_position   = []
right_hip_slide_position   = []
right_ankle_pitch_position = []
left_hip_pitch_position    = []
left_hip_slide_position    = []
left_ankle_pitch_position  = []

j = -1
filePath = './'

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

for drive in ODriveSet:
    drive.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
    drive.motor1.set_pos_setpoint(0.0, 0.0, 0.0)

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
    setpoint_right_anklePitch = 64000.0 * right_ankle_pitch_position[i*speed_multiplier+1]*3 # gear ratio: 1:16
    setpoint_left_anklePitch = -64000.0 * left_ankle_pitch_position[i*speed_multiplier+1]*3 # gear ratio: 1:16

############################### Sending commands to corresponding motors ###############################################
    left_hip_drive.motor1.set_pos_setpoint(setpoint_left_slide, 0.0, 0.0)
    left_hip_drive.motor0.set_pos_setpoint(setpoint_left_pitch, 0.0, 0.0)
    right_hip_drive.motor1.set_pos_setpoint(setpoint_right_slide, 0.0, 0.0)
    right_hip_drive.motor0.set_pos_setpoint(setpoint_right_pitch, 0.0, 0.0)
    ankle_drive.motor0.set_pos_setpoint(setpoint_left_anklePitch, 0.0, 0.0) 
    ankle_drive.motor1.set_pos_setpoint(setpoint_right_anklePitch, 0.0, 0.0)

    #print("{}\t{:.5f}\t{:.5f}".format(i,setpoint_left_slide,setpoint_left_pitch))
    i = i + 1

    time.sleep(0.001)
