from exceptions           import ParameterError
from nucleotide_sequences import *

from abc          import ABC, abstractmethod
from copy         import deepcopy
from numpy.random import choice, randint, random

class Sequencer(ABC):

    @abstractmethod
    def sequence(nucleotide_sequence: Nucleotide_sequence) -> Nucleotide_sequence:
        pass

    def insertion(self, nucleotide_sequence: Nucleotide_sequence, i: int) -> None:

        nucleotide = choice(nucleotide_sequence.nucleotides)
        nucleotide_sequence.sequence = nucleotide_sequence.sequence[:i] + nucleotide + nucleotide_sequence.sequence[i:]

    def deletion(self, nucleotide_sequence: Nucleotide_sequence, i: int):

        nucleotide_sequence.sequence = nucleotide_sequence.sequence[:i] + nucleotide_sequence.sequence[i+1:]
 
    def substitution(self, nucleotide_sequence: Nucleotide_sequence, i: int) -> None:
        
        nucleotide = choice([nucleotide for nucleotide in nucleotide_sequence.nucleotides if nucleotide != nucleotide_sequence.sequence[i]])
        nucleotide_sequence.sequence = nucleotide_sequence.sequence[:i-1] + nucleotide + nucleotide_sequence.sequence[i:]
        
class Long_read_sequencer(Sequencer):

    def check_input(self, fragmentation_rate: float, substitution_rate: float, indel_rate: float):

        message = ''
        if not ((0 <= fragmentation_rate) and (fragmentation_rate <=1)):
            message += "fragmentation_rate must be from [0,1]"
        if not ((0 <= substitution_rate) and (substitution_rate <=1)):
            message += "substitution_rate must be from [0,1]"
        if not ((0 <= fragmentation_rate) and (fragmentation_rate <=1)):
            message += "substitution_rate must be from [0,1]"
        if message:
            raise ParameterError('\n'+message)

    def __init__(self, fragmentation_rate: float, substitution_rate: float, indel_rate: float):
        '''
        Parameters:
            fragmentation_rate (float), a value from [0,1].
            substitution_rate  (float), a value from [0,1].
            indel_rate         (float), a value from [0,1].
        '''

        self.check_input(fragmentation_rate, substitution_rate, indel_rate)

        self.fragmentation_rate = fragmentation_rate
        self.substitution_rate  = substitution_rate
        self.indel_rate         = indel_rate

    def fragment(self, nucleotide_sequence: Nucleotide_sequence) -> tuple:

        sequence_length             = len(nucleotide_sequence.sequence)

        if self.fragmentation_rate==0:

            return 0, sequence_length
        
        else:

            fragmentation_probabilities = []
            for _ in range(sequence_length):
                fragmentation_probabilities.append((1 - sum(fragmentation_probabilities)) * self.fragmentation_rate)
            fragmentation_probabilities[sequence_length-1] += 1 - sum(fragmentation_probabilities)

            fragment_length = choice(range(sequence_length), p=fragmentation_probabilities)
            fragment_start  = randint(0, sequence_length-fragment_length)
            fragment_end    = fragment_start + fragment_length

            nucleotide_sequence.sequence = nucleotide_sequence.sequence[fragment_start:fragment_end]

            return fragment_start, fragment_end
         
    def sequence_errors(self, nucleotide_sequence: Nucleotide_sequence) -> tuple:

        nucleotides = ["A", "C", "G", "U"]
        i = 0
        align_a = ""
        align_b = ""
        while i<len(nucleotide_sequence.sequence):
            #print(i)
            e = random()
            # no error
            if (e >= self.indel_rate + self.substitution_rate):
                align_a += nucleotide_sequence.sequence[i]
                align_b += nucleotide_sequence.sequence[i]
                i += 1
            # indel
            elif (e >= self.substitution_rate):
                if 0.5 > random():
                    self.insertion(nucleotide_sequence, i)
                    align_a += " "
                    align_b += nucleotide_sequence.sequence[i+1]
                    i += 2
                else:
                    align_a += nucleotide_sequence.sequence[i]
                    self.deletion(nucleotide_sequence, i)
                    align_b += " "
            # substitution
            else:
                align_a += nucleotide_sequence.sequence[i]
                self.substitution(nucleotide_sequence,i)
                align_b += nucleotide_sequence.sequence[i]
                i += 1
            
        return align_a, align_b

    def sequence(self, nucleotide_sequence: Nucleotide_sequence, verbose=True):

        read = deepcopy(nucleotide_sequence)

        fragment_start, fragment_end = self.fragment(read)

        align_a, align_b = self.sequence_errors(read)

        if verbose:

            sequence = nucleotide_sequence.sequence
            
            indent  = "".join([" " for _ in range(fragment_start)])
            matches = ''.join(["*" if align_a[i]==align_b[i] else " " for i in range(len(align_a))])

            print(sequence[:fragment_start] + align_a + sequence[fragment_end:])
            print(indent + matches)
            print(indent + align_b)
        
        return read