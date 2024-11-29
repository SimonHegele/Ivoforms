from abc        import ABC, abstractmethod
from itertools  import combinations
from numpy      import max, zeros
from os         import path
from time       import sleep
from typing     import Generator
from re         import compile

import logging

from src.io.file_services.buffered_writer   import BufferedWriter
from src.clustering.sequence_mapping_queue  import SequenceMappingQueue
    
class LongreadClusteringService():

    component_regex = compile(r"Component_(?P<COMPONENT>\d+)")
    contig_regey    = compile(r"Contig_(?P<CONTIG>\d+)")

    @classmethod
    def overlaps(cls, mapping1, mappings, t=3)->bool:
        """
        Determines if a mapping overlaps with any other mappings for at least t bases
        """
    
        for mapping2 in mappings:

            if int(mapping1["query_start"])<=int(mapping2["query_start"]):
                if int(mapping2["query_start"])+t<=int(mapping1["query_end"]):
                    return True
            if int(mapping2["query_start"])<=int(mapping1["query_start"]):
                if int(mapping1["query_start"])+t<=int(mapping2["query_end"]):
                    return True
                
        return False

    @classmethod
    def extract_best_non_overlapping_mappings(cls, mappings: list[dict])->list[dict]:

        best_non_overlapping_mappings = []

        while any(mappings):

            best_score   = max([int(m["alignment_quality"]) for m in mappings])
            best_mapping = [m for m in mappings if int(m["alignment_quality"])==best_score][0]

            if not cls.overlaps(best_mapping,best_non_overlapping_mappings):
                best_non_overlapping_mappings.append(best_mapping)
            
            mappings.remove(best_mapping)

        return best_non_overlapping_mappings
    
    @classmethod
    def extract_component_index(cls, mapping: dict)->str:

        return cls.component_regex.search(mapping["target_name"]).group("COMPONENT")
    
    @classmethod
    def extract_component_indices(cls, mappings: dict)->list[str]:

        return list(set([cls.extract_component_index(m) for m in mappings]))
    
    @classmethod
    def determine_cluster(cls, mappings: list[dict])->str:

        if any(mappings):
            mappings   = cls.extract_best_non_overlapping_mappings(mappings)
            components = cls.extract_component_indices(mappings)
            if len(components)==1:
                return components[0]
            else:
                return "potential_chimeras"
        else:
            return "unmapped"
        
    @classmethod   
    def get_contig_indices(cls, mappings: list[dict])->list[tuple[int,int]]:
        """
        Args:
            mappings (list[dict])

        Returns:
            list[tuple[int,int]]: A list of two-tuples
                                  (Component_index, Contig_index)
        """
        
        if any(mappings):
            mappings   = cls.extract_best_non_overlapping_mappings(mappings)
            return [cls.component_regex.search(m["target_name"]).group("CONTIG") for m in mappings]     
        else:
            return []

    @classmethod
    def cluster(cls, longreads: str, mappings: str, outdir: str):
        """
        Assign long reads to the files corresponding to the components of the assembly
        graph. Long reads and their corresponding mappings where different regions of the
        reads are mapped to different components are written to a separate file.

        Also keeps track of the frequency each time a long read maps to a contig.

        Args:
            longreads (str): path to a file with long reads
            mappings (str):  path to corresponding .paf file
            outdir (str):
            n (int):         number of components in the assembly graph
        """

        contig_frequencies = {}                                           

        with BufferedWriter(outdir, lines_per_file=40) as writer:

            progress = 0
            unmapped = 0

            for read, mappings in SequenceMappingQueue(longreads, mappings).queue():

                cluster   = cls.determine_cluster(mappings)

                if cluster == "unmapped":
                    unmapped += 1

                read_file = f"cluster_{cluster}.fasta"

                # for index in cls.get_contig_indices(mappings):

                #     if not index in contig_frequencies.keys():
                #         contig_frequencies[index]  = 1
                #     else:
                #         contig_frequencies[index] += 1

                writer.write_line(read_file, read["header"])
                writer.write_line(read_file, read["sequence"])

                progress += 1

                if progress%100_000==0:
                    logging.info(f"   {int(progress/1_000)}k long reads processed")
            
            logging.info(f"   {int(progress/1_000)}k long reads processed")
        
            return progress, unmapped, contig_frequencies