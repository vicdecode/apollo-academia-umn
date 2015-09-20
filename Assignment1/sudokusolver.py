import queue
"""This is where the problem is defined. Initial state, goal state and other information that can be got from the problem"""


class Problem(object):

    """
        My notes:
        - each 0 in the list is an empty node that needs to be solved.
        - need a build initial tree function of nodes that is called by init.
        - since each level is based on numbers, create nodes with value 1 -> length
        - goal test needs to check if the constraints are obeyed.
        - perhaps add a separate flag to enable pruning? (later)
    """

    def __init__(self, representation, goal=None):
        """This is the constructor for the Problem class. It specifies the initial state, and possibly a goal state, if there is a unique goal.  You can add other arguments if the need arises"""

        """
            Based on the set up initial is of type node. A Tree of Nodes.
            Goal is also a node tree.
        """
        self.representation = representation
        self.initial = 0
        self.goal = goal
        self.numberOfUnknowns = 0
        self.dimension = len(representation)  # dimension of sudoku

        for row in self.representation:
            # 0 represents an unknown number
            self.numberOfUnknowns += row.count(0)

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        # if state == 0:  #First Node in tree with no child
        return [x for x in range(1, self.dimension + 1)]

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        return action     #since we want a bunch of nodes

    def goal_test(self, collapsedState, depth):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        if depth != self.numberOfUnknowns:
            return False
            # print("not there yet")
        return False


class Node:

    """A node in a search tree. Contains:
        - a pointer to the parent (the node that this is a successor of, up one level) 
        - a pointer to the actual state for this node. 
        - the action that got us to this state

    If a state is arrived at by two paths, then there are two nodes with
    the same state.

    """

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action.
        Update the node parameters based on constructor values"""
        # update(self, state=state, parent=parent, action=action, depth=0)
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        # If depth is specified then depth of node will be 1 more than the
        # depth of parent
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        # List the nodes reachable in one step from this node.
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    # Makes a child node
    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        return Node(next, self, action)

    def collapse(self):
        if self.state is 0:
            return
        else:
            x = self.state
            self = self.parent
            return [x].append(self.collapse())

    def __str__(self):
        return "Node %i - Depth %i" % (self.state, self.depth)

# def printTree(parentNode):
#     print(parentNode)
#     print("|", end="")
#     for parentNode.child


def breadth_first_search(problem):
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node.state, node.depth):
        return node
    # Create a Queue to store all nodes of a particular level. Import
    # QueueClass()
    frontier = queue.Queue()
    frontier.put(node)

    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test
    # criteria are met
    while frontier:
        # Remove from frontier, for analysis
        node = frontier.get()
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes
        # here
        print(node)
        for child in node.expand(problem):
            print(" |--", child, "--", end="")
            # If child node meets Goal_Test criteria
            if problem.goal_test(child.collapse(), child.depth):
                return child
            # Add every new child to the frontier
            frontier.put(child)
            print("")
    # printTree(node)
    return None


def runApp():
    sudoku = [
        [1, 5, 0, 0, 4, 0],
        [2, 0, 0, 0, 5, 6],
        [4, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 4],
        [6, 3, 0, 0, 2, 0],
        [0, 2, 0, 0, 3, 1],
    ]
    # problemStartNode = Node(sudoku) -- This is done by BFS
    breadth_first_search(Problem(sudoku))

if(__name__ == '__main__'):
    runApp()