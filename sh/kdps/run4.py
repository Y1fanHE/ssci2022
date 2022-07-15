from sys import argv
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

    error = est.solution.total_error + est.test_error.sum()
    length = len(est.solution.genome)
    with open("summary.csv", "a") as f:
        f.write(f"{problem},{seed},{error},{length}\n")
