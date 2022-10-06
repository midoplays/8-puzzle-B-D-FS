from collections import deque
import random
from math import floor

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Puzzle():
    def __init__(self):
        ''' Generate random 8 puzzle '''
        # Generate a randomized list of unrepeated numbers from 1 to 8
        self.problem = random.sample(range(1, 9), 8)

        # Choose a random location for the blank and insert it into the list
        self.start = random.randint(0, 8)
        self.problem.insert(self.start, ' ')

        # Transform the list from 1D to 2D (3x3 list of lists)
        self.problem = [self.problem[x:x + 3] for x in range(0, len(self.problem), 3)]

        # Calculate the new position of blank
        self.start = (floor(self.start / 3), self.start % 3)
        if self.start[0] == 3:
            self.start = (2, self.start[1])

        self.solution = None

        # For Lab discussion purposes (since random problem turned out to take very long time):
        self.problem = [[1,2,3],[4,6,8],[7,5,' ']] # Easy problem for BFS
        # self.problem = [[1,2,4],[3,' ',5],[7,6,8]] # Intermediate for BFS
        # self.problem = [[1,2,3],[4,5,' '],[7,8,6]] # Easy problem for DFS (still choice dependent though, if it takes time, stop and run again)

        #for p in self.problem:
            #print(p)
        #print(self.start)


    def neighbours(self, state):
        blankpos = None
        for r in state:
            if ' ' in r:
                blankpos = (state.index(r), r.index(' '))

        row, col = blankpos
        candidates = {
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        }

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < 3 and 0 <= c < 3:
                result.append((action, (r, c)))
        print(result)
        print()
        return result

    def transition_model(self, state, action):
        newblankpos = (action[1][0], action[1][1])
        if action[0] == 'up':
            state[newblankpos[0] + 1][newblankpos[1]] = state[newblankpos[0]][newblankpos[1]]
        elif action[0] == 'down':
            state[newblankpos[0] - 1][newblankpos[1]] = state[newblankpos[0]][newblankpos[1]]
        elif action[0] == 'right':
            state[newblankpos[0]][newblankpos[1] - 1] = state[newblankpos[0]][newblankpos[1]]
        elif action[0] == 'left':
            state[newblankpos[0]][newblankpos[1] + 1] = state[newblankpos[0]][newblankpos[1]]

        state[newblankpos[0]][newblankpos[1]] = ' '
        '''for p in state:
            print(p)
            print()'''
        return state

    def goal_test(self, state):
        l = state[0] + state[1]
        l += state[2]
        if l.index(' ') == 8:
            l.pop(8)
            return l == sorted(l)
        elif l.index(' ') == 0:
            l.pop(0)
            return l == sorted(l)

    def DFS(self):
        # Keep track of number of explored states
        self.num_explored = 0

        # Initialize the frontier to the starting position
        start = Node(state=self.problem, parent=None, action=None)
        self.frontier = deque()
        self.frontier.append(start)

        # Initialize an empty explored set
        self.explored = []

        # Loop till solution found
        while True:

            # If frontier is empty and no solution was found yet, then no solution
            if not self.frontier:
                raise Exception("No solution")

            # Remove a node from frontier
            node = self.frontier.pop()
            self.num_explored += 1

            # Print node state
            for row in node.state:
                print(row)
            print()

            # If this node is the goal, we have a solution
            if self.goal_test(node.state):
                cells = []
                actions = []
                while node.parent is not None:
                    cells.append(node.state)
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                print("Solution found!")
                print(f"Number of explored states: {self.num_explored}")
                return self.solution

            # Add node to explored set
            self.explored.append(node.state)

            # Expand node, adding resulting nodes to frontier
            for action in self.neighbours(node.state):
                state = [node.state[0].copy(), node.state[1].copy(), node.state[2].copy()]
                state = self.transition_model(state=state, action=action)
                if state not in self.explored and not any(node.state == state for node in self.frontier):
                    child = Node(state=state, parent=node, action=action)
                    print(action)
                    self.frontier.append(child)

    def BFS(self):
        # Keep track of number of explored states
        self.num_explored = 0

        # Initialize the frontier to the starting position
        start = Node(state=self.problem, parent=None, action=None)
        self.frontier = deque()
        self.frontier.append(start)

        # Initialize an empty explored set
        self.explored = []

        # Loop till solution found
        while True:

            # If frontier is empty and no solution was found yet, then no solution
            if not self.frontier:
                raise Exception("No solution")

            # Remove a node from frontier
            node = self.frontier.popleft()
            self.num_explored += 1

            # Print node state
            for row in node.state:
                print(row)
            print()

            # If this node is the goal, we have a solution
            if self.goal_test(node.state):
                cells = []
                actions = []
                while node.parent is not None:
                    cells.append(node.state)
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                print("Solution found!")
                print(f"Number of explored states: {self.num_explored}")
                return self.solution

            # Add node to explored set
            self.explored.append(node.state)

            # Expand node, adding resulting nodes to frontier
            for action in self.neighbours(node.state):
                state = [node.state[0].copy(), node.state[1].copy(), node.state[2].copy()]
                state = self.transition_model(state=state, action=action)
                if state not in self.explored and not any(node.state == state for node in self.frontier):
                    child = Node(state=state, parent=node, action=action)
                    print(action)
                    self.frontier.append(child)



p = Puzzle()

# sol = p.DFS()
sol = p.BFS()


i = 0
for action in sol[0]:
    print()
    print(action)
    for state in sol[1][i]:
        print(state)
    i += 1
