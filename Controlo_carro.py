import math
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200)

#angulo da roda
R = 0.15

def controlo (angulo):
#calculo da velocidade angular do carro
	LAMB = 10
	omega_robot = LAMB * math.sin(angulo)
	V = 0.3

#calculo da velocidade de cada roda
	omega_l = (V - R * omega_robot) / R
	omega_r = (V + R * omega_robot) / R

#calculo da tensão a ser aplicada a cada motor
	M = (12-6)/(169.2-77.5)

	vl = ((omega_l * 2*math.pi * M) / 60)
	vr = ((omega_r * 2*math.pi * M) / 60)
#envio dos valores de tensão para a stm32
	ser.write ('sou lindo')

