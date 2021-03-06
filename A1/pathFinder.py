# Generates 2x2 matrix for maze using DFS random tiebreaking
import time
import random
import sys
import math
import pygame
import heapq
import csv
import os
from mazeBuild import *

dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0,0,128)
GOLD = (255,215,0)
# This sets the WIDTH and HEIGHT of each grid location
WIDTH =	8
HEIGHT = 7
REMOVED = '<removed-point>'
class PriorityQueue:
	def __init__(self):
		self.elements = []
		self._dict = {}

	def empty(self):
		return len(self.elements) == 0

	def put(self, point, priority):
		e = (priority,point)
		heapq.heappush(self.elements, e)
		self._dict[point] = e

	def contains(self, point):
		return point in self._dict

	def remove(self, item):
		entree = self._dict.pop(item)
		entree[-1] = REMOVED

	def get(self):
		while self.elements:
			priority, point = heapq.heappop(self.elements)
			if point is not REMOVED:
				del self._dict[point]
				return point
		raise KeyError('pop from an empty priorty queue')


# This sets the margin between each cell
MARGIN = 1
counter = 0
openSet = PriorityQueue()
closedSet = {}



def randomPoint(x,y):
	return (random.randint(0,x-1),random.randint(0,y-1))



def pointEquals(a,b):
	if ( a[0] == b[0] and a[1] == b[1] ):
		return 1
	else:
		return 0

def heuristic_func(start,goal):
    return abs(start[0]-goal[0]) + abs(start[1]-goal[1])

#def dfstie(maze):

class Maze(object):
	def __init__(self, x= 101, y=101):
		self.x = x
		self.y = y
		self.maze = [[0 for i in range(self.x)] for j in range(self.y)]
		self.start = ()
		self.goal = ()

	#def dfsMaze():

def generateMaze(m):
	temp = randomPoint(m.x,m.y)
	stack = [temp]
	visited_set = set()
	visited_set.add(((temp[0],temp[1])))
	while len(stack) > 0:
	    (cx, cy) = stack[-1]
	    visited_set.add((cx, cy))
	    if random.random() < .30:
	    	m.maze[cx][cy] = 0
	    else:
	    	m.maze[cx][cy] = 1

	    # find a new cell to add
	    nlst = [] # list of available neighbors
	    for i in range(4):
	        nx = cx + dx[i]; ny = cy + dy[i]
	        if nx >= 0 and nx < m.x and ny >= 0 and ny < m.y:
	            if (nx,ny) not in visited_set:
	                # of occupied neighbors must be 1
	                nlst.append(i)
	    # if 1 or more neighbors available then randomly select one and move
	    if len(nlst) > 0:
	        ir = nlst[random.randint(0, len(nlst) - 1)]
	        cx += dx[ir]; cy += dy[ir]
	        stack.append((cx, cy))
	    else: stack.pop()

gscore = {}
fscore = {}
hscore = {}
tree = {}
foundblocks = set()
total_path = []
mx = 101
my = 101
maze = Maze(mx,my)
mode = ""
maxgscore = mx*my-1
if len(sys.argv) > 1:
	mode = sys.argv[1]

