#!/usr/bin/env python3

# for finding motor & encoder config during manual calibration

# from __future__ import print_function

# import odrive.core

# my_odrive = odrive.core.find_any(consider_usb=True, consider_serial=False)

# print("ODrive serial number: {}".format(my_odrive.serial_number))
# print()
# print("Copy and paste the following into Firmware/MotorControl/low_level.c")
# print()
# print("#define M0_ENCODER_OFFSET       {}".format(my_odrive.motor0.encoder.encoder_offset))
# print("#define M0_ENCODER_MOTOR_DIR    {}".format(my_odrive.motor0.encoder.motor_dir))
# print("#define M0_PHASE_INDUCTANCE     {}".format(my_odrive.motor0.config.phase_inductance))
# print("#define M0_PHASE_RESISTANCE     {}".format(my_odrive.motor0.config.phase_resistance))
# print()
# print("#define M1_ENCODER_OFFSET       {}".format(my_odrive.motor1.encoder.encoder_offset))
# print("#define M1_ENCODER_MOTOR_DIR    {}".format(my_odrive.motor1.encoder.motor_dir))
# print("#define M1_PHASE_INDUCTANCE     {}".format(my_odrive.motor1.config.phase_inductance))
# print("#define M1_PHASE_RESISTANCE     {}".format(my_odrive.motor1.config.phase_resistance))




#!/usr/bin/env python3

# Trajectory

from __future__ import print_function

import odrive.core
import time
import math
from openpyxl import load_workbook
from openpyxl import Workbook
import csv

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
for my_odrive in ODriveSet:
    if my_odrive.serial_number == 53232789697077:
        hiproll_my_odrive      = my_odrive
        print("Found hip roll, M0: {}, M1: {}".format(my_odrive.motor0.error, my_odrive.motor1.error))
    if my_odrive.serial_number == 61977222983735:
        right_hip_my_odrive    = my_odrive
        print("Found left leg, M0: {}, M1: {}".format(my_odrive.motor0.error, my_odrive.motor1.error))
    if my_odrive.serial_number == 61977223245879:
        left_hip_my_odrive     = my_odrive
        print("Found right leg, M0: {}, M1: {}".format(my_odrive.motor0.error, my_odrive.motor1.error))
    if my_odrive.serial_number == 61908504096823:
        ankle_my_odrive        = my_odrive
        print("Found ankle pitch, M0: {}, M1: {}".format(my_odrive.motor0.error, my_odrive.motor1.error))
    print("ODrive serial number: {}".format(my_odrive.serial_number))
    print()
    print("Copy and paste the following into Firmware/MotorControl/low_level.c")
    print()
    print("#define M0_ENCODER_OFFSET       {}".format(my_odrive.motor0.encoder.encoder_offset))
    print("#define M0_ENCODER_MOTOR_DIR    {}".format(my_odrive.motor0.encoder.motor_dir))
    print("#define M0_PHASE_INDUCTANCE     {}".format(my_odrive.motor0.config.phase_inductance))
    print("#define M0_PHASE_RESISTANCE     {}".format(my_odrive.motor0.config.phase_resistance))
    print()
    print("#define M1_ENCODER_OFFSET       {}".format(my_odrive.motor1.encoder.encoder_offset))
    print("#define M1_ENCODER_MOTOR_DIR    {}".format(my_odrive.motor1.encoder.motor_dir))
    print("#define M1_PHASE_INDUCTANCE     {}".format(my_odrive.motor1.config.phase_inductance))
    print("#define M1_PHASE_RESISTANCE     {}".format(my_odrive.motor1.config.phase_resistance))
