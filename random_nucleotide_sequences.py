from numpy import random

map = {'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A'}

class GCcontentError(Exception):
    pass

class Nucleotide_sequence():

    def info(self):
        return (f'Sequence:   {self.sequence}\nType:       {type(self)}\nLength:     {len(self.sequence)}')
    
    def __init__(self, sequence):

        self.sequence = sequence

class Transcript(Nucleotide_sequence):
    pass

class Random_nucleotide_sequence(Nucleotide_sequence):

    def info(self):
        return (f'Sequence:   {self.sequence}\nType:       {type(self)}\nLength:     {len(self.sequence)}')
    
    def __init__(self, length: int, gc_content=0.5):

        if not ((0 <= gc_content) and (gc_content <= 1)):
            raise GCcontentError("GC-content must be in [0,1]")

        self.sequence = ''.join([self.random_nucleotide(gc_content) for i in range(length)])

class Random_rna_sequence(Random_nucleotide_sequence):

    def random_nucleotide(self, gc_content=0.5):
        
        return random.choice([random.choice(['C', 'G']), random.choice(['A', 'U'])], p=[gc_content, 1-gc_content])
    
class Random_dna_sequence(Random_nucleotide_sequence):

    def random_nucleotide(self, gc_content=0.5):
        
        return random.choice([random.choice(['C', 'G']), random.choice(['A', 'T'])], p=[gc_content, 1-gc_content])
    
class Random_exon(Random_dna_sequence):

    def transcribe(self):

        return ''.join([self.map[nucleotide] for nucleotide in self.sequence])