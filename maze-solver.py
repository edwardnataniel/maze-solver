class node:
    	def __init__(self, coord, path_cost, f_n, parent):
            self.coord = coord
            self.path_cost = path_cost
            self.f_n = f_n
            self.parent = parent

class maze:
    def __init__(self, maze_attributes):
        for attr in maze_attributes:
            setattr(self, attr, maze_attributes[attr])
        self.build_adjlist()
        self.compute_heuristics()

    def build_adjlist(self):
        """
        Builds a dictionary that contains the adjacency list based on the maze paths.
        """
        adj_list = {}
        for i in range(0, self.maze_numrows):
            for j in range (0, self.maze_numcols):
                adjacent_cells = []
                if(self.paths[i][j] == 0):
                    # check if connected to northwest cell
                    if(i - 1 >= 0) and  (j - 1 >= 0):
                        if(self.paths[i - 1][j - 1] == 0):
                            adjacent_cells.append(str(i - 1) + " " + str(j - 1))
                    # check if connected to north cell
                    if(i - 1 >= 0):
                        if(self.paths[i - 1][j] == 0):
                            adjacent_cells.append(str(i - 1) + " " + str(j))
                    # check if connected to northeast cell
                    if(i - 1 >= 0) and (j + 1 < self.maze_numcols):
                        if(self.paths[i - 1][j + 1] == 0):
                            adjacent_cells.append(str(i - 1) + " " + str(j + 1))
                    # check if connected to west cell
                    if(j - 1 >= 0):
                        if(self.paths[i][j - 1] == 0):
                            adjacent_cells.append(str(i) + " " + str(j - 1))
                    # check if connected to east cell
                    if(j + 1 < self.maze_numcols):
                        if(self.paths[i][j + 1] == 0):
                            adjacent_cells.append(str(i) + " " + str(j + 1))
                    # check if connected to southwest cell
                    if(i + 1 < self.maze_numrows) and (j - 1 >= 0):
                        if(self.paths[i + 1][j - 1] == 0):
                            adjacent_cells.append(str(i + 1) + " " + str(j - 1))
                    # check if connected to south cell
                    if(i + 1 < self.maze_numrows):
                        if(self.paths[i + 1][j] == 0):
                            adjacent_cells.append(str(i + 1) + " " + str(j))
                    # check if connected to southeast cell
                    if(i + 1 < self.maze_numrows) and (j + 1 < self.maze_numcols):
                        if(self.paths[i + 1][j + 1] == 0):
                            adjacent_cells.append(str(i + 1) + " " + str(j + 1))
                    adj_list[str(i) + " " + str(j)] = adjacent_cells                    
        setattr(self, 'adj_list', adj_list)

    def compute_heuristics(self):
        """
        Builds a dictionary that contains the heuristic values based on the maze paths.
        Heuristic values are computed as the euclidean distance of each cell to the destination cell.
        """
        heuristics = {}
        dest_x, dest_y = self.dest.split()
        for i in range(0, self.maze_numrows):
            for j in range(0, self.maze_numcols):
                val = (((int(dest_x) - i) ** 2.0) + (int(dest_y) - j) ** 2.0) ** (1.0 / 2.0)
                heuristics[str(i) + " " + str(j)] = val
        setattr(self, 'heuristics', heuristics)

    def solve_maze(self, algorithm):
        """
        Performs the specified search algorithm to solve the maze.
        """
        fringe = []
        explored = []

        # appends the source node to the open list
        fringe.append(node(self.source, 0, self.heuristics[self.source], "none"))
        curr_min = node("", 0 ,0 ,"")

        # checks if the current minimum is not equal to the destination
        while (self.dest != curr_min.coord):
            # checks if no path exists
            if (len(fringe) == 0):
                break

            # gets the minimum f_n = h(n) where h(n) is the heuristic function
            curr_min = min(fringe, key=lambda fringe: fringe.f_n)

            # removes the node with the minimun f(n) on the open list and add it to the closed list
            fringe.remove(curr_min)
            explored.append(curr_min)
            for cell in self.adj_list.keys():
                if curr_min in self.adj_list[cell]:
                    self.adj_list[cell].remove(curr_min)
            explored_coords = [o.coord for o in explored]

            # determines the step cost and recomputes the heuristic functions
            for cell in self.adj_list[curr_min.coord]:
                if (cell not in explored_coords):
                    c_min = curr_min.coord.split()
                    exp = cell.split()

                    # movement = "right"
                    if (int(exp[0]) == int(c_min[0])) and (int(exp[1]) == int(c_min[1]) + 1):
                        step_cost = self.cost_right

                    # movement = "left"
                    if (int(exp[0]) == int(c_min[0])) and (int(exp[1]) == int(c_min[1]) - 1):
                        step_cost = self.cost_left

                    # movement = "up"
                    if (int(exp[0]) == int(c_min[0]) - 1) and (int(exp[1]) == int(c_min[1])):
                        step_cost = self.cost_up

                    # movement = "down"
                    if (int(exp[0]) == int(c_min[0]) + 1) and (int(exp[1]) == int(c_min[1])):
                        step_cost = self.cost_down

                    # movement = "diagonal"
                    if (int(exp[0]) != int(c_min[0])) and (int(exp[1]) != int(c_min[1])):
                        step_cost = self.cost_diagonal

                    # every non-expanded node adjacent to min is added to the open list
                    if algorithm == 'greedy':
                        f_n = self.heuristics[cell]
                    elif algorithm == 'astar':
                        f_n = curr_min.path_cost + step_cost + self.heuristics[cell]
                    fringe.append(node(cell, curr_min.path_cost + step_cost, f_n, curr_min))

        solution_path = self.trace_path(curr_min)
        solution_cost = curr_min.path_cost
        solution = {'path': solution_path, 'cost': solution_cost}
        return solution

    def trace_path(self, curr_node):
        """
        Traces the path discovered from destination back to the source.
        """
        if (curr_node.coord == self.dest):
            path = []
            path.append(curr_node.coord)
            final_path_cost = curr_node.path_cost

            # tracing the path from destination to root
            while (curr_node.coord != self.source):
                curr_node = curr_node.parent
                path.append(curr_node.coord)
            path.reverse()
            return path
        else : 
            return None

