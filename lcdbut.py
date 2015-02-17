import time
import Adafruit_CharLCD as LCD
from pydispatch import dispatcher
'''
SELECT = 0
RIGHT = 1
DOWN = 2
UP = 3
LEFT = 4
'''

class lcdbut:
	''' I should put something here '''
	def __init__(self, display):
		''' Initialize!!! '''
		
		self.stop = False
		self.interval = 0.1
		''' map contains LCD.BUTTONNAME, currentStateOfButton, SignalForButtonWhenPressed, SignalForButtonWhenReleased '''
		self.display = display
		self.buttons = [ [0, self.display.is_pressed(0), 'selectPressed', 'selectReleased'],
					[1, self.display.is_pressed(1), 'rightPressed', 'rightReleased'],
					[2, self.display.is_pressed(2), 'downPressed', 'downReleased'],
					[3, self.display.is_pressed(3), 'upPressed', 'upReleased'],
					[4, self.display.is_pressed(4), 'leftPressed', 'leftReleased'] ]
		
	def __buttonPressed(self, signal):
		dispatcher.send(signal)

	def startup(self):
		try:
			while not self.stop:
				__btn_index = 0
				while __btn_index < len(self.buttons):
					if self.display.is_pressed(self.buttons[__btn_index][0]):
						if not self.buttons[__btn_index][1]:
							self.buttons[__btn_index][1] = True
							self.__buttonPressed(self.buttons[__btn_index][2])
					else:
						if self.buttons[__btn_index][1]:
							self.buttons[__btn_index][1] = False
							self.__buttonPressed(self.buttons[__btn_index][3])
					__btn_index += 1
				time.sleep(self.interval)
		except KeyboardInterrupt:
			print "Exiting..."
			exit()
