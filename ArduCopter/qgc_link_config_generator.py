#!/usr/bin/env python
'''waypoint command handling'''

import multiprocessing
import subprocess
import sys
import os
import time

try :
    instances = 0
    if len(sys.argv) == 2:
        instances = sys.argv[1]
    else:
	    print("usage: %s <number of vehicles>" % sys.argv[0])
	    quit()

    lines = []
    startPort = 14560
    for x in range(int(instances)):
        lines.append("Link%d\\auto=true\n" %x)
        lines.append("Link%d\high_latency = false\n" % x)
        lines.append("Link%d\hostCount = 0\n" % x)
        lines.append("Link%d\\name = udp on %d\n" % (x,startPort) )
        lines.append("Link%d\port = %d\n" % (x,startPort))
        lines.append("Link%d\\type = 1\n" % x)
        startPort += 10
    
      
    qgcconfig = "./qgc_link_config.txt"
    open(qgcconfig, 'w').writelines(lines)

except KeyboardInterrupt:
    quit()


