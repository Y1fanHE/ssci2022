from sys import argv
import numpy as np
from psb import program_synth as ps


problem, search, npop, ngen, nproc, seed = argv[1:]

if __name__ == "__main__":

    est = ps(problem=problem,
             search=search,
             npop=int(npop),
             ngen=int(ngen),
             nproc=int(nproc),
             seed=int(seed))

    est.save(f"{problem}/{seed}.sol")
