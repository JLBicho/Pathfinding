import math
import random
import time

class position:
	def __init__(self,pos):
		self.x = pos[0]
		self.y = pos[1]

	def print(self):
		print(str(self.x) + " " + str(self.y))

	def toTuple(self):
		return (self.x, self.y)

class pose:
	def __init__(self, pos, orientation):
		self.position = position(pos)
		self.orientation = orientation

	def print(self, log):
		if log:
			print(str(self.position.x) + " " + str(self.position.y) + " " + str(self.orientation))
		else:
			return str(self.position.x) + " " + str(self.position.y) + " " + str(self.orientation)

	def __copy__(self):
		self.normalizeArgs()
		return pose((self.position.x, self.position.y), self.orientation)

	def normalizeArgs(self):
		if not hasattr(self, "position"):
			self.position = None
		if not hasattr(self, "orientation"):
			self.orientation = None

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

	def move(self, goal):
		around = [0, 0, 0, 0, 0, 0, 0, 0]
		check = position((0,0))
		for i in range(8):
			check.x = robot.pose.position.x + x_sgn[i] * 10
			check.y = robot.pose.position.y + y_sgn[i] * 10
			check2 = check.toTuple()
			if check2 in self.visited:
				penalizacion = self.visited.count(check2)*resolution*5
			else:
				penalizacion = 0
			if check2 not in blocked:
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
			self.last_bisection = robot.pose.position
		else:
			idx = around.index(minimum)

		self.previous_pose = robot.pose.__copy__()

		robot.pose.position.x = robot.pose.position.x + x_sgn[idx]*10
		robot.pose.position.y = robot.pose.position.y + y_sgn[idx]*10
		robot.pose.orientation = direction[idx]
		self.distance = self.distance + dist2robot[idx%2]
		#self.printPoseAndDistance()
		self.visited.append(robot.pose.position.toTuple())
		path.append(robot.pose.__copy__())


resolution = 10

start = position((60, 60))
end = position((0, 0))
robot = robot(start.toTuple(), 'N')
# robot.printPoseAndDistance()


''' 
	BLOCKED POSITIONS
	The borders define a box
	If the box is nxn, then maxRange = n-1

	For example, lets define a 4x4 box like this

	 4X X X X X X
	 3X .	.	.	.	X
	 2X .	.	.	.	X
	 1X .	.	.	.	X
	 0X .	.	.	.	X
	-1X X X X X X
	 -1 0 1 2 3 4
	
	maxRange would be 5

	The blocked positions are to be defined individually
'''

borders = []
maxRange = 8
for i in range(-1,maxRange):
	borders.append((-resolution, i*resolution))
for i in range(-1,maxRange):
	borders.append(((maxRange-1)*resolution, i*resolution))
for i in range(-1,maxRange):
	borders.append((i*resolution, -resolution))
for i in range(-1,maxRange):
	borders.append((i*resolution, (maxRange-1)*resolution))
blocked = [(0,10),
					 (0,50),
					 (10,10),
					 (10,20),
					 (10,30),
					 (10,50),
					 (20,30),
					 (20,50),
					 (30,20),
					 (30,30),
					 (40,10),
					 (40,50),
					 (50,10),
					 (50,40),
					 (50,50),
					 (60,30),
					 (60,50)]
blocked.extend(borders)


''' 
	ROBOT SURROUNDINGS CHARACTERISTICS 
	dist2robot = distance the robot must move to go to the destination
	x_sign, y_sign = sign of the incremental X or Y to the position of the robot
	direction = where the robot is going
'''
dist2robot = [resolution, math.sqrt(2)*resolution]
x_sgn = [0, 1, 1, 1, 0, -1, -1, -1]
y_sgn = [1, 1, 0, -1, -1, -1, 0, 1]
direction = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

path = []
path.append(robot.pose.__copy__())

while 1:
	robot.move(end)
	if robot.pose.position.x == end.x and robot.pose.position.y == end.y:
		break

print(" ====== ====== ======")
print("Distance = " + str(round(robot.distance)))
print("Followed path: ")
for p in path:
	p.print(log=True)
print(" ====== ====== ======")
