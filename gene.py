from nucleotide_sequences import Transcript

from numpy.random import choice

class Gene:

    def __init__(self, exons, splice_model):
        '''
        Parameters:
            exons        (list),        a list of Random_exons
            splice_model (Splice_model) a
        '''

        self.exons        = exons
        self.splice_model = splice_model

    def transcribe(self) -> Transcript:
        '''
        Returns:
            (Transcript), a transcript generated randomly according to the splice model 
        '''
        # Choose first exon
        exon_index = choice([i for i in range(len(self.exons))], p=self.splice_model.p)
        transcript_sequence = self.exons[exon_index].sequence
        # Extend transcript sequence
        while (sum(self.splice_model.T[exon_index])>0):
            exon_index  = choice([i for i in range(len(self.exons))], p=self.splice_model.T[exon_index])
            transcript_sequence += self.exons[exon_index].sequence
        return Transcript(transcript_sequence)
    
    def path_extension(self, path: list) -> list:
        '''
        Parameters:
            path (list), a list of integers representing a continous path in the splice graph
        Recursively extends paths in the splice graph
        '''
        next_exons = [i for i in range(len(self.exons)) if self.splice_model.T[path[len(path)-1]][i]]
        if bool(next_exons):
            paths  = [path+[exon] for exon in next_exons]
            paths  = [self.path_extension(path) for path in paths]
            return paths
        else:
            return [path]
        
    def flatten_and_filter(self, input_list) -> list:
        '''
        Parameters:
            input_list (list), a nested list
        Returns:
            list, a list of non nested list
        '''
        result = []
        for item in input_list:
            if not isinstance(item[0], list):
                result.append(item)
            else:
                result.extend(self.flatten_and_filter(item))
        return result
  
    def all_paths(self) -> list:
        '''
        Returns:
            (list), a list of lists with integers, each representing a path through the splice graph
        '''
        paths = [[i] for i in range(len(self.splice_model.p)) if bool(self.splice_model.p[i])]
        paths = [self.path_extension(path) for path in paths]
        paths = self.flatten_and_filter(paths)
        return paths
    
    def all_isoforms(self) -> list:
        '''
        Returns:
            (list), a list with all transcripts that can be generated from the gene
        '''
        paths = self.all_paths()
        transcripts = [Transcript("".join([self.exons[exon_index].sequence for exon_index in path])) for path in paths]
        transcripts.sort(key=lambda transcript: len(transcript.sequence))
        return transcripts