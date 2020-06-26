# reading the input file
fileobj = open("input.txt", "r")
line = fileobj.readline()

# first two lines contain the dimension of the maze
maze_numrows, maze_numcols = [int(x) for x in line.split()]

 # reading the maze
i = 0
j = 0
maze = []
while (i < maze_numrows):
    line = fileobj.readline()
    val = [int(x) for x in line.split()]
    maze.append(val);
    i += 1

source = fileobj.readline()
sourcex, sourcey = source.split()[1:]
source = sourcex + " " + sourcey

dest = fileobj.readline()
destx, desty = dest.split()[1:]
dest = destx + " " + desty

i = 0
while (i < 5):
    direction = fileobj.readline().split()
    if (direction[0].upper() == "UP:"):
         cost_up = float(direction[1])
    elif (direction[0].upper() == "DOWN:"):
         cost_down = float(direction[1])
    elif (direction[0].upper() == "LEFT:"):
         cost_left = float(direction[1])	
    elif (direction[0].upper() == "RIGHT:"):
         cost_right = float(direction[1])
    elif (direction[0].upper() == "DIAGONAL:"):
         cost_diagonal = float(direction[1])
    i = i + 1

# building the adjacency list. 
i = 0
adjlist = {}
while(i < maze_numrows):
	j = 0
	while(j < maze_numcols):
		adjlistbuild = []
		if(maze[i][j] == 0):
            #northwest
			if(i - 1 >= 0) and  (j - 1 >= 0):
				if(maze[i - 1][j - 1] == 0):
					adjlistbuild.append(str(i - 1) + " " + str(j - 1))
			#north
			if(i - 1 >= 0):
				if(maze[i - 1][j] == 0):
					adjlistbuild.append(str(i - 1) + " " + str(j))
			#northeast
			if(i - 1 >= 0) and (j + 1 < maze_numcols):
				if(maze[i - 1][j + 1] == 0):
					adjlistbuild.append(str(i - 1) + " " + str(j + 1))
			#west
			if(j - 1 >= 0):
				if(maze[i][j - 1] == 0):
					adjlistbuild.append(str(i) + " " + str(j - 1))
			#east
			if(j + 1 < maze_numcols):
				if(maze[i][j + 1] == 0):
					adjlistbuild.append(str(i) + " " + str(j + 1))
			#southwest
			if(i + 1 < maze_numrows) and (j - 1 >= 0):
				if(maze[i + 1][j - 1] == 0):
					adjlistbuild.append(str(i + 1) + " " + str(j - 1))
			#south
			if(i + 1 < maze_numrows):
				if(maze[i + 1][j] == 0):
					adjlistbuild.append(str(i + 1) + " " + str(j))
			#southeast
			if(i + 1 < maze_numrows) and (j + 1 < maze_numcols):
				if(maze[i + 1][j + 1] == 0):
					adjlistbuild.append(str(i + 1) + " " + str(j + 1))

			adjlist[str(i) + " " + str(j)] = adjlistbuild
		j += 1
	i += 1


#dictionary for heuristic values
heuristics = {}
i = 0
while(i < maze_numrows):
	j = 0
	while(j < maze_numcols):
		val = (((int(destx) - i) ** 2.0) + (int(desty) - j) ** 2.0) ** (1.0 / 2.0)
		heuristics[str(i) + " " + str(j)] = val
		j = j + 1
	i = i + 1

import json
f = open('heuristics.txt', 'w')
f.write(json.dumps(heuristics))

# node
class Node:
	def __init__(self, coord, path_cost, f_n, parent):
		self.coord = coord
		self.path_cost = path_cost
		self.f_n = f_n
		self.parent = parent

# greedy best first search

# open and closed lists are initialized to be empty
fringe = []
explored = []

# appends the source node to the open list
fringe.append(Node(sourcex + " " + sourcey, 0, heuristics[sourcex + " " + sourcey], "none"))
curr_min = Node("dummy", 0 ,0 ,"dummy")

