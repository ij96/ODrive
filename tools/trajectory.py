#!/usr/bin/env python3

from __future__ import print_function

import odrive.core
import time
import math
from openpyxl import load_workbook
from openpyxl import Workbook
import csv

#################### adjustable parameters #####################################
trajectory_file_path = './traj_test.csv' # trajectory CSV file
speed_multiplier = 8                     # speed multiplier, for faster movement

print("\nRunning trajectory from {}".format(trajectory_file_path))
print("Trajectory speed multiplier: {}".format(speed_multiplier))

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

traj_size = -1

with open(trajectory_file_path) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if traj_size > -1:
            right_hip_pitch_position.append(float(row[0]))
            right_hip_slide_position.append(float(row[1]))
            right_ankle_pitch_position.append(float(row[2]))
            left_hip_pitch_position.append(float(row[3]))
            left_hip_slide_position.append(float(row[4]))
            left_ankle_pitch_position.append(float(row[5]))
        traj_size = traj_size + 1

print("\nTrajectory size: {}".format(traj_size))

#################### zero position #############################################
print("\nReturning to zero position...")

for drive in ODriveSet:
    drive.motor0.set_pos_setpoint(0.0, 0.0, 0.0)
    drive.motor1.set_pos_setpoint(0.0, 0.0, 0.0)

#################### begin trajectory ##########################################
print("\nRunning trajectory... (press Ctrl+C to stop)")

i = 0   # counter

i_max = int(traj_size / speed_multiplier) - 1 # max value of i, calculated based
                                              #   traj size and speed multiplier

while True:
    if i > i_max:
        i = 0

    setpoint_index = i * speed_multiplier + 1

    setpoint_left_pitch       = 30558.0 *   left_hip_pitch_position[setpoint_index] # gear ratio: 1:24, 1/3.1415*24*4000
    setpoint_left_slide       = -400000.0 * left_hip_slide_position[setpoint_index] # gear ratio: 1:4, 4*4000*4, problem with encoder
    setpoint_right_pitch      = -30558.0 *  right_hip_pitch_position[setpoint_index] # gear ratio: 1:24, 1/3.1415*24*4000
    setpoint_right_slide      = 400000.0 *  right_hip_slide_position[setpoint_index] # gear ratio: 1:4, 4*4000*4, problem with encoder
    setpoint_right_anklePitch = 64000.0  *  right_ankle_pitch_position[setpoint_index] * 3 # gear ratio: 1:16
    setpoint_left_anklePitch  = -64000.0 *  left_ankle_pitch_position[setpoint_index]  * 3 # gear ratio: 1:16

    ################ sending commands to corresponding motors ##################
    left_hip_drive.motor1.set_pos_setpoint(setpoint_left_slide, 0.0, 0.0)
    left_hip_drive.motor0.set_pos_setpoint(setpoint_left_pitch, 0.0, 0.0)
    right_hip_drive.motor1.set_pos_setpoint(setpoint_right_slide, 0.0, 0.0)
    right_hip_drive.motor0.set_pos_setpoint(setpoint_right_pitch, 0.0, 0.0)
    ankle_drive.motor0.set_pos_setpoint(setpoint_left_anklePitch, 0.0, 0.0) 
    ankle_drive.motor1.set_pos_setpoint(setpoint_right_anklePitch, 0.0, 0.0)

    i = i + 1

    time.sleep(0.001)
