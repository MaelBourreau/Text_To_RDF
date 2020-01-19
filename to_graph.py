import rdflib
import networkx as nx
import matplotlib.pyplot as plt
import sys

G_nx = nx.DiGraph()

def toString(url):
    return url.rsplit('/', 1)[-1]



try:
    file = sys.argv[1]
        #sentence = 'A rare black squirrel has become a regular visitor to a suburban garden'
except IndexError:
    print ("Enter the file name")
filehandle = open(file, "r")

for line in filehandle:
    [subject,predicate,obj] = line.split()
    G_nx.add_edge(toString(subject),toString(obj), r=toString(predicate))

pos = nx.spring_layout(G_nx, k=2)

print(G_nx.nodes())
print(G_nx.edges())

nx.draw(G_nx, pos, with_labels=True)
edge_labels = dict([((u, v,), d['r'])for u, v, d in G_nx.edges(data=True)])

nx.draw_networkx_edge_labels(G_nx,pos,edge_labels = edge_labels, alpha=1)

plt.savefig("mygraph.png")
