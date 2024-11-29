from setuptools import setup

setup(
    name        = 'ivocluster',
    version     = '0.1',
    description = "".join([ 'A python command line tool for the short read assembly ',
                                    'graph guided clustering of sequence reads for hybrid',
                                    'transcriptome assembly']),
    author      = 'Simon Hegele',
    packages    = ['src',
                   'src.clustering',
                   'src.correction',
                   'src.graph_component_analysis',
                   'src.graph_construction',
                   'src.io',
                   'src.io.file_services',
                   'src.mapping',
                   ],

    install_requires = ['numpy==1.26.4',
                        'networkx==3.3']
)