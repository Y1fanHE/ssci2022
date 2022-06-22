from sys import argv
from psb import program_synth as ps
from garch import genome_archive_part as gap


problem, search, npop, ngen, nproc, seed = argv[1:]
garch = gap(["small-or-large/1017.sol", "median/1010.sol"], n_part=5)


if __name__ == "__main__":

    est = ps(problem=problem,
             search=search,
             npop=int(npop),
             ngen=int(ngen),
             nproc=int(nproc),
             seed=int(seed),
             archive=garch,
             replacement_rate=0.0,
             adaptation_rate=0.0,
             savepop=f"{problem}/{seed}.hst")

    est.save(f"{problem}/{seed}.sol")