def RFAS(testNum, filename, count, dataType=None, write=False):
	global maze, openSet, closedSet, gscore, fscore, tree, foundblocks, hscore

	# if dataType != None:
	# 	mode = dataType
	#
	if(not pointEquals(maze.start,maze.goal)):
		gscore = {}
		fscore = {}
		expandednodes = []
		if mode == "back":
			gscore = {maze.goal:0}
			fscore = {maze.goal:heuristic_func(maze.start,maze.goal)}
			gscore[maze.start] = math.inf

		else:
			gscore = {maze.start:0}
			if mode == "adaptive" and maze.start in hscore:
				fscore = {maze.start:hscore[maze.start]}
			else:
				fscore = {maze.start:heuristic_func(maze.start,maze.goal)}
			gscore[maze.goal] = math.inf

		openSet.elements = []
		openSet._dict = {}
		tree = {}
		closedSet = set()
		if not mode:
			openSet.put(maze.start,fscore[maze.start])
		if mode == "highg" or mode == "adaptive":
			openSet.put(maze.start,maxgscore*fscore[maze.start] - gscore[maze.start])
		if mode == "lowg":
			openSet.put(maze.start,maxgscore*fscore[maze.start] + gscore[maze.start])
		if mode == "back":
			openSet.put(maze.goal,fscore[maze.goal])
		#updates observed blockings
		for i in range(4):
			next = (maze.start[0] + dx[i], maze.start[1] + dy[i])
			if next[0] >= 0 and next[0] < maze.x and next[1] >= 0 and next[1] < maze.y:
				# check surroundings if blocked
					if(maze.maze[next[0]][next[1]] == 0):
						foundblocks.add(next)
		if(len(total_path) == 0):
			start = time.time()
			if mode == "back":
				computePath(maze.goal,maze.start)
			else:
				computePath(maze.start,maze.goal)
			end = time.time()
			print('astar calculation took: ' + str(end-start))
			if write:
				with open(filename, 'a') as csvfile:
					writer = csv.writer(csvfile, delimiter=',')
					writer.writerow([count, testNum, str(end-start)])
		else:
			for points in total_path:
				if points in foundblocks:
					start = time.time()
					if mode == "back":
						computePath(maze.goal,maze.start)
					else:
						computePath(maze.start,maze.goal)
					end = time.time()
					print('astar calculation took: ' + str(end-start))
					if write:
						with open(filename, 'a') as csvfile:
							writer = csv.writer(csvfile, delimiter=',')
							writer.writerow([count, testNum, str(end-start)])
			if(pointEquals(maze.start,total_path[0])):
				total_path.pop(0)
			maze.start = total_path.pop(0)

		if openSet.empty():
			print ("I cannot reach the target")
			if write:
				with open(filename, 'a') as csvfile:
					writer = csv.writer(csvfile, delimiter=',')
					writer.writerow(["FAIL", "FAIL", "FAIL"])
			return -1
	else:
		print('I am at the target')
		if write:
			with open(filename, 'a') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				writer.writerow(["DONE","DONE","DONE"])
		return 1

def computePath(start, goal):
	global counter, maze, openSet, closedSet, gscore, fscore, tree, foundblocks, hscore
	while(not openSet.empty()):
		tempg = {}
		tempf = {}
		current = openSet.get()
		#print (current)

		if pointEquals(current, goal):
			return construct_path(current)



		closedSet.add(current)
		nlst = [] # list of available neighbors
		for i in range(4):
			next = (current[0] + dx[i], current[1] + dy[i])
			if next[0] >= 0 and next[0] < maze.x and next[1] >= 0 and next[1] < maze.y and next not in foundblocks:
				# of occupied neighbors must be 1
					gscore[next] = gscore[current] + 1
					nlst.append(next)
		for succ in nlst:
			if succ in closedSet:
				continue

			if not openSet.contains(succ):
				gscore[succ] = gscore[current] + 1
				if mode == "adaptive" and succ in hscore:
					fscore[succ] = gscore[succ] + hscore[succ]
				else:
					fscore[succ] = gscore[succ] + heuristic_func(succ,maze.goal)
				tree[succ] = current
				if not mode or mode == "back":
					openSet.put(succ, fscore[succ])
				if mode == "highg" or mode == "adaptive":
					openSet.put(succ, maxgscore*fscore[succ]-gscore[succ])
				if mode == "lowg":
					openSet.put(succ, maxgscore*fscore[succ]+gscore[succ])
			else:
				tentativeg = gscore[current] + 1
				if tentativeg >= gscore[succ]:
					continue
				else:
					tree[succ] = current
					gscore[succ] = gscore[current] + 1
					if mode == "adaptive" and succ in hscore:
						fscore[succ] = gscore[succ] + hscore[succ]
					else:
						fscore[succ] = gscore[succ] + heuristic_func(succ,maze.goal)
					openSet.remove(succ)
					if not mode or mode == "back":
						openSet.put(succ, fscore[succ])
					if mode == "highg" or mode == "adaptive":
						openSet.put(succ, maxgscore*fscore[succ]-gscore[succ])
					if mode == "lowg":
						openSet.put(succ, maxgscore*fscore[succ]+gscore[succ])

def construct_path(current):
	global maze, total_path, hscore, closedSet
	total_path = [current]
	while current in tree.keys():
		current = tree[current]
		if mode == "back":
			total_path.append(current)
		else:
			total_path.insert(0,current)
	if mode == "adaptive":
		for point in closedSet:
			hscore[point] = gscore[maze.goal] - gscore[point]


