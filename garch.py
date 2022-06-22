from typing import Sequence
import numpy as np
from pyshgp.gp.genome import Genome, GenomeArchive
from pyshgp.gp.individual import Individual



def load_genome(path: str) -> Genome:
    individual = Individual.load(path)
    return individual.genome


def __subgenome(genome: Genome, subgenome_length: int) -> Genome:
    genome_length = len(genome)
    start = np.random.randint(0, genome_length-subgenome_length)
    return genome[start:start+subgenome_length]


def random_subgenome(genome: Genome, min_length: int = 1, max_length: int = 5) -> Genome:
    subgenome_length = np.random.randint(min_length, max_length+1)
    return __subgenome(genome, subgenome_length)


def divide_subgenome_part(genome: Genome, n_part: int) -> Sequence[Genome]:
    length = len(genome)
    subgenome_length = length // n_part
    if subgenome_length==0:
        return [Genome([i]) for i in genome]
    subgenomes = []
    count = 0
    cummulative_length = 0
    for i in range(0, length, subgenome_length):
        subgenomes.append(genome[i:i+subgenome_length])
        count += 1
        cummulative_length += subgenome_length
        if count == n_part-1:
            break
    subgenomes.append(genome[cummulative_length:])
    return subgenomes


def divide_subgenome_length(genome: Genome, length: int) -> Sequence[Genome]:
    subgenomes = []
    for i in range(0, len(genome), length):
        subgenomes.append(genome[i:i+length])
    return subgenomes


def genome_archive_random(
    genomes: Sequence[str],
    size: int,
    min_length: int,
    max_length: int
):
    subgenomes = []
    for genome_name in genomes:
        genome = load_genome(genome_name)
        while len(subgenomes) < size:
            subgenome = random_subgenome(genome, min_length, max_length)
            if subgenome not in subgenomes:
                subgenomes.append(subgenome)
    return GenomeArchive(subgenomes)


def genome_archive_part(
    genomes: Sequence[str],
    n_part: int = None,
    n_gene: int = None
):
    subgenomes = []
    for genome_name in genomes:
        genome = load_genome(genome_name)
        if n_part:
            subgenomes.extend(divide_subgenome_part(genome, n_part))
        if n_gene:
            subgenomes.extend(divide_subgenome_length(genome, n_gene))

    return GenomeArchive(subgenomes)