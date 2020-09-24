import math
import random

import settings
from geometry_utils import position, pose

class robot:
	def __init__(self, position, orientation):
		self.pose = pose(position, orientation)
		self.distance = 0
		self.visited = []
		self.visited.append(self.pose.position.toTuple())
		self.last_bisection = None
		self.previous_pose = self.pose

	def printPoseAndDistance(self):
		print(self.pose.print(log=False) +" "+ str(round(self.distance)))


	def checkAround(self):
		around = [0, 0, 0, 0, 0, 0, 0, 0]
		check = position((0,0))
		for i in range(8):
			check.x = self.pose.position.x + settings.x_sgn[i] * settings.resolution
			check.y = self.pose.position.y + settings.y_sgn[i] * settings.resolution
			check2 = check.toTuple()
			if check2 not in settings.blocked and check2 not in settings.borders:
				around[i] = 0
			else:
				around[i] = -1

		orientation = dict(zip(settings.direction,around))
		return orientation

	def move(self, goal):
		
		dist2robot = [settings.resolution, math.sqrt(2)*settings.resolution]
		x_sgn = [-1, -1, 0, 1, 1,  1,  0, -1]
		y_sgn = [ 0,  1, 1, 1, 0, -1, -1, -1]
		direction = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
		
		around = [0, 0, 0, 0, 0, 0, 0, 0]
		check = position((0,0))
		for i in range(8):
			check.x = self.pose.position.x + x_sgn[i] * settings.resolution
			check.y = self.pose.position.y + y_sgn[i] * settings.resolution
			check2 = check.toTuple()
			if check2 in self.visited:
				penalizacion = self.visited.count(check2)*settings.resolution*5
			else:
				penalizacion = 0
			if check2 not in settings.blocked and check2 not in settings.borders:
				around[i] = dist2robot[i%2] + math.sqrt(pow(check.x-goal.x,2)+pow(check.y-goal.y,2)) + penalizacion
			else:
				around[i] = float("inf")
			for i in (0, 2, 4, 6):
				if i == 6:
					j = 0
				else: 
					j = i+2
				if around[i] == float("inf") and around[(j)] == float("inf"):
					around[i+1] = float("inf")
		
		minimum = float("inf")	
		for a in around:
			if a < minimum and a != float("inf"):
				minimum = a

		if around.count(minimum) > 1:
			min_idx = [i for i, value in enumerate(around) if value == minimum]
			idx = min_idx[random.randint(0,1)]
			self.last_bisection = self.pose.position
		else:
			idx = around.index(minimum)

		self.previous_pose = self.pose.__copy__()

		self.pose.position.x = self.pose.position.x + x_sgn[idx]*settings.resolution
		self.pose.position.y = self.pose.position.y + y_sgn[idx]*settings.resolution
		self.pose.orientation = direction[idx]
		self.distance = self.distance + dist2robot[idx%2]
		self.visited.append(self.pose.position.toTuple())
		settings.path.append(self.pose.__copy__())
