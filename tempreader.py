import os
import glob
import time


class tempreader:
	def __init__(self):
		os.system('modprobe w1-gpio')
		os.system('modprobe w1-therm')
		self.stopbit = 0
		self.base_dir = '/sys/bus/w1/devices/'
		self.device_folder = glob.glob(self.base_dir + '28*')
		if len(self.device_folder) == 0:
			self.device_folder = ""
		else:
			self.device_folder = self.device_folder[0]
		self.device_file = self.device_folder + '/w1_slave'
		self.tempc = ''
		self.tempf = ''

	def read_temp_raw(self):
	    f = open(self.device_file, 'r')
	    lines = f.readlines()
	    f.close()
	    return lines

	def read_temp(self):
	    lines = self.read_temp_raw()
	    while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	    equals_pos = lines[1].find('t=')
	    if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f
	def startup(self):
		if self.device_folder == "":
			self.stopbit = 0
			print "No temp sensor found"
		else:
			self.stopbit = 1
			print "Temp sensor found"
		try:
			while self.stopbit:
				temps = self.read_temp()
				self.tempc = temps[0]
				self.tempf = temps[1]
				time.sleep(1)
		except KeyboardInterrupt:
			self.stopbit = 0
	def stop(self):
		self.stopbit = 0


if __name__ == "__main__":
	tr = tempreader()
	tr.startup()
	