# checks if the current minimum is not equal to the destination
while (dest != curr_min.coord):

	# checks if no path exists
	if (len(fringe) == 0):
		break

	# gets the minimum f_n = h(n) where h(n) is the heuristic function
	minimum = fringe[0]
	i = 0
	while(i < len(fringe)):
		if(fringe[i].f_n <= minimum.f_n):
			minimum = fringe[i]
		i = i + 1
	curr_min = minimum

	# removes the node with the minimun f(n) on the open list and add it to the closed list
	fringe.remove(curr_min)
	explored.append(curr_min)
	for x in adjlist.keys():
		if curr_min in adjlist[x]:
			adjlist[x].remove(curr_min)
	explored_coords = [o.coord for o in explored]

	# determines the step cost
	for x in adjlist[curr_min.coord]:
		if (x not in explored_coords):
			c_min = curr_min.coord.split()
			exp = x.split()

            # movement = "right"
			if (int(exp[0]) == int(c_min[0])) and (int(exp[1]) == int(c_min[1]) + 1):
				step_cost = cost_right

            # movement = "left"
			if (int(exp[0]) == int(c_min[0])) and (int(exp[1]) == int(c_min[1]) - 1):
				step_cost = cost_left

            # movement = "up"
			if (int(exp[0]) == int(c_min[0]) - 1) and (int(exp[1]) == int(c_min[1])):
				step_cost = cost_up

            # movement = "down"
			if (int(exp[0]) == int(c_min[0]) + 1) and (int(exp[1]) == int(c_min[1])):
				step_cost = cost_down

            # movement = "diagonal"
			if (int(exp[0]) != int(c_min[0])) and (int(exp[1]) != int(c_min[1])):
				step_cost = cost_diagonal

			# every non-expanded node adjacent to min is added to the open list
			f_n = heuristics[x]
			fringe.append(Node(x, curr_min.path_cost + step_cost, f_n, curr_min))

path = []
path.append(curr_min.coord)
final_path_cost = curr_min.path_cost
f = open('greedy.out', 'w')
if (curr_min.coord == dest):
	
    # tracing the path from destination to root
	while (curr_min.coord != source):
		curr_min = curr_min.parent
		path.append(curr_min.coord)
	path.reverse()

	for x in path:
		f.write(x + "\n")
	f.write(str(final_path_cost))

else : 
	f.write("No path from source to destination.")
f.close()

# a-star search

# initialiazes open and closed list
fringe = []
explored = []

# appends the source node to the open list
fringe.append(Node(sourcex + " " + sourcey, 0, 0 + heuristics[sourcex + " " + sourcey], "none"))
curr_min = Node("dummy", 0, 0, "dummy")

# checks if  the current minimum is not equal to the destination
while (dest != curr_min.coord):

	# checks if no path exists
	if (len(fringe) == 0):
		break

	# gets the minimum f_n = g(n) + h(n) where h(n) is the heuristic function and g(n) is the path cost from source to current
	minimum = fringe[0]

	i = 0
	while(i < len(fringe)):
		if(fringe[i].f_n <= minimum.f_n):
			minimum = fringe[i]
		i = i + 1
	curr_min = minimum

	# removes the node with the minimun f(n) on the open list and add it to the closed list
	fringe.remove(curr_min)
	explored.append(curr_min)
	for x in adjlist.keys():
		if curr_min in adjlist[x]:
			adjlist[x].remove(curr_min)
	explored_coords = [o.coord for o in explored]

	# determines the step cost
	for x in adjlist[curr_min.coord]:
		if (x not in explored_coords):
			c_min = curr_min.coord.split()
			exp = x.split()
            
            # movement = "right"
			if (int(exp[0]) == int(c_min[0])) and (int(exp[1]) == int(c_min[1]) + 1):
				step_cost = cost_right

            # movement = "left"
			if (int(exp[0]) == int(c_min[0])) and (int(exp[1]) == int(c_min[1]) - 1):
				step_cost = cost_left

            # movement = "up"
			if (int(exp[0]) == int(c_min[0]) - 1) and (int(exp[1]) == int(c_min[1])):
				step_cost = cost_up

            # movement = "down"
			if (int(exp[0]) == int(c_min[0]) + 1) and (int(exp[1]) == int(c_min[1])):
				step_cost = cost_down

            # movement = "diagonal"
			if (int(exp[0]) != int(c_min[0])) and (int(exp[1]) != int(c_min[1])):
				step_cost = cost_diagonal

			#every non-expanded node adjacent to min is added to the open list
			f_n = curr_min.path_cost + step_cost + heuristics[x]
			fringe.append(Node(x, curr_min.path_cost + step_cost ,f_n, curr_min))

path = []
path.append(curr_min.coord)
final_path_cost = curr_min.path_cost
f = open('astar.out', 'w')
if (curr_min.coord == dest):
	#tracing the path from destination to root
	while (curr_min.coord != source):
		curr_min = curr_min.parent
		path.append(curr_min.coord)
	path.reverse()

	for x in path:
		f.write(x + "\n")
	f.write(str(final_path_cost))
else : 
	f.write("No path from source to destination.")
f.close()