from exceptions import GCcontentError

from abc   import ABC, abstractmethod
from numpy import random

class Nucleotide_sequence(ABC):

    def info(self, ):
        return (f'Sequence:   {self.sequence}\nType:       {type(self)}\nLength:     {len(self.sequence)}')
    
    def __init__(self, sequence):

        self.sequence = sequence

    def to_fasta(self, file, id):

        with open(file, 'a') as fasta:
            fasta.write(">"+id)
            fasta.write(self.sequence)

    @abstractmethod
    def random_nucleotide(self) -> str:
        pass

class Transcript(Nucleotide_sequence):

    nucleotides = ['A','C','G','U']
    
    def random_nucleotide(self, gc_content=0.5):
        
        return random.choice([random.choice(['C', 'G']), random.choice(['A', 'U'])], p=[gc_content, 1-gc_content])

class Random_nucleotide_sequence(Nucleotide_sequence):

    def info(self):
        return (f'Sequence:   {self.sequence}\nType:       {type(self)}\nLength:     {len(self.sequence)}')
    
    def __init__(self, length: int, gc_content=0.5):

        if not ((0 <= gc_content) and (gc_content <= 1)):
            raise GCcontentError("GC-content must be in [0,1]")

        self.sequence = ''.join([self.random_nucleotide(gc_content) for i in range(length)])

class Random_rna_sequence(Random_nucleotide_sequence):

    nucleotides = ['A','C','G','U']

    def random_nucleotide(self, gc_content=0.5):
        
        return random.choice([random.choice(['C', 'G']), random.choice(['A', 'U'])], p=[gc_content, 1-gc_content])
    
class Random_dna_sequence(Random_nucleotide_sequence):

    nucleotides = ['A','C','G','T']

    def random_nucleotide(self, gc_content=0.5):
        
        return random.choice([random.choice(['C', 'G']), random.choice(['A', 'T'])], p=[gc_content, 1-gc_content])
    
class Random_exon(Random_dna_sequence):

    map = {'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A'}

    def transcribe(self):

        return ''.join([self.map[nucleotide] for nucleotide in self.sequence])