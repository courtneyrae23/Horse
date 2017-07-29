import random
import collections

totalInstances = 3

def parseGraph(n):
	filename = "cs170_sample_inputs/sample" + str(n) + ".in"
	# filename = "sample1.in"
	fileObj = open(filename)
	V = int(fileObj.readline())
	weights = {}
	edges = {} 
	for i in range(V):
		line = fileObj.readline().split()
		weights[i] = int(line[i])
		edges[i] = []
		for j in range(len(line)):
			if i != j and int(line[j]) == 1:
				edges[i].append(j)
	return V, weights, edges

######################
#### Brute Force #####
###########################################################################

def bestSetOfTeams(teamSet):
	scores = []
	for teams in teamSet:
		score = 0
		for team in teams:
			total = 0       
			for node in team:
				total += weights[node]
			total *= len(team)
			score += total
		scores.append(score)

	return max(scores), teamSet[scores.index(max(scores))]


def bestPath(paths):
	scores = []
	for path in paths:
		total = 0       
		for node in path:
			total += weights[node]
		total *= len(path)
		scores.append(total)
	return max(scores), paths[scores.index(max(scores))]

def remainingNodes(v, deletedNodes):
	nodesLeft = [x for x in range(0, v)]
	for node in deletedNodes:
		nodesLeft.remove(node)
	return nodesLeft

def possiblePathsFromStart(v, weights, edges, start, deletedNodes, explored, path, possiblePaths):
	newpath = path[:]
	newpath.append(start)
	possiblePaths.append(newpath)

	newExplored = explored[:]
	newExplored.append(start)

	for node in edges[start]:
		if node not in explored and node not in deletedNodes:
			possiblePathsFromStart(v, weights, edges, node, deletedNodes, newExplored, newpath, possiblePaths)


def bestPossiblePathFromStart(v, weights, edges, start, deletedNodes):
	possiblePaths = []
	possiblePathsFromStart(v, weights, edges, start, deletedNodes, [], [], possiblePaths)
	score, path = bestPath(possiblePaths)
	return path

def bestPossibleTeamsFromStart(v, weights, edges, start):
	
	deletedNodes = []
	teams = []

	while len(deletedNodes) != v:

		nodesLeft = [x for x in range(0, v)]
		for node in deletedNodes:
			nodesLeft.remove(node)

		nextPossiblePaths = []

		for i in nodesLeft:
			nextPath = bestPossiblePathFromStart(v, weights, edges, i, deletedNodes)
			nextPossiblePaths.append(nextPath)

		nextBestScore, nextBestPath = bestPath(nextPossiblePaths)
		for node in nextBestPath:
			deletedNodes.append(node)
		teams.append(nextBestPath)
	return teams

def optimalTeams(v, weights, edges):

	teamSet = []

	for i in range(v):
		teamSet.append(bestPossibleTeamsFromStart(v, weights, edges, i))

	return bestSetOfTeams(teamSet)

#########################################################################################
#########################################################################################

###################################
#### Greedy With Optimizations ####
#########################################################################################

def heaviestFirstSearch(v, weights, edges, start, deletedNodes, explored, path):

	path.append(start)

	deletedNodesCopy = list(deletedNodes)
	exploredCopy = list(explored)
	maxScore = 0
	maxNode = -1
	for node in edges[start]:
		if node not in explored and node not in deletedNodes:
			val = lookAhead(v, weights, edges, node, deletedNodesCopy, exploredCopy, weights[node])
			if val > maxScore:
				maxScore = val
				maxNode = node

	if maxNode != -1:
		explored.append(start)
		return heaviestFirstSearch(v, weights, edges, maxNode, deletedNodes, explored, path)
	else:
		return path, explored

def lookAhead(v, weights, edges, start, deletedNodes, explored, score):
	max_weight = 0
	maxNextNode = -1
	count = 0

	while count < 3:
		for node in edges[start]:
			if node not in explored and node not in deletedNodes:
				if weights[node] >= max_weight:
					maxNextNode = node
					max_weight = weights[node]
		if maxNextNode != -1:
			explored.append(start)
			count+=1
			score+=max_weight
			start = maxNextNode
			max_weight = 0
			maxNextNode = -1
		else:
			return score*(count+1)
	return score*(count+1)

def findBestTeams(v, weights, edges, start):
	
	deletedNodes = []
	teams = []
	score = 0
	
	while len(deletedNodes) != v: 
	
		nodesLeft = [x for x in range(0, v)]
	
		total = 0

		heaviestPath, explored = heaviestFirstSearch(v, weights, edges, start, deletedNodes, [], [])
		for node in heaviestPath:
			total += weights[node]
			deletedNodes.append(node)
		total *= len(heaviestPath)

		score += total
		teams.append(heaviestPath)

		for node in deletedNodes:
			nodesLeft.remove(node)
		maxScore = 0
		maxNode = -1

		if len(deletedNodes) != v:
			betterNodesLeft = []
			for node in nodesLeft:
				if len(edges[node]) > 0:
					betterNodesLeft.append(node)
			if len(betterNodesLeft) == 0:
				start = nodesLeft[random.randint(0, len(nodesLeft)-1)]
			else:
				start = betterNodesLeft[random.randint(0, len(betterNodesLeft)-1)]

	return score, teams

def greedy(v, weights, edges, optimal):
	max_score = 0
	best_teams = []

	for i in range(v):
		if edges[i] == []:
			continue
		s, t = findBestTeams(v, weights, edges, i)
		if s > max_score:
			max_score = s
			best_teams = t
		if max_score == optimal:
			return max_score, best_teams
	return max_score, best_teams

###############################################################################################
###############################################################################################

def sanityCheck(v, weights,edges, teams):
	for team in teams: 
		i = 0
		while i < len(team) -1:
			if team[i+1] not in edges[team[i]]:
				return "Not Valid"
			i+=1
		return "Valid"

###############################################################################################
###############################################################################################

filename = "horse.out"
output = open(filename, 'w')

for i in range(1, totalInstances+1):
	v, weights, edges = parseGraph(i)
	print("\nInput number: " + str(i));
	print("Number of vertices: " + str(v));
	if (v <= 15):
		score, teams = optimalTeams(v, weights, edges)
		print("Optimal Score: ", v*sum(weights.values()))
		print("Our Score: ", score)
		print(sanityCheck(v, weights, edges, teams))
	else:
		score, teams = greedy(v, weights, edges,  v*sum(weights.values()))
		print("Optimal Score: ", v*sum(weights.values()))
		print("Our Score: ", score)
		print(sanityCheck(v, weights, edges, teams))
	for n in range(len(teams)):
		for m in range(len(teams[n])):
			if m == len(teams[n]) - 1 and n != len(teams) - 1:
				output.write(str(teams[n][m]) + "; ")
			elif m == len(teams[n]) - 1 and n == len(teams) - 1:
				output.write(str(teams[n][m]) + "\n")
			else:
				output.write(str(teams[n][m]) + " ")

output.close()