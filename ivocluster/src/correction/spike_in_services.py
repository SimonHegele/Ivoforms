from os         import listdir, path
from re         import compile

from src.io.file_services.fasta_file_service  import FastaFileService

class Injector():
    """
    The purpose of this class is to inject contig sequences to their respective clusters
    of long reads.
    """

    cluster_regex = compile(r"cluster_(?P<CLUSTER>\d+)")

    @classmethod
    def inject_spike_ins(cls,
                         directory_components: str,
                         directory_longreads: str,
                         directory_longreads_spiked: str,
                         accuracy: int):
        
        longread_files  = sorted(listdir(directory_longreads))
        longread_files  = [path.join(directory_longreads,f) for f in longread_files]

        for longread_file in longread_files:

            try:
                component      = cls.cluster_regex.search(longread_file).group("CLUSTER")
                component_file = path.join(directory_components,f"component_{component}.fasta")
                contigs        = list(FastaFileService().read(component_file))
                longreads      = list(FastaFileService().read(longread_file))

                FastaFileService().write(path.join(directory_longreads_spiked,
                                                path.basename(longread_file)),
                                                longreads)
                
                for _ in range(accuracy):

                    FastaFileService().write(path.join(directory_longreads_spiked,
                                                    path.basename(longread_file)),
                                                    contigs,
                                                    mode="a")
            except:
                _

class Extractor():

    def extract_spike_ins()