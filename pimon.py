import math
import time
import Adafruit_CharLCD as LCD
import psutil
import threading
from pydispatch import dispatcher
import lcdbut
import tempreader

color=3
colorlist = [[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,1,1]]
#
#	That's right, you need psutil installed.  AFAIK, all you have to do on Raspbian is enter:
#				sudo apt-get install build-essential python-dev python-pip
#	Followed by:
#				sudo pip install psutil
#	And then you can check by making sure you get no errors when you execute:
#				sudo python -c "import psutil"
#
#
#


# Initialize the plate
lcd = LCD.Adafruit_CharLCDPlate()

# Clear content
lcd.clear()

# Set color to blac (RGB)
lcd.set_color(0, 0, 0)

# This is the loop variable.
GoBabyGo = True

# Set up the display with static CPU: and RAM:
msg = "CPU:   \nRAM:    "
lcd.message(msg)

def goRight():
	global color
	if color == (len(colorlist) - 1):
		color = 0
	else:
		color += 1
	updateColor()
def goLeft():
	global color
	if color == 0:
		color = (len(colorlist) - 1)
	else:
		color -= 1
	updateColor()
def updateColor():
	lcd.set_color(colorlist[color][0], colorlist[color][1], colorlist[color][2])

dispatcher.connect( goLeft, signal='leftPressed', sender=dispatcher.Any)
dispatcher.connect( goRight, signal='rightPressed', sender=dispatcher.Any)

x = lcdbut.lcdbut(lcd)

t = threading.Thread(target=x.startup)

t.start()

tr = tempreader.tempreader()
trThread = threading.Thread(target=tr.startup)
trThread.daemon = True
trThread.start()

# Start checking the processor and memory
while GoBabyGo:

	# Retrieve CPU and RAM usage
	cpu = psutil.cpu_percent()
	ram = psutil.virtual_memory()
	# Check the temp of the sensor
	tempf = tr.tempf
	
	# Check the length of the floating point number.  We want to make sure it's pretty in the output.
	if len(str(cpu)) < 4:
		# Prepend a space to X.X format and add percent sign
		msg = " " + str(cpu) + "% "
	else:
		# Add percent sign to XX.X format
		msg = str(cpu) + "% "
		
	# Place the cursor at the beginning of the number spot for CPU usage and update the message to the LCD
	lcd.set_cursor(5, 0)
	lcd.message(msg)
	
	# Check the length of the floating point number.  We want to make sure it's pretty in the output.
	if len(str(ram.percent)) < 4:
		# Prepend a space to X.X format and add percent sign
		msg = " " + str(ram.percent) + "%"
	else:
		# Add percent sign to XX.X format
		msg = str(ram.percent) + "%"
		
	# Place the cursor at the beginning of the number spot for RAM usage and update the message to the LCD
	lcd.set_cursor(5, 1)
	lcd.message(msg)

	# Now set color threshholds.
	#	If CPU usage is above 75% then set the color of the display to red
	#	If CPU usage is above 50% (but less than 75%) set the color to yellow
	#	If CPU usage is under 50%, set the color to green (or other default color you've chosen via buttons)
	if cpu >= 75.0 or ram.percent >=75.0:
		lcd.set_color(1, 0, 0)
	elif (cpu >= 50.0 and cpu < 75) or (ram.percent >= 50 and ram.percent < 75.0):
		lcd.set_color(1, 1, 0)
	else:
		updateColor()

	# This is just a temp placeholder
	lcd.set_cursor(11, 1)
	lcd.message(str(tempf))
		
	# Sleep for 1 second, then do the next update
	try:
		time.sleep (1)
		
	except KeyboardInterrupt:
		print "Killing button listener and exiting..."
		x.stop = True
		lcd.clear()
		lcd.set_backlight(False)
		lcd.enable_display(False)
		tr.stopbit = 0
		exit()
