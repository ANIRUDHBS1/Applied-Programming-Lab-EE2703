import numpy
import sys
import networkx as nx
import time
g = nx.DiGraph()
name = input("Enter the name of the netlist including extension (.netlist)")
with open(name) as f :
    lines = f.readlines()
inputs = set()
ip = []
outputs = {}
for indline in lines :
    line = indline.split()
    if line[1] == 'inv' or line[1] == 'buf':
        i, o = line[2:]
        inputs.add(i)
        outputs[o] = line[1]
        g.add_edge(i,o)
    else:
        i1, i2, o = line[2:]
        inputs.add(i1)
        inputs.add(i2)
        outputs[o] = line[1]
        g.add_edge(i1,o)
        g.add_edge(i2, o)
for inp in inputs :
    if inp in outputs.keys() :
        continue
    else :
        ip.append(inp)
for inp in ip :
    g.nodes[inp]["gateType"] = "PI"
for out in outputs:
    g.nodes[out]["gateType"] = outputs[out]
n1 = list(nx.topological_sort(g))
for node in n1:
    g.nodes[node]['value'] = 0
with open("inputs.txt") as f:
     linesip = f.readlines()
l1 = linesip[0]
l2 = linesip[1:]
l1 = l1.split()
def AND(a, b):
    return a*b
def OR(a,b) :
    if a+b == 0 :
        return 0
    else :
        return 1
def XOR(a,b) :
    if (a==1 and b==0) or (a==0 and b==1):
        return 1
    else :
        return 0
def NOT(a):
    if a == 1:
        return 0
    else :
        return 1
def NOR(a,b):
    if a+b == 0:
        return 1
    else :
        return 0
def XNOR(a,b):
    if a==b:
        return 1
    else :
        return 0
def NAND(a,b):
    if a*b ==1 :
        return 0
    else :
        return 1
def BUF(a):
    return a
statetable = {}
for i in ip:
    statetable[i] = ['x']
for j in outputs :
    statetable[j] = ['x']
queue = []
state = []
def updatereturn(node):
    ip = list(g.predecessors(node))
    ips = []
    for i in ip:
        ips.append(g.nodes[i]['value'])
    if g.nodes[node]['gateType'] == "and2":
        return  AND(ips[0], ips[1]) 
    if g.nodes[node]['gateType'] == "or2" :
        return  OR(ips[0], ips[1]) 
    if g.nodes[node]['gateType'] == "xor2":
        return XOR(ips[0], ips[1]) 
    if g.nodes[node]['gateType'] == "inv":
        return  NOT(ips[0]) 
    if g.nodes[node]['gateType'] == "nor2":
        return NOR(ips[0], ips[1])
    if g.nodes[node]['gateType'] == "xnor2":
        return XNOR(ips[0], ips[1])
    if g.nodes[node]['gateType'] == "nand2":
        return NAND(ips[0], ips[1])
    if g.nodes[node]['gateType'] == "buf":
        return  BUF(ips[0]) 
def eventdrivensimulation():
    global queue, state
    while len(queue) != 0:
        n = queue[0]
        #print(n)
        ys = len(statetable[n])
        yprev = statetable[n][ys-1]
        for i in ip:
            y = len(statetable[i])
            statetable[i].append((statetable[i][y-1]))
        for j in outputs :
            y = len(statetable[j])
            statetable[j].append((statetable[j][y-1]))
        if g.nodes[n]['gateType'] == 'PI':
            if yprev != state[0] :
                l = list(g.successors(n))
                g.nodes[n]['value'] = state[0]
                statetable[n].pop()
                statetable[n].append(g.nodes[n]['value'])
                for ele in l :
                    queue.append(ele)
                queue.pop(0)
                state.pop(0)
            else :
                queue.pop(0)
                state.pop(0)
                statetable[n].pop()
                statetable[n].append(g.nodes[n]['value'])
        else :
            temp = updatereturn(n)
            state.append(temp)
            if yprev != state[0] :
                l = list(g.successors(n))
                g.nodes[n]['value'] = state[0]
                statetable[n].pop()
                statetable[n].append(g.nodes[n]['value'])
                for ele in l :
                    queue.append(ele)
                queue.pop(0)
                state.pop(0)
            else :
                queue.pop(0)
                state.pop(0)
                statetable[n].pop()
                statetable[n].append(g.nodes[n]['value'])
def solveEDS():
    global queue, state
    while len(l2) !=0 :
        for ele in l1:
            queue.append(ele)
        l21 = l2[0].split()
        for ele1 in l21:
            state.append(int(ele1))
        eventdrivensimulation()
        #for node in n1:
            #print (node + ":" + str(g.nodes[node]['value']))
        l2.pop(0)
        queue = []
        state = []
        #print()
begin = time.time()
solveEDS()
end = time.time()
print("Time taken is "+str(end-begin))
