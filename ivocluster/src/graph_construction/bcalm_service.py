from os         import path
from subprocess import run

import logging

class BcalmService():

    def construct_dbg(short_read_files: list[str], outdir, threads):

        """
        Construction of a collapsed de bruijn graph from provided short reads using BCALM

        Args:
            short_read_files (list[str]): _description_
            outdir (_type_): _description_
            threads (_type_): _description_
        """

        short_reads_file = path.join(outdir, "bcalm.txt")

        with open(short_reads_file, "w") as srf:
            for f in short_read_files:
                if not (f==None):
                    print(f)
                    srf.write(f+"\n")

        print(f"bcalm -in {short_reads_file} -out-dir {outdir} -nb-cores {threads}")

        command = ["bcalm",
                "-in",
                short_reads_file,
                "-out-dir",
                outdir,
                "-nb-cores",
                str(threads)]
        
        run(command, check=True)