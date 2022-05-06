import networkx as nx
from script import Movie, Actor

net = open('history.txt', 'r')

G = nx.MultiGraph()

s = net.readline()
m, a = s.split(',')
M = Movie(m)
print(M)
G.add_node(M)

net.seek(0)
for line in net.readlines()[1:]:
    #print(line)
    m, a = line.split(',')
    #print(m)
    a = a.strip()
    #print(a)
    M = Movie(m); A = Actor(a)
    print(M)
    G.add_node(M)
    G.add_edge(list(G.nodes)[-1], list(G.nodes)[-2], A)

nx.write_graphml_lxml(G, 'sample.net')

