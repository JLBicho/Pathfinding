global blocked, path, resolution, maxRange, borders

blocked = []
path = []
borders = []
resolution = 1
maxRange = 20

for i in range(-1,maxRange):
	borders.append((-resolution, i*resolution))
for i in range(-1,maxRange):
	borders.append(((maxRange)*resolution, i*resolution))
for i in range(-1,maxRange):
	borders.append((i*resolution, -resolution))
for i in range(-1,maxRange):
	borders.append((i*resolution, (maxRange)*resolution))


# Orientation
x_sgn = [-1, -1, 0, 1, 1,  1,  0, -1]
y_sgn = [ 0,  1, 1, 1, 0, -1, -1, -1]
direction = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']