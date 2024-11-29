from argparse   import ArgumentParser
from os         import path, scandir

import logging

class MyArgumentParser(ArgumentParser):

    prog        =   "IVOFORMS - CLUSTERING"

    description =   """
                    Clustering of transcriptomic long read data by mapping them to the 
                    disconnected components of an assembly graph constructed from short
                    reads.

                    Additionally, the clustered long reads can be (self-) corrected using
                    Racon while spiked in contig sequences increase the accuracy of the
                    correction.
                    """

    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("long",
                          type=str,
                          help=".fasta or .fastq with long reads")
        self.add_argument("--graph",
                          type=str,
                          help="Assembly graph constructed from short reads (highly recommended)")
        self.add_argument("-f",
                          type=str,
                          help="Assembly graph file format",
                          default="fastg",
                          choices=["fastg", "bcalm"])
        self.add_argument("-l","--left",
                          type=str,
                          help=".fasta or .fastq with left reads from paired-end illumina RNAseq")
        self.add_argument("-r","--right",
                          type=str,
                          help=".fasta or .fastq of right reads from paired-endillumina RNAseq")
        self.add_argument("-s","--short",
                          type=str,
                          help=".fasta or .fastq with unpaired reads from illumina RNAseq")
        self.add_argument("-o","--outdir",
                          type=str,
                          help="output folder",
                          default="out")
        self.add_argument("-t", "--threads",
                          type=int,
                          help="Number of threads",
                          default=4)
        self.add_argument("--loglevel",
                          type=str,
                          help="Choose loglevel. Mostly logs information about the progess",
                          default="info",
                          choices=["debug","info","warning","error","critical"])
        
        # Arguments required only for correction
        self.add_argument("-c","--correct",
                          help="Set to self-correct clustered long reads with racon",
                          action="store_true")
        self.add_argument("-a",
                          "--accuracy",
                          type=int,
                          help="Choose how often each contig from the assembly graph is"
                               +"spiked in for the self-correction with racon.",
                          default=10)
        self.add_argument("--longread_type",
                          type=str,
                          default="ont")
        
    def check_input(self):

        reads = {"s": self.args.short,
                 "l": self.args.left,
                 "r": self.args.right,
                 "long": self.args.long}
         
        if not (reads["l"]==None) ^ (reads["r"]==None):
            raise Exception("Illumina read pair incomplete! Use both -l and -r parameters")
            
        if self.args.graph == None:
            logging.warning("You can run Ivoforms - clustering without providing a precomputed assembly graph but you really should not.")
            if (reads["s"]==None) and (reads["l"]==None) or (reads["r"]==None):
                raise Exception("Must provide assembly graph and/or short reads")
        else:
            if self.args.f==None:
                raise Exception("Must specify assembly graph format")  

    def parse_args(self):

        self.args   = super().parse_args()

        self.check_input()

        return self.args