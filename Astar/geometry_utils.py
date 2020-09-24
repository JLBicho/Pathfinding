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