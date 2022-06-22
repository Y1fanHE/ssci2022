import pandas as pd
import pickle as pc
from pyshgp.gp.individual import Individual
from pyshgp.gp.genome import GenomeArchive
from sys import argv
from garch import divide_subgenome_part as divide


last_problem = argv[1]

summary = pd.read_csv("summary.csv", header=None)
summary.columns=["prob","seed","err","len"]
success = summary[(summary.prob==last_problem) & (summary.err==0)]
best_seed_of_last_problem = success[success.len==success.len.min()].seed.values[0]

genome = Individual.load(f"{last_problem}/{best_seed_of_last_problem}.sol").genome

try:
    with open("subprogram.arch", "rb") as f:
        garch = pc.load(f)
        garch = garch.extend(divide(genome, 5))
except FileNotFoundError:
    garch = GenomeArchive(divide(genome, 5))

with open("subprogram.arch", "wb") as f:
    pc.dump(garch, f)