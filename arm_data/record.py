import gzip
import pickle
import os
import numpy as np
from utils import get_error, isImprovedByReplacement


"""Record names"""
error_file = "error.csv"
anytime_file = "anytime.csv"


"""Problems, Methods, Seeds"""

problems = [ # Problems and short names
    "small-or-large-string"
]
problem_names = [
    "SLSTR"
]

methods = [ # Methods and names
    "r0.1-a0.5-kdps"
]
method_names_map = {
    "r0.0-a0.0": "PushGP",
    "r0.1-a0.0": "PushGP+EP+RRM",
    "r0.1-a0.5": "PushGP+EP+ARM",
    "r0.1-a0.5-h": "PushGP+HP+ARM",
    "r0.1-a0.5-kdps": "KDPS"
}
method_names = [method_names_map[i] for i in methods]

seeds = range( # Seeds
    1001, 1026
)


"""Backup files"""

os.system(f"cp {error_file} {error_file}.bp")
os.system(f"cp {anytime_file} {anytime_file}.bp")


"""Table heads"""

# with open(error_file, "w") as f: # write table head
#     f.write("Problem,Method,Seed,Period,Error,Success Rate\n")

# with open(anytime_file, "w") as f:
#     f.write("Problem,Method,Seed,Generation,Best Error,Average Genome Length,Improvement by Replacement\n")


"""Table contents"""

for p, problem in enumerate(problems): # data for every problem
    for m, method in enumerate(methods): # data for every method
        for seed in seeds: # data for every seed
            fname = problem + "-" + method + "/" + str(seed) + ".log" # log filename
            train_error, test_error = get_error(fname) # train, test error
            train_success = (train_error==0) # is train succeeded
            test_success = train_success and (test_error==0) # is test succeeded
            with open(error_file, "a") as f: # write record
                f.write(f"{problem_names[p]},{method_names[m]},{seed},Train,{train_error},{train_success}\n")
                f.write(f"{problem_names[p]},{method_names[m]},{seed},Test,{test_error},{test_success}\n")

for p, problem in enumerate(problems): # data for every problem
    for m, method in enumerate(methods): # data for every method
        for seed in seeds:
            fname = problem + "-" + method + "/" + str(seed) + ".log"
            with open(fname, "r") as log_file:
                for line in log_file:
                    if "GENERATION" in line:
                        tmp = line.replace(",","|").replace(":","|").split("|")
                        generation = tmp[4].strip()
                        min_error = tmp[6].replace("best=", "").strip()
                        avg_genome_length = tmp[11].replace("avg_genome_length=", "").strip()
                        improvement_by_replace = np.nan
                        with open(anytime_file, "a") as f:
                            f.write(f"{problem_names[p]},{method_names[m]},{seed},{generation},{min_error},{avg_genome_length},{improvement_by_replace}\n")

# for p, problem in enumerate(problems): # data for every problem
#     for m, method in enumerate(methods): # data for every method
#         for seed in seeds:
#             fname = problem + "-" + method + "/" + str(seed) + ".hst.gz"
#             with gzip.open(fname, "rb") as hst:
#                 generation = 1
#                 while True:
#                     try:
#                         pop = pickle.load(hst)
#                         min_error = np.min([ind.total_error for ind in pop])
#                         avg_genome_length = np.mean([len(ind.genome) for ind in pop])
#                         improvement_by_replace = np.mean([isImprovedByReplacement(ind) for ind in pop])
#                         with open(anytime_file, "a") as f:
#                             f.write(f"{problem_names[p]},{method_names[m]},{seed},{generation},{min_error},{avg_genome_length},{improvement_by_replace}\n")
#                     except EOFError:
#                         break
#                     generation += 1
#             print(f"Finish writing {problem} {method} {seed}")
