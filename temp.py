"""
Read the CPU temperature
"""

from subprocess import Popen, PIPE

temp_cmd = Popen("/opt/vc/bin/vcgencmd measure_temp", shell=True, stdout=PIPE)
temp = temp_cmd.stdout.readlines()[0].decode().split("=")[1][0:-3]
print(temp)