def parse_input(file_object):
    """
    Parses the maze attributes from the input file.
    """
    maze_attributes = dict()

    line = file_object.readline()
    maze_numrows, maze_numcols = [int(x) for x in line.split()]

    maze_attributes['maze_numrows'] = maze_numrows
    maze_attributes['maze_numcols'] = maze_numcols
    maze_attributes['paths'] = []

    for i in range(0, maze_numrows):
        line = file_object.readline()
        row_values = [int(x) for x in line.split()]
        maze_attributes['paths'].append(row_values)

    source = file_object.readline().split(':')[1].strip()
    maze_attributes['source'] = source

    dest = file_object.readline().split(':')[1].strip()
    maze_attributes['dest'] = dest

    for i in range(0, 5):
        direction = file_object.readline().split()
        if (direction[0].lower() == 'up:'):
            maze_attributes['cost_up'] = float(direction[1])
        elif (direction[0].lower() == 'down:'):
            maze_attributes['cost_down'] = float(direction[1])
        elif (direction[0].lower() == 'left:'):
            maze_attributes['cost_left'] = float(direction[1])
        elif (direction[0].lower() == 'right:'):
            maze_attributes['cost_right'] = float(direction[1])
        elif (direction[0].lower() == 'diagonal:'):
            maze_attributes['cost_diagonal'] = float(direction[1])
    return maze_attributes

def create_maze(file_object):
    """
    Reads an input file and runs the greedy and a-star algorithm.
    """
    maze_attributes = parse_input(file_object)
    maze_object = maze(maze_attributes)
    return maze_object

def write_output(filename, solution):
    """
    Writes the solution of the searching algorithm to the specified filename.
    """
    file_object = open(filename, "w")
    if solution['path'] != None:
        for cell in solution['path']:
            file_object.write(cell + '\n')
        file_object.write(str(solution['cost']))
    else:
        file_object.write('No path exists from source to destination.')
    file_object.close()

def main():
    """
    Reads an input file and runs the greedy and a-star algorithm.
    """
    file_object = open("input.txt", "r")
    maze_object = create_maze(file_object)
    file_object.close()

    solution_greedy = maze_object.solve_maze('greedy')
    write_output('greedy.out', solution_greedy)

    solution_astar = maze_object.solve_maze('astar')
    write_output('astar.out', solution_astar)

if __name__ == "__main__":
    main()