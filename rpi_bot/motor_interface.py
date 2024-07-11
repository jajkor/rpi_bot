import RPi.GPIO as GPIO
import time

class RPi_Motors(object):

	def __init__(self, in1=27, in2=22, ena=17, in3=10, in4=9, enb=11):
		self.IN1 = in1
		self.IN2 = in2
		self.IN3 = in3
		self.IN4 = in4
		self.ENA = ena
		self.ENB = enb

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.IN1,GPIO.OUT)
		GPIO.setup(self.IN2,GPIO.OUT)
		GPIO.setup(self.IN3,GPIO.OUT)
		GPIO.setup(self.IN4,GPIO.OUT)
		GPIO.setup(self.ENA,GPIO.OUT)
		GPIO.setup(self.ENB,GPIO.OUT)
		self.forward(1)
		self.PWMA = GPIO.PWM(self.ENA,50)
		self.PWMB = GPIO.PWM(self.ENB,50)
		self.PWMA.start(0)
		self.PWMB.start(0)

	def __del__(self):
		GPIO.cleanup()

	def forward(self, seconds):
		GPIO.output(self.IN1, GPIO.HIGH)
		GPIO.output(self.IN2, GPIO.LOW)
		GPIO.output(self.IN3, GPIO.LOW)
		GPIO.output(self.IN4, GPIO.HIGH)
		time.sleep(seconds)

	def stop(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)

	def backward(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.HIGH)
		GPIO.output(self.IN3,GPIO.HIGH)
		GPIO.output(self.IN4,GPIO.LOW)

	def left(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.HIGH)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.HIGH)

	def right(self):
		GPIO.output(self.IN1,GPIO.HIGH)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.HIGH)
		GPIO.output(self.IN4,GPIO.LOW)

	def setPWMA(self,value):
		self.PWMA.ChangeDutyCycle(value)

	def setPWMB(self,value):
		self.PWMB.ChangeDutyCycle(value)

	def setMotors(self, left_vel, right_vel):
		# Right Motor
		if (left_vel >= 0) and (left_vel <= 100):
			GPIO.output(self.IN1, GPIO.HIGH)
			GPIO.output(self.IN2, GPIO.LOW)
			self.PWMA.ChangeDutyCycle(left_vel)
		elif (left_vel < 0) and (left_vel >= -100):
			GPIO.output(self.IN1, GPIO.LOW)
			GPIO.output(self.IN2, GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - left_vel)

        # Left Motor
		if (right_vel >= 0) and (right_vel <= 100):
			GPIO.output(self.IN3, GPIO.HIGH)
			GPIO.output(self.IN4, GPIO.LOW)
			self.PWMB.ChangeDutyCycle(right_vel)
		elif (right_vel < 0) and (right_vel >= -100):
			GPIO.output(self.IN3, GPIO.LOW)
			GPIO.output(self.IN4, GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - right_vel)


def main():
	bot = RPi_Motors()

if __name__=='__main__':
	main()