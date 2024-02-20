from exceptions import ParameterError

from networkx import DiGraph, draw, is_directed_acyclic_graph, is_weakly_connected

class Splice_model:

    def set_graph(self):

        n = len(self.T)
        self.graph = DiGraph()
        self.graph.add_nodes_from([f"exon {i}" for i in range(n)])
        self.graph.add_edges_from([(f"exon {i}", f"exon {j}") for i in range(n) for j in range(n) if self.T[i][j]])

    def check_input(self):

        message = ""

        if not sum(self.p)==1:
            message += 'p is not a probability vector!\n'

        if not len(self.p)==len(self.T):
            message += 'Length of p and number of lines in T do not match\n'
            
        if not is_weakly_connected(self.graph):
            message += 'Splice graph is not connected\n'
            
        if not is_directed_acyclic_graph(self.graph):
            message += 'Splice graph is not acyclic\n'

        t = [i for i in range(len(self.T)) if not len(self.T[i])==len(self.p)]
        if t:
            message += f'Length of lines {t} do not match the length of p'

        if len(message):
            raise ParameterError('\n'+message)

    def __init__(self, p, T):

        self.p = p
        self.T = T
        self.set_graph()
        self.check_input()

    def plot_graph(self, axes, name='Splice graph'):

        axes.set_ylim((-1,0.5))
        axes.set_title(name, fontweight='bold', fontsize=20)
        node_positions = {f"exon {i}": (i, 0) for i in range(len(self.T))}
        draw(self.graph, pos=node_positions, node_size=2500, connectionstyle='angle,angleA=-30,angleB=45', ax=axes, with_labels=True)