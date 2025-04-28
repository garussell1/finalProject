import sys
dfaFile1 = sys.argv[1]
dfaFile2 = sys.argv[2]

# file format:
# alphabet (separated by spaces)
# state names (separated by spaces)
# accepting states (separated by spaces)
# input outputting state (in pairs, separated by spaces. same order as states specified)
# example files are attached
# EX:
# 0 1
# S1 S2
# S1
# 0 S1 1 S2 (this would map to S1)
# 0 S2 1 S1 (this would map to S2)

dfa1 = {}
with open(dfaFile1) as f:
    alphabetLine = f.readline()
    alphabet = alphabetLine.split()
    states = f.readline()
    statesList = states.split()
    stateNames = statesList.copy()
    acceptingState1 = f.readline()
    accepts1 = acceptingState1.split()
    for x in range(0, len(statesList)):
        line = f.readline()
        currentState = line.split()
        statesList[x] = {}
        if len(currentState) % 2 != 0:
            print("ERROR! States are declared incorrectly for", dfaFile1, ". Please check comments for correct formatting.")
            sys.exit()
        for y in range(0, len(currentState),2):
                if currentState[y] not in alphabet:
                     print("ERROR!", currentState[y], "is not part of the specified alphabet. Please edit file ", dfaFile1, " for adjustments.")
                     sys.exit()
                if currentState[(y+1)] not in stateNames:
                     print("ERROR!", currentState[y+1], "is not part of the specified states. Please edit file ", dfaFile1, " for adjustments.")
                     sys.exit()
                statesList[x][currentState[y]] = currentState[(y + 1)]
        dfa1[stateNames[x]] = statesList[x]





dfa2 = {}
with open(dfaFile2) as f:
    alphabetLine2 = f.readline()
    alphabet2 = alphabetLine2.split()
    states2 = f.readline()
    statesList2 = states2.split()
    stateNames2 = statesList2.copy()
    acceptingState2 = f.readline()
    accepts2 = acceptingState2.split()
    for x in range(0, len(statesList2)):
        line = f.readline()
        currentState2 = line.split()
        # make a dictionary for each state first
        statesList2[x] = {}
        if len(currentState2) % 2 != 0:
            print("ERROR! States are declared incorrectly for", dfaFile2, ". Please check comments for correct formatting.")
            sys.exit()
        for y in range(0, len(currentState2),2):
                if currentState2[y] not in alphabet2:
                     print("ERROR!", currentState2[y], "is not part of the specified alphabet. Please edit file ", dfaFile2, " for adjustments.")
                     sys.exit()
                if currentState2[(y+1)] not in stateNames2:
                     print("ERROR!", currentState2[y+1], "is not part of the specified states. Please edit file ", dfaFile2, " for adjustments.")
                     sys.exit()
                statesList2[x][currentState2[y]] = currentState2[(y + 1)]
        dfa2[stateNames2[x]] = statesList2[x]

print("DFA1:")
print(dfa1)
print("DFA2:")
print(dfa2)
print("\n")


start1 = stateNames[0]
start2 = stateNames2[0]

def productConstruction(trans1, start1, accepts1, trans2, start2, accepts2):
    product_trans = {}
    product_accepts = set()
    product_start = (start1, start2)
    
    from collections import deque
    queue = deque([product_start])
    visited = set()
    while queue:
        state = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        
        s1, s2 = state
        product_trans[state] = {}
        for symbol in trans1[s1]:  
            new1 = trans1[s1][symbol]
            new2 = trans2[s2][symbol]
            new_state = (new1, new2)
            product_trans[state][symbol] = new_state
            queue.append(new_state)
        if s1 in accepts1 and s2 in accepts2:
            product_accepts.add(state)
    return product_trans, product_start, product_accepts

product_trans, product_start, product_accepts = productConstruction(
    dfa1, start1, accepts1,
    dfa2, start2, accepts2
)
from pprint import pprint
print("Transitions:")
pprint(product_trans)
print("\nStart State:")
print(product_start)
print("\nAccepting States:")
print(product_accepts)


# DFA visualization
# Creating a .dot file that displays the product DFA when uploaded to third-party visualizing tool
# Using "https://dreampuf.github.io/GraphvizOnline" as our third-party visualization tool
def createDotFile(product_trans, product_start, product_accepts, filename="product_dfa.dot"):
    with open(filename, "w") as f:

        # create digraph named DFA
        f.write("digraph DFA {\n")

        # left to right orientation
        f.write('    rankdir=LR;\n')
        
        # define "start spot"
        f.write('    start [shape=none, label="start"];\n')
        # arrow from "start spot" to the actual start state
        f.write(f'    start -> "{product_start}";\n')
        
        # define accepting states using results from product construction above
        f.write('    node [shape = doublecircle];\n')
        for state in product_accepts:
            f.write(f'    "{state}"\n')
        
        # define states and transitions using results from product construction above
        f.write('    node [shape = circle];\n')
        for state, transitions in product_trans.items():
            for symbol, next_state in transitions.items():
                f.write(f'    "{state}" -> "{next_state}" [label = "{symbol}"];\n')
        f.write("}")

createDotFile(product_trans, product_start, product_accepts)
print("\nDOT file has been created.\n" \
"Upload 'product_dfa.dot' to https://dreampuf.github.io/GraphvizOnline to view product DFA.")
