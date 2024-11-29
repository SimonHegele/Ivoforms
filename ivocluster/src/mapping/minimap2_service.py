from multiprocessing import Pool
from os              import path, mkdir, listdir
from subprocess      import run

class Minimap2Service():

    def split_file(cls, file, outdir, n):

        command = ["seqkit",
                   "split2",
                   "-p",
                   str(n),
                   "-O",
                   outdir,
                   file]
        
        run(command, check=True)

    def build_index(cls, components, outdir, threads):

        command = ["minimap2",
                   "-x",
                   "splice",
                   "-t",
                   str(threads),
                   "-d",
                   path.join(outdir,"mm2.idx"),
                   components]
        
        run(command, check=True)

    def map_longreads_to_contigs(cls, longreads, components, outdir, threads):

        longreads_dir = path.join(outdir,"longreads_binned")
        mappings_dir  = path.join(outdir,"longreads_mappings")

        cls.build_index(components, outdir, threads)
        cls.split_file(longreads, longreads_dir, threads)

        commands = []
        files    = [path.join(longreads_dir, f) for f in sorted(listdir(longreads_dir))]

        for i, file in enumerate(files):

            commands.append(["minimap2",
                             "-x",
                             "splice",
                             "-t",
                             str(1),
                             "-o",
                             path.join(mappings_dir,f"lr2c_{i}.paf"),
                             path.join(outdir,"mm2.idx"),
                             file])
        
        with Pool(threads) as pool:
            pool.map(run, commands)

    @classmethod
    def map_longreads_all_vs_all(cls, longreads_file, outfile, threads):

        command = ["minimap2"]
