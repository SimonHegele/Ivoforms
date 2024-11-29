from networkx import Graph, connected_components
from os       import path

import logging

class AssemblyGraph(Graph):
    '''
    Networkx representation of assembly graphs.

    Here, the actual edges of the assembly graph are represented as nodes and vice versa
    '''

    def init_from(self, edges: list[dict]):

        for edge in edges:
            self.add_node(edge["id"], sequence=edge["sequence"])
            for neighbor in edge["neighbors"]:
                self.add_edge(edge["id"], neighbor)                                      

    def write_components(self, outdir):

        with open(path.join(outdir,"components.fasta"), "w") as components_file:

            n = 0

            for i, component in enumerate(connected_components(self)):

                with open(path.join(path.join(outdir,"components"), f"component_{i+1}.fasta"), "w") as component_file:

                    j = 1

                    for node in component:

                        components_file.write(f">Component_{i+1}_Contig_{j}"+"\n")
                        components_file.write(self.nodes[node]["sequence"]+"\n")
                        component_file.write(f">Component_{i+1}_Contig_{j}"+"\n")
                        component_file.write(self.nodes[node]["sequence"]+"\n")
                    
                        j += 1
                        n += 1

                        if n%10_000==0:
                            info = f"   Processed contigs: {n} of {self.number_of_nodes()}"
                            logging.info(info)

        info = f"   Processed contigs: {n} of {self.number_of_nodes()}"
        logging.info(info)

        return i