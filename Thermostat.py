# servo control
import time
import wiringpi

class Thermostat:
	ON_DEGREE = 200
	OFF_DEGREE = 75 
	OUTPUT_PIN = 12
	DELAY_PERIOD = 0.01

	def __init__(self):
		self.current_degree = Thermostat.OFF_DEGREE
		# use 'GPIO naming'
		wiringpi.wiringPiSetupGpio()

		# set OUTPUT_PIN to be a PWM output
		wiringpi.pinMode(Thermostat.OUTPUT_PIN, wiringpi.GPIO.PWM_OUTPUT)

		# set the PWM mode to milliseconds stype
		wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

		# divide down clock
		wiringpi.pwmSetClock(192)
		wiringpi.pwmSetRange(2000)
	
	def turn_on(self):
		for pulse in range(self.current_degree, Thermostat.ON_DEGREE, 1):
			wiringpi.pwmWrite(Thermostat.OUTPUT_PIN, pulse)
			time.sleep(Thermostat.DELAY_PERIOD)
		self.current_degree = Thermostat.ON_DEGREE

	def turn_off(self):
		for pulse in range(self.current_degree, Thermostat.OFF_DEGREE, -1):
			wiringpi.pwmWrite(Thermostat.OUTPUT_PIN, pulse)
			time.sleep(Thermostat.DELAY_PERIOD)
		self.current_degree = Thermostat.OFF_DEGREE
