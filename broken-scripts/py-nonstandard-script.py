import os, sys
from math import *

class myclass:
	def __init__(self, x, y):
		self.X = x
		self.Y = y
	def MyFunction(self):
		return self.X+self.Y
	def anotherFunction(self):
		try:
			if self.X == None:
				print("X is None")
			elif self.Y == None:
				print("Y is None")
			elif self.X == True:
				print("X is True")
			elif self.Y == False:
				print("Y is False")
			return self.X / self.Y
		except:
			return "Error"

def calculateAverage(Numbers):
	total=0
	for num in Numbers:
		total+=num
	return total/len(Numbers)

if __name__=="__main__":
	instance=myclass(10,5)
	print("Sum:",instance.MyFunction())
	print("Div:",instance.anotherFunction())

	Numbers=[10,20,30,40,50]
	print("Avg:",calculateAverage(Numbers))