def main():
	#pass in testcase number as string, returns 2d array
	testNum = input("Please specify testcase to perform A* on (1-50): ")
	maze.maze = test_to_array(testNum)

	#omaze = [[1 for i in range(maze.x)] for j in range(maze.y)]
	#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in maze.maze]))
	# maze.maze =
	#print('\n')
	#print('[{}]'.format(',\n'.join(['[{}]'.format(','.join(['{}'.format(item) for item in row])) for row in maze.maze])))
	maze.start = startPoint(testNum)
	maze.maze[maze.start[0]][maze.start[1]] = 1


	maze.goal = goalPoint(testNum)

	if len(sys.argv) > 1:
		dataType = sys.argv[1]
	else:
		dataType = 'normal'

	filename = 'data/' + dataType + '/test' + testNum + '.csv'
	#cleaning files for record keeping
	# i:
	# try:
	#     os.remove(filename)
	# except OSError:
	#     pass

	while(pointEquals(maze.start,maze.goal)):
			maze.goal = randomPoint(mx,my)
	maze.maze[maze.goal[0]][maze.goal[1]] = 1

	pygame.init()
	size =((WIDTH+MARGIN)*maze.y,(WIDTH+HEIGHT)*maze.x)
	sq_size = 64
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("A*")
	done = False
	view = True
	clock = pygame.time.Clock()
	count = 1
	#Main program loop
	while not done:
		for event in pygame.event.get():  # User did something
			if event.type == pygame.QUIT:  # If user clicked close
				done = True  # Flag that we are done so we exit this loop
				#elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
					done = True
				if event.key == pygame.K_SPACE:
					RFAS(testNum, filename, count)
					count += 1
					#for x in total_path:
					#	print (x[0], x[1])
				if event.key == pygame.K_TAB:
					view = not view
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
				maze.start = (row,column)
	# Debug prints
				print("Start ", pos, "Grid coordinates: ", row, column)
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
				maze.goal = (row,column)
				# Debug prints
				print("Goal ", pos, "Grid coordinates: ", row, column)


	    # --- Game logic should go here
		pos = pygame.mouse.get_pos()
		x = pos[0]
		y = pos[1]

		# Set the screen background
		screen.fill(BLACK)
		if view:
			for row in range(maze.x):
				for column in range(maze.y):
					color = BLACK
					if maze.maze[row][column] == 1:
						color = WHITE
					if maze.start[0] == row and maze.start[1] == column:
						color = GREEN
					if maze.goal[0] == row and maze.goal[1] == column:
						color = RED
					pygame.draw.rect(screen,color,
					[(MARGIN + WIDTH) * column + MARGIN,
					(MARGIN + HEIGHT) * row + MARGIN,
					WIDTH,
					HEIGHT])
		else:
			for row in range(maze.x):
				for column in range(maze.y):
					color = WHITE
					if (row,column) in foundblocks:
						color = BLACK
					if maze.start[0] == row and maze.start[1] == column:
						color = GREEN
					if maze.goal[0] == row and maze.goal[1] == column:
						color = RED
					pygame.draw.rect(screen,color,
					[(MARGIN + WIDTH) * column + MARGIN,
					(MARGIN + HEIGHT) * row + MARGIN,
					WIDTH,
					HEIGHT])
		for points in total_path:
			pygame.draw.circle(screen,GOLD,
				((MARGIN + WIDTH) * points[1] + MARGIN + 4,
				(MARGIN + HEIGHT) * points[0] + MARGIN + 4),
				3,
				3)
		# Limit to 60 frames per second
		clock.tick(2)
		pygame.display.flip()

	pygame.quit()

def test(testNum='-1', mode=""):
	#pass in testcase number as string, returns 2d array
	if testNum == '-1':
		testNum = input("Please specify testcase to perform A* on (1-50): ")

	maze.maze = test_to_array(testNum)

	#omaze = [[1 for i in range(maze.x)] for j in range(maze.y)]
	#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in maze.maze]))
	# maze.maze =
	#print('\n')
	#print('[{}]'.format(',\n'.join(['[{}]'.format(','.join(['{}'.format(item) for item in row])) for row in maze.maze])))
	maze.start = startPoint(testNum)
	# print (maze.start)
	maze.maze[maze.start[0]][maze.start[1]] = 1


	maze.goal = goalPoint(testNum)
	count = 1
	write = True
	# if len(sys.argv) > 1:
	# 	dataType = sys.argv[1]
	# else:
	# 	dataType = 'normal'
	if mode == "":
		dataType = 'normal'
	else:
		dataType = mode
		print(dataType)

	filename = 'data/' + dataType + '/test' + testNum + '.csv'
	#cleaning files for record keeping
	try:
	    os.remove(filename)
	except OSError:
	    pass

	while(pointEquals(maze.start,maze.goal)):
			maze.goal = randomPoint(mx,my)
	maze.maze[maze.goal[0]][maze.goal[1]] = 1

	status = 0
	while status != -1 and status != 1:
		status = RFAS(testNum, filename, count, mode, write)
		count += 1

	if status == 1:
		return "goal found"
	else:
		return "goal not reached"

if __name__ == "__main__":
	main()
	# test()
