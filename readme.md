# Ivoforms

A collection of commandline tools for hybrid transcriptome assembly.
    
--------------------------------------------------------------------

## Installation

### Anaconda

**TODO**

### Installing Ivoforms manually

**Requirements**

- Minimap2 (https://github.com/lh3/minimap2)
- SeqKit (https://github.com/shenwei356/seqkit)
- Racon (https://github.com/isovic/racon)
- Python (>=3.6)
- Numpy
- Networkx

**TODO**

## 1. Ivocluster

Short read assembly graph guided partitioning of long read data.

The driving idea here is, that components of an assembly graph<br>
constructed from short reads should each correspond to the isoforms<br>
of either a single gene or a group of genes that share parts of their<br>
sequence. By mapping both long reads to the assembly graph they can<br>
seperated into smaller clusters. This can greatly improve the speed<br>
of a downstream long read assembly or correction methods that would<br>
require an all-versus-all mapping.

### 1.1. Usage

**TODO**

### 1.2. Algorithm / Workflow:

1. **Assembly graph construction**
   Options:
   a) Provide prcomputed assembly graph from SPAdes in .fastg-format
   b) Provide short reads and Ivocluster will construct a compressed<br>
      de Bruijn graph.
   Using a precomputed assembly graph should be preferred as it is<br>
   expected to contain less sequenecing artifacts and usually have<br>
   a less complex structure which makes Ivocluster a lot faster and<br>
   posibly more accurate.
2. **Separation of the non connected components of the assembly graph**
   By parsing the data from the previous step to a networkx.Graph<br>
   object, it's components can be separated from each other. The contig<br>
   sequences are written to a new fasta file where the header of each<br>
   entry shows the index of the corresponding graph component.
3. **Mapping longreads to the assembly graph**
   The long reads are mapped to the contigs of the assembly graph<br>
   using Minimap2.
   Multithreading:
   Unfortunately, mapping must be performed using only a single thread<br>
   in order to guarantee, that mappings are reported in the same order<br>
   as their corresponding longreads appear in their file.<br>
   However, multiple threads can be used for the construction of the<br>
   index. By using SeqKit to split the longreads to smaller files first<br>
   and mapping each of them separately, multiple threads can be utilized.<br>
   Since each thread has to load the index of the assembly graph, which<br>
   is often sevaral gigabytes large. Using many threads will therefore<br>
   eat your RAM like a bachelor student whose grandma pays for the<br>
   all-you-can-eat buffet.
4. **Assigning long reads**
   The SequenceMappingQueue allows to sequentially iterate through all<br>
   long reads and their corresponding mappings to the assembly graph.<br>
   For each longread and it's reported mappings the a greedy heuristic<br>
   attempts to find a set of longread to contig mappings where the<br>
   individual mappings do not overlap and have the highest possible combined<br>
   alignment score.
   The longread then get assigned to the cluster corresponding to the<br>
   component of the assembly graph with the best set of non overlapping<br>
   mappings.<br>
   Longreads that could not be mapped to the assembly graph are stored<br>
   in a separate file. Similarly, longreads were different regions map<br>
   to different components of the assembly graph are also written to
   a separate file<br>
   *Why could that happen?*
   1. Longreads are chimeras, transcript fragments unintentionally fused<br>
      together.
   2. Longreads cover transcriptomic regions that have insufficient short<br>
      read coverage which leads to graph components breaking apart.
   *What will Ivocluster do in cases like this?*
    Nothing.<br>
    Ideally, a statistical analysis would determine which of the two cases<br>
    applies. For case 1, longreads would be discarded and for case 2 the<br>
    corresponding read clusters would be merged and the longreads added.<br>
    I will implement this once this happens.

### Known issues, limitations, and further plans

**Issues**
- Currently the SequenceMappingQueue loses a single read

**Limitations**
- Multithreading: Depending on the size of the assembly graph a lot of RAM
                  is required per thread

**Future plans**

Further plans (other than fixing known issues) sorted by priority:

1. Support for assembly graphs in GFA-format
   (GFA is probably the most used file format for assembly graphs<br>
   and would allow to use a wide variety of tools for the construction<br>
   of the sort read assembly graph)
2. Improving multithreading
   (The user could provide any number of threads to be used for the<br>
   construction of the Minimap2 index while Ivocluster would limit the<br>
   number of threads used for the mapping according to the available RAM<br>
   and the size of the index and the long read file.
3. Clustering short read data.
4. Include construction of an actual assembly graph from user provided
   short reads.
5. Support for different mapping tools or user provided alignment files

## 2. Ivocorrect

"Hybrid self-correction" of clustered longreads with spike-in contigs<br>
using Minimap2 and Racon.

### 2.1 Usage

### 1.2. Algorithm / Workflow:

1. Spiking longread clusters with the contigs from the corresponding<br>
   components of short read assembly graph at a user defined rate.
2. All-versus-all mapping with Minimap2
3. Self-correction with Racon
4. Removing spike-in contigs from the files of corrected long-reads.
                        
