#!/usr/bin/env python
'''waypoint command handling'''

# from pymavlink import mavutil, mavwp
# from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util


import multiprocessing
import subprocess
import sys
import os
import time
import math

class Config :
        basePositionLat = 28.536667
        basePositionLon = 77.319065
        basePositionAlt = 17
        basePositionHdg = 0
        instances = 10
        launchDelay = 10
        interVehicleDistance = 10

def worker(num):
    instanceFolder = "./sitl%d" % num
    if not os.path.exists(instanceFolder):
        os.makedirs(instanceFolder)
    os.chdir(instanceFolder)
    
    row = math.floor((num-1)/4)
    col = ((num-1) % 4)
    
    print("vehicle at %d,%d\n" % (row,col))
    
    newLat,newLon = mp_util.gps_offset(Config.basePositionLat, Config.basePositionLon,
                                       Config.interVehicleDistance*(col),-(row)*Config.interVehicleDistance)
    vehicleCmd = "sim_vehicle.py -I%d -l%f,%f,%d,%d" % (num,newLat,newLon,
                                                        Config.basePositionAlt,Config.basePositionHdg)
    print(vehicleCmd)

    defaultParam = "/home/avinash/copter/ardupilot/Tools/autotest/default_params/copter.parm"
    lines = open(defaultParam, 'r').readlines()
    new_last_line = "SYSID_THISMAV %f\n" % num
    lines[-1] = new_last_line
    # print lines
    open(defaultParam, 'w').writelines(lines)

    subprocess.check_call(vehicleCmd, shell=True)

try :
    if len(sys.argv) == 4:
        Config.instances = int(sys.argv[1])
        Config.interVehicleDistance = int(sys.argv[2])
        Config.launchDelay = int(sys.argv[3])
    else:
	    print("usage: %s <number of vehicles> <distance between vehicles> <launch_delay>" % sys.argv[0])
	    quit()

    jobs = []
    for x in range(Config.instances):
        p = multiprocessing.Process(target=worker, args=(x+1,))
        jobs.append(p)
        time.sleep(Config.launchDelay)
        p.start()
        
    for job in jobs:
        job.join()

except KeyboardInterrupt:
    for job in jobs:
        job.terminate()
    quit()


