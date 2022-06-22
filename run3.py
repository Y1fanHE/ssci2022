from sys import argv
from pyshgp.gp.genome import Genome, GenomeArchive
from pyshgp.gp.individual import Individual
from psb import program_synth as ps


problem, search, npop, ngen, nproc, seed = argv[1:]
sl = Individual.load("small-or-large/1017.sol").genome
md = Individual.load("median/1010.sol").genome
garch = GenomeArchive([
    sl[:3], sl[3:5], sl[5:8], sl[8:10], sl[10:],
    md[:2], md[2:3], md[5:6], md[6:9], md[9:]
])


if __name__ == "__main__":

    est = ps(problem=problem,
             search=search,
             npop=int(npop),
             ngen=int(ngen),
             nproc=int(nproc),
             seed=int(seed),
             archive=garch,
             replacement_rate=0.1,
             adaptation_rate=0.5,
             savepop=f"{problem}/{seed}.hst")

    est.save(f"{problem}/{seed}.sol")
