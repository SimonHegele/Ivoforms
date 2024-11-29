from multiprocessing    import Pool
from os                 import listdir, mkdir, path
from subprocess         import run 

import logging

from src.clustering.longread_clustering_service     import LongreadClusteringService
from src.correction.spike_in_services               import Injector
from src.graph_component_analysis.assembly_graph    import AssemblyGraph
from src.graph_construction.bcalm_service           import BcalmService
from src.io.argument_parser                         import MyArgumentParser
from src.io.logging_setup                           import logging_setup
from src.io.file_services                           import utils
from src.mapping.minimap2_service                   import Minimap2Service
#from src.correction.spike_in_sevices                import Injector

def short_report(n_reads, n_unassigned, n_components, outdir):

    n_assigned = n_reads-n_unassigned

    p_reads      = 100
    p_assigned   = round(n_assigned/n_reads,3)*100
    p_unassigned = round(n_unassigned/n_reads,3)*100

    with open(path.join(outdir, "short_report.txt"),"w") as report:
        report.write(f"# longreads\t{n_reads}\t{p_reads}%\n")
        report.write(f"# assigned\t{n_assigned}\t{p_assigned}%\n")
        report.write(f"# unassigned\t{n_unassigned}\t{p_unassigned}%\n")
        report.write(f"# cluster\t{n_components}")

def main():

    args = MyArgumentParser().parse_args()

    logging_setup(args.loglevel, "ivocluster.log")

    # Initializing paths
    directory_longreads_binned    = path.join(args.outdir,"longreads_binned")
    directory_longreads_clustered = path.join(args.outdir,"longreads_clustered")
    directory_longread_mappings   = path.join(args.outdir,"longreads_mappings")
    directory_components          = path.join(args.outdir,"components")

    mkdir(args.outdir)
    mkdir(directory_longreads_binned)
    mkdir(directory_longreads_clustered)
    mkdir(directory_longread_mappings)
    mkdir(directory_components)

    logging.info("Ivoforms - Clustering started")
    
    ######################################################################################
    # STEP 1: ASSEMBLY GRAPH CONSTRUCTION                                                #
    ######################################################################################

    if args.graph == None:
        files = [f for f in [args.left, args.right, args.short] if f != None]
        logging.info(f"De bruijn construction from {files}")
        BcalmService().construct_dbg(files, args.outdir, args.threads)
        logging.info("Done")
        graph_format = "bcalm"
        graph_file   = "bcalm.unitigs.fa"
    else:
        graph_format = args.f
        graph_file   = args.graph

    ######################################################################################
    # STEP 1: ASSEMBLY GRAPH CONSTRUCTION                                                #
    ######################################################################################

    """XOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOX"""

    ######################################################################################
    # STEP 2: SEPARATING GRAPH COMPONENTS                                                #                                                
    ######################################################################################

    # Reading assembly graph
    logging.info(f"Loading assembly graph from: {graph_file}")
    graph_reader = utils.get_graph_reader(graph_format)
    graph_data   = graph_reader.read(graph_file)
    graph        = AssemblyGraph()
    graph.init_from(graph_data)
    logging.info(f"Done")

    # Writing components fasta
    logging.info("Writing components.fasta")
    number_of_components = graph.write_components(args.outdir)
    logging.info(f"#Components: {number_of_components}")
    logging.info("Done")

    ######################################################################################
    # STEP 2: SEPARATING GRAPH COMPONENTS                                                #                                                
    ######################################################################################

    """XOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOX"""

    ######################################################################################
    # STEP 3: MAPPING LONG READS TO THE COMPONENT GRAPH                                  #                                                
    ######################################################################################

    logging.info(f"Mapping long reads to assembly graph")
    Minimap2Service().map_longreads_to_contigs(args.long, 
                                               path.join(args.outdir,"components.fasta"),
                                               args.outdir,
                                               args.threads)
    logging.info(f"Done")
    
    ######################################################################################
    # STEP 3: MAPPING LONG READS TO THE COMPONENT GRAPH                                  #                                                
    ######################################################################################

    """XOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOX"""

    ######################################################################################
    # STEP 4: Clustering                                                                 #                                                
    ######################################################################################

    logging.info("Clustering")

    longread_files = sorted(listdir(directory_longreads_binned))
    longread_files = [path.join(directory_longreads_binned,f) for f in longread_files]
    mappings_files = sorted(listdir(directory_longread_mappings))
    mappings_files = [path.join(directory_longread_mappings,f) for f in mappings_files]

    n_reads            = 0
    n_unassigned       = 0
    contig_frequencies = []
        
    for i in range(args.threads):
        logging.info(f"   Bin {i+1} of {args.threads}")
        a, b, c = LongreadClusteringService().cluster(longread_files[i],
                                                      mappings_files[i],
                                                      directory_longreads_clustered)
        n_reads      += a
        n_unassigned += b
        contig_frequencies.append(c)

    logging.info("Done")

    short_report(n_reads,
                 n_unassigned,
                 number_of_components,
                 args.outdir)

    if not args.correct:
        logging.info("CLUSTERING COMPLETED")
        exit(0)

    ######################################################################################
    # STEP 4: Clustering                                                                 #                                                
    ######################################################################################

    """XOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOXOXOOXOXOXOXOXOXOXOXOXOX"""

    ######################################################################################
    # STEP 5: LONGREAD CORRECTION                                                        #                                                
    ######################################################################################

    logging.info("Correcting reads")

    directory_longreads_spiked = path.join(args.outdir,"longreads_spiked")

    mkdir(directory_longreads_spiked)
    
    Injector.inject(directory_components,
                    directory_longreads_clustered,
                    directory_longreads_spiked,
                    args.accuracy)

if __name__ == "__main__":
    main()