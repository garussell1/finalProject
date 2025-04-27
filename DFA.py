dfa1 = {
    '0': {'a': '1', 'b': '0'},
    '1': {'a': '0', 'b': '1'}
}
start1 = '0'
accepts1 = {'1'}

dfa2 = {
    '0':{'a': '1', 'b': '0'},
    '1':{'a': '1', 'b': '2'},
    '2':{'a': '2', 'b': '0'}

}
start2 = '0'
accepts2 = {'0','1'}

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
