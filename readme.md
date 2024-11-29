Ivoforms

A collection of commandline tools for hybrid transcriptome assembly
    
-------------------------------------------------------------------

Ivoforms - Clustering

Short read assembly graph guided partitioning of long read data.

The driving idea here is, that components of an assembly graph constructed from short
reads should each correspond to either a single gene or a group of genes that share parts
of their sequence. By mapping both long and short reads to the assembly graph we can
separate them into smaller clusters of reads that can be assembled independently of each
other.

Overview:
1.  Assembly graph construction:
    An assembly graph is constructed from short reads or provided by the user.
2.  Assembly graph components:
    Separation of components of the assembly graph
3.  Mapping
    Mapping between reads and the components of the assembly graph
4.  Clustering of the reads:
    Clustering of reads based on the components they map to.
    
In more detail:
1.  The first step is the construction of an assembly graph.
    Option a): Providing a precomputed assembly graph (recommended)
    Assembly graphs in .fastg (from SPAdes) format can be provided.
    Support for the more common .gfa format will be comming soon.
    Option b): Computation of a compressed de Bruijn graph (discouraged)
    This tool can use BCALM to compute a compressed Bruijn graph from provided short reads.
    I highly recommend to provide a precomputed assembly graph in.fastg format from SPAdes.
    I will definitely add support for .gfa format since it is the most common format.
    Alternatively, a compressed de Bruijn graph is computed from the user provided short
    reads. So far this graph is not edited further.
    The editing operations that transform a de Bruijn graph to an assembly graph account
    for sequencing errors and decrease the complexity of the graphs structur. This 
    increases the of speed of the clustering. 
2.  The second step is the separation of the assembly graph into it's disconnected
    components.
    A .fasta-file containing all unitig sequences is generated. The header of each 
    sequence will clearly indicate the component it belongs to. 
3.  Mapping long reads to the contigs of the assembly graph.
    The split read mapping is facilitated using minimap2.
    Using minimap2 with only on thread has the great adventage that mappings are reported
    in the same order as the query sequences which is important for step 4. In order to be
    able to use several CPU cores at the same time, the reads are divided evenly between
    several files. Minimap2 is then started for each of them seperately.
4.  
5.  The error correction is a self-correction with Racon. In order to take still take 
    advantage of the higher accuracy in short reads, for each cluster the contigs are
    spiked in before and extraced after the correction step. 

TODO:
1. Adding .gfa support
2. Construction of an actual assembly graph
3. Adding support of different mapping tools or user provided .sam-files
4. Use seqkit or similar tool for read binning (probably much faster)                     Done
5. Clustering short read data
6. Implement cluster
7. Prevent last read to be lost by the read mapping queue
