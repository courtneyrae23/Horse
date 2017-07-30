Caroline Kim, Courtney Pasco, Emily Pedersen, and Ruihan Zhao
5 December 2016
CS 170 Final Project Report

We implemented a greedy algorithm of going through the nodes and iteratively setting each of the nodes to be the starting node. When we assign a node as a start node, we look through all of its adjacent vertices. We follow this vertex up to three steps through the graph and then we pick the adjacent vertex that has the heaviest weighted 3-step path and add that vertex to our overall path. If a vertex has a lot of connections (more than 30), we then instead just pick that vertex rather than looking forward three steps. This is because a vertex with many children is more likely to produce a longer path. Finally, we assign that vertex as our new starting vertex and recurse, eventually finding one of the heaviest paths from the original start node up to a node that is no longer connected to any other edges. Once we have found this heaviest path from our start node, we delete that path from our original graph and randomly select one of the remaining nodes to be our new starting node if it has outgoing edges. If no remaining nodes have outgoing edges, then we randomly select from all the nodes remaining. Then we again run this algorithm to pick the heaviest path from this new start node on the remaining graph. We continue this step until there are no more remaining nodes in the graph. This leaves us with teams of horses that we calculated starting from the original vertex.  Since we are iteratively assigning all of our vertices to be the start node, and greedily searching for the potential maximum scores starting from that assigned start node, we keep track of a set of teams that produces the max score and return the teams. 

In terms of optimization, we calculated the optimal score of the graph as if all the nodes were connected and if in the process of recursively running our algorithm, we find a team’s score equaled the optimal score, we would terminate the program and return that team. This sped up our calculations for fully connected graphs. We also chose to first only consider nodes as potential start nodes if they had outgoing edges, which was helpful for sparse graphs.  Starting nodes without outgoing edges can only form a team of one horse, which for the goal of our algorithm can’t form a team that would maximize the total score of the graph. Finally, we included a brute force version of the algorithm for use when the graph is small enough (under 15 nodes). Computationally, this brute force algorithm is expensive, but it yields optimal results because it checks through every possible path and returns the maximum.  If graphs are larger than 15 vertices, we still run our greedy algorithm with the other optimizations instead. 

To run:  >> python horse.py

Input (as outlined in the spec):
• The first line contains an integer which is the number of vertices |V|
• The remaining |V| lines are the adjacency matrix, where adj[i][j] = 1 ⇐⇒ (i, j) is an edge. The entries of the matrix are separated by spaces.
• The diagonal entries of adj[i][j] contain the performance rating of the ith horse, which is an integer in [0,99]

Output (as outlined in the spec):
Solutions will be contained in a single output file, where the ith line is your solution to the ith instance. Each solution is represented a list of paths, each separated by a semicolon. The path is represented as a sequence of vertices, separated by spaces. For example, if the paths are (1,4,5) and (2,3,6), the output would be 1 4 5; 2 3 6.

To run our algorithm on the final inputs, please adjust the number of inputs and redirect the input to the cs170_final_inputs folder. 
