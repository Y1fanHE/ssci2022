import string
import numpy as np
import pandas as pd
import time
from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.config import PushConfig
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.types import Char, IntVector, FloatVector, StrVector


class _PSB1:

    def __init__(self, name, edge, rand, test, root="psb", seed=None):
        self.edge_path = root + "/" + name + "/" + name + "-edge.json"
        self.rand_path = root + "/" + name + "/" + name + "-random.json"
        self.edg = edge
        self.rnd = rand
        self.tst = test
        self.seed = seed

    def process_type(self, dat):
        return dat

    @property
    def train(self):
        edge = pd.read_json(self.edge_path,
                            orient="records",
                            lines=True,
                            precise_float=True).sample(self.edg,
                                                       replace=False,
                                                       random_state=self.seed,
                                                       ignore_index=True)
        rand = pd.read_json(self.rand_path,
                            orient="records",
                            lines=True,
                            precise_float=True).sample(self.rnd,
                                                       replace=False,
                                                       random_state=self.seed,
                                                       ignore_index=True)
        dat = pd.concat([edge, rand], ignore_index=True)
        dat = self.process_type(dat)

        inputs = []
        outputs = []
        for col in dat.columns:
            if "input" in col:
                inputs.append(col)
            else:
                outputs.append(col)
        inp, out = dat[inputs], dat[outputs]
        return inp, out

    @property
    def test(self):
        dat = pd.read_json(self.rand_path,
                           orient="records",
                           lines=True,
                           precise_float=True).sample(self.tst,
                                                      replace=False,
                                                      random_state=self.seed+1000,
                                                      ignore_index=True)

        dat = self.process_type(dat)

        inputs = []
        outputs = []
        for col in dat.columns:
            if "input" in col:
                inputs.append(col)
            else:
                outputs.append(col)
        inp, out = dat[inputs], dat[outputs]
        return inp, out


# PSB1 Problems


class Checksum(_PSB1):

    def __init__(self, name="checksum", edge=106, rand=194, test=2000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1000
        self.max_genome_size = 3200
        self.initial_genome_size = (80, 400)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=1500)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "stdout"}),
            literals=["Check sum is ", Char(" "), 64],
            erc_generators=[self.random_integer_128, self.random_char_visible]
        )

    def random_integer_128(self):
        return np.random.randint(-128,129)

    def random_char_visible(self):
        visible = string.digits + string.ascii_letters + string.punctuation + "\n\t"
        return Char(np.random.choice(visible))


class CollatzNumbers(_PSB1):

    def __init__(self, name="collatz-numbers", edge=16, rand=184, test=2000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1000000
        self.max_genome_size = 2400
        self.initial_genome_size = (60, 300)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=15000)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "float", "bool"}),
            literals=[0, 1],
            erc_generators=[self.random_integer_100]
        )

    def random_integer_100(self):
        return np.random.randint(-100,101)


class CompareStringLengths(_PSB1):

    def __init__(self, name="compare-string-lengths", edge=22, rand=78, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1
        self.max_genome_size = 1600
        self.initial_genome_size = (40, 200)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=3,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "str"}),
            literals=[],
            erc_generators=[self.random_boolean]
        )

    def random_boolean(self):
        return np.random.choice([True, False])


class CountOdds(_PSB1):

    def __init__(self, name="count-odds", edge=32, rand=168, test=2000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1000
        self.max_genome_size = 2000
        self.initial_genome_size = (50, 250)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=1500)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "vector_int"}),
            literals=[0,1,2],
            erc_generators=[self.random_integer_1000]
        )

    def random_integer_1000(self):
        return np.random.randint(-1000, 1001)

    def process_type(self, dat):
        dat["input1"] = [IntVector(item) for item in dat.input1]
        return dat


class Digits(_PSB1):
    def __init__(self, name="digits", edge=15, rand=85, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 1200
        self.initial_genome_size = (30, 150)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "stdout"}),
            literals=[Char("\n")],
            erc_generators=[self.random_integer_10]
        )

    def random_integer_10(self):
        return np.random.randint(-10, 10)


class DoubleLetters(_PSB1):

    def __init__(self, name="double-letters", edge=32, rand=68, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 3200
        self.initial_genome_size = (80, 400)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=1600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "stdout"}),
            literals=[Char("!")],
            erc_generators=[]
        )


class EvenSquares(_PSB1):

    def __init__(self, name="even-squares", edge=17, rand=83, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 1600
        self.initial_genome_size = (40, 200)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=2000)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "stdout"}),
            literals=[],
            erc_generators=[]
        )


class ForLoopIndex(_PSB1):

    def __init__(self, name="for-loop-index", edge=10, rand=90, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 1200
        self.initial_genome_size = (30, 150)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=3,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "stdout"}),
            literals=[],
            erc_generators=[]
        )


class Grade(_PSB1):

    def __init__(self, name="grade", edge=41, rand=159, test=2000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 1600
        self.initial_genome_size = (40, 200)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=800)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=5,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "str", "stdout"}),
            literals=["Student has a ", " grade.", "A", "B", "C", "D", "F"],
            erc_generators=[self.random_integer_100]
        )

    def random_integer_100(self):
        return np.random.randint(0, 101)


class LastIndexOfZero(_PSB1):

    def __init__(self, name="last-index-of-zero", edge=72, rand=78, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1000000
        self.max_genome_size = 1200
        self.initial_genome_size = (30, 150)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "vector_int"}),
            literals=[0],
            erc_generators=[]
        )

    def process_type(self, dat):
        dat["input1"] = [IntVector(item) for item in dat.input1]
        return dat


class Median(_PSB1):

    def __init__(self, name="median", edge=0, rand=100, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1
        self.max_genome_size = 800
        self.initial_genome_size = (20, 100)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=200)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=3,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "stdout"}),
            literals=[],
            erc_generators=[self.random_integer_100]
        )

    def random_integer_100(self):
        return np.random.randint(-100, 101)

    def process_type(self, dat):
        dat["output1"] = [str(item) for item in dat.output1]
        return dat


class MirrorImage(_PSB1):

    def __init__(self, name="mirror-image", edge=23, rand=77, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1
        self.max_genome_size = 1200
        self.initial_genome_size = (30, 150)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=2,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "vector_int"}),
            literals=[],
            erc_generators=[self.random_boolean]
        )

    def random_boolean(self):
        return np.random.choice([True, False])

    def process_type(self, dat):
        dat["output1"] = [IntVector(item) for item in dat.output1]
        dat["output2"] = [IntVector(item) for item in dat.output2]
        return dat


class NegativeToZero(_PSB1):

    def __init__(self, name="negative-to-zero", edge=17, rand=183, test=2000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 2000
        self.initial_genome_size = (50, 250)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=1500)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "vector_int"}),
            literals=[0, IntVector()],
            erc_generators=[]
        )

    def process_type(self, dat):
        dat["input1"] = [IntVector(item) for item in dat.input1]
        dat["output1"] = [IntVector(item) for item in dat.output1]
        return dat


class NumberIO(_PSB1):

    def __init__(self, name="number-io", edge=0, rand=25, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 1e-04
        self.penalty = 5000
        self.max_genome_size = 800
        self.initial_genome_size = (20, 100)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=200)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=2,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "float", "stdout"}),
            literals=[],
            erc_generators=[self.random_integer_100, self.random_float_100]
        )

    def random_integer_100(self):
        return np.random.randint(-100, 101)

    def random_float_100(self):
        return np.random.uniform(-100, 100)

    def process_type(self, dat):
        dat["output1"] = [str(item) for item in dat.output1]
        return dat


class PigLatin(_PSB1):

    def __init__(self, name="pig-latin", edge=33, rand=167, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 4000
        self.initial_genome_size = (100, 500)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=2000)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "stdout"}),
            literals=["ay", Char(" "), Char("a"), Char("e"), Char("i"), Char("o"), Char("u"), "aeiou"],
            erc_generators=[self.random_char_visible, self.random_input_20]
        )

    def random_char_visible(self):
        visible = string.digits + string.ascii_letters + string.punctuation + "\n\t"
        return Char(np.random.choice(visible))

    def random_input_20(self):
        length = np.random.randint(0, 21)
        return self._input(length)

    def _input(self, length):
        lower = string.ascii_lowercase
        tmp = []
        for _ in range(length):
            if np.random.random() < 0.2:
                tmp.append(" ")
            else:
                l = lower[np.random.randint(0,len(lower))]
                tmp.append(l)
        s = "".join(tmp)
        tmp_lst = s.split(" ")
        tmp_lst_ = []
        for item in tmp_lst:
            if item != "":
                tmp_lst_.append(item)
        s = " ".join(tmp_lst_)
        return s


class ReplaceSpaceWithNewline(_PSB1):

    def __init__(self, name="replace-space-with-newline", edge=30, rand=70, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 3200
        self.initial_genome_size = (80, 400)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=1600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "stdout"}),
            literals=[Char(" "), Char("\n")],
            erc_generators=[self.random_char_visible, self.random_input_20]
        )

    def random_char_visible(self):
        visible = string.digits + string.ascii_letters + string.punctuation + "\n\t"
        return Char(np.random.choice(visible))

    def random_input_20(self):
        length = np.random.randint(0, 21)
        return self._input(length)

    def _input(self, length):
        visible = string.digits + string.ascii_letters + string.punctuation
        tmp = []
        for _ in range(length):
            if np.random.random() < 0.2:
                tmp.append(" ")
            else:
                l = visible[np.random.randint(0,len(visible))]
                tmp.append(l)
        s = "".join(tmp)
        return s


class ScrabbleScore(_PSB1):

    def __init__(self, name="scrabble-score", edge=50, rand=150, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1000
        self.max_genome_size = 4000
        self.initial_genome_size = (100, 500)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=2000)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "vector_int"}),
            literals=[IntVector(self.scrabble_vector)],
            erc_generators=[]
        )

    @property
    def scrabble_vector(self):
        vec = [0] * 127
        letter_score = [1, 3, 3, 2, 1,
                        4, 2, 4, 1, 8,
                        5, 1, 3, 1, 1,
                        3, 10, 1, 1, 1,
                        1, 4, 4, 8, 4,
                        10]

        for i, score in enumerate(letter_score):
            vec[i+65] = vec[i+97] = score
        return vec


class SmallOrLarge(_PSB1):

    def __init__(self, name="small-or-large", edge=27, rand=73, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 800
        self.initial_genome_size = (20, 100)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=300)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "str", "stdout"}),
            literals=["small", "large"],
            erc_generators=[self.random_integer_10000]
        )

    def random_integer_10000(self):
        return np.random.randint(-10000, 10001)


class Smallest(_PSB1):

    def __init__(self, name="smallest", edge=5, rand=95, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1
        self.max_genome_size = 800
        self.initial_genome_size = (20, 100)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=200)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=4,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "stdout"}),
            literals=[],
            erc_generators=[self.random_integer_100]
        )

    def random_integer_100(self):
        return np.random.randint(-100, 101)

    def process_type(self, dat):
        dat["output1"] = [str(item) for item in dat.output1]
        return dat


class StringDifferences(_PSB1):

    def __init__(self, name="string-differences", edge=30, rand=170, test=2000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 4000
        self.initial_genome_size = (100, 500)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=2000)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=2,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "stdout"}),
            literals=[Char(" "), Char("\n")],
            erc_generators=[self.random_integer_10]
        )

    def random_integer_10(self):
        return np.random.randint(-10, 11)


class StringLengthsBackwards(_PSB1):

    def __init__(self, name="string-lengths-backwards", edge=10, rand=90, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 1200
        self.initial_genome_size = (30, 150)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "str", "vector_str", "stdout"}),
            literals=[],
            erc_generators=[self.random_integer_100]
        )

    def random_integer_100(self):
        return np.random.randint(-100, 101)

    def process_type(self, dat):
        dat["input1"] = [StrVector(item) for item in dat.input1]
        return dat


class SumOfSquares(_PSB1):

    def __init__(self, name="sum-of-squares", edge=6, rand=44, test=100, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1000000000
        self.max_genome_size = 1600
        self.initial_genome_size = (40, 200)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=4000)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool"}),
            literals=[0, 1],
            erc_generators=[self.random_integer_100]
        )

    def random_integer_100(self):
        return np.random.randint(-100, 101)


class SuperAnagrams(_PSB1):

    def __init__(self, name="super-anagrams", edge=30, rand=170, test=2000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1
        self.max_genome_size = 3200
        self.initial_genome_size = (80, 400)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=1600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=2,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "bool", "char", "str"}),
            literals=[],
            erc_generators=[self.random_boolean, self.random_char_visible, self.random_integer_1000]
        )

    def random_boolean(self):
        return np.random.choice([True, False])

    def random_char_visible(self):
        visible = string.digits + string.ascii_letters + string.punctuation + "\n\t"
        return Char(np.random.choice(visible))

    def random_integer_1000(self):
        return np.random.randint(-1000, 1001)


class Syllables(_PSB1):

    def __init__(self, name="syllables", edge=17, rand=83, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 3200
        self.initial_genome_size = (80, 400)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=1600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "stdout"}),
            literals=["The number of syllables is ", "aeiouy", Char("a"), Char("e"), Char("i"), Char("o"), Char("u"), Char("y")],
            erc_generators=[self.random_char_visible, self.random_input_20]
        )

    def random_char_visible(self):
        visible = string.digits + string.ascii_letters + string.punctuation + "\n\t"
        return Char(np.random.choice(visible))

    def random_input_20(self):
        length = np.random.randint(0, 21)
        return self._input(length)

    def _input(self, length):
        letters = string.digits + string.ascii_lowercase + string.punctuation + " "
        tmp = []
        for _ in range(length):
            if np.random.random() < 0.2:
                l = np.random.choice(["a", "e", "i", "o" ,"u", "y"])
            else:
                l = letters[np.random.randint(0, len(letters))]
            tmp.append(l)
        s = "".join(tmp)
        return s


class VectorAverage(_PSB1):

    def __init__(self, name="vector-average", edge=10, rand=240, test=2550, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 1e-03
        self.penalty = 1000000
        self.max_genome_size = 1600
        self.initial_genome_size = (40, 200)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=800)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "float", "vector_float"}),
            literals=[],
            erc_generators=[]
        )

    def process_type(self, dat):
        dat["input1"] = [FloatVector(item) for item in dat.input1]
        return dat


class VectorsSummed(_PSB1):

    def __init__(self, name="vectors-summed", edge=15, rand=135, test=1500, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1000000000
        self.max_genome_size = 2000
        self.initial_genome_size = (50, 250)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=1500)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=2,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "vector_int"}),
            literals=[IntVector()],
            erc_generators=[self.random_integer_1000]
        )

    def random_integer_1000(self):
        return np.random.randint(-1000, 1001)

    def process_type(self, dat):
        dat["input1"] = [FloatVector(item) for item in dat.input1]
        dat["input2"] = [FloatVector(item) for item in dat.input2]
        dat["output1"] = [FloatVector(item) for item in dat.output1]
        return dat


class WallisPi(_PSB1):

    def __init__(self, name="wallis-pi", edge=15, rand=135, test=50, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 1e-03
        self.penalty = 1000000.0
        self.max_genome_size = 2400
        self.initial_genome_size = (60, 300)
        self.simplification_steps = 5000
        self.last_str_from_stdout = False
        self.push_config = PushConfig(step_limit=8000)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "float", "bool"}),
            literals=[],
            erc_generators=[self.random_integer_500, self.random_integer_10, self.random_float_500, self.random_float_1]
        )

    def random_integer_500(self):
        return np.random.randint(-500, 501)

    def random_integer_10(self):
        return np.random.randint(-10, 11)

    def random_float_500(self):
        return np.random.uniform(-500, 500)

    def random_float_1(self):
        return np.random.uniform(0, 1)


class WordStats(_PSB1):

    def __init__(self, name="word-stats", edge=36, rand=64, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.02
        self.penalty = 10000
        self.max_genome_size = 3200
        self.initial_genome_size = (80, 400)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=6000)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "float", "bool", "char", "str", "vector_int", "vector_float", "vector_str"}),
            literals=[Char("."), Char("?"), Char("!"), Char(" "), Char("\t"), Char("\n"), IntVector(), FloatVector(), StrVector(), "words of length ", ": ", "number of sentences: ", "average sentence length: "],
            erc_generators=[self.random_integer_100]
        )

    def random_integer_100(self):
        return np.random.randint(-100, 101)


class XWordLines(_PSB1):

    def __init__(self, name="x-word-lines", edge=46, rand=104, test=1000, root="psb", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 3200
        self.initial_genome_size = (80, 400)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=1600)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=2,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "char", "str", "stdout"}),
            literals=[Char(" "), Char("\n")],
            erc_generators=[]
        )


# Used-Defined Problems


class SmallOrLargeString(_PSB1):

    def __init__(self, name="small-or-large-string", edge=26, rand=74, test=1000, root="psbext", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 800
        self.initial_genome_size = (20, 100)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=300)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=1,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "str", "stdout"}),
            literals=["small", "large"],
            erc_generators=[self.random_integer_1000p]
        )

    def random_integer_1000p(self):
        return np.random.randint(0, 1001)


class MedianStringLength(_PSB1):

    def __init__(self, name="median-string-length", edge=0, rand=100, test=1000, root="psbext", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 1
        self.max_genome_size = 800
        self.initial_genome_size = (20, 100)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=200)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=3,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "str", "stdout"}),
            literals=[],
            erc_generators=[self.random_integer_100p, self.random_boolean]
        )

    def random_integer_100p(self):
        return np.random.randint(0, 101)

    def random_boolean(self):
        return np.random.choice([True, False])

    def process_type(self, dat):
        dat["output1"] = [str(item) for item in dat.output1]
        return dat


class SmallOrLargeMedian(_PSB1):

    def __init__(self, name="small-or-large-median", edge=0, rand=100, test=1000, root="psbext", seed=None):
        super().__init__(name, edge, rand, test, root, seed)
        self.error_threshold = 0.0
        self.penalty = 5000
        self.max_genome_size = 800
        self.initial_genome_size = (20, 100)
        self.simplification_steps = 5000
        self.last_str_from_stdout = True
        self.push_config = PushConfig(step_limit=300)

    @property
    def spawner(self):
        return GeneSpawner(
            n_inputs=4,
            instruction_set=InstructionSet().register_core_by_stack({"exec", "int", "bool", "str", "stdout"}),
            literals=["small", "large"],
            erc_generators=[self.random_integer_1000p, self.random_integer_100]
        )

    def random_integer_1000p(self):
        return np.random.randint(0, 1001)

    def random_integer_100(self):
        return np.random.randint(-100, 101)


# Problem Sets


__problem_set = {
    "checksum": Checksum,
    "count-odds": CountOdds,
    "even-squares": EvenSquares,
    "last-index-of-zero": LastIndexOfZero,
    "negative-to-zero": NegativeToZero,
    "replace-space-with-newli": ReplaceSpaceWithNewline,
    "small-or-large": SmallOrLarge,
    "sum-of-squares": SumOfSquares,
    "vector-average": VectorAverage,
    "word-stats": WordStats,
    "collatz-numbers": CollatzNumbers,
    "digits": Digits,
    "for-loop-index": ForLoopIndex,
    "median": Median,
    "number-io": NumberIO,
    "scrabble-score": ScrabbleScore,
    "string-differences": StringDifferences,
    "super-anagrams": SuperAnagrams,
    "vectors-summed": VectorsSummed,
    "x-word-lines": XWordLines,
    "compare-string-lengths": CompareStringLengths,
    "double-letters": DoubleLetters,
    "grade": Grade,
    "mirror-image": MirrorImage,
    "pig-latin": PigLatin,
    "smallest": Smallest,
    "string-lengths-backwards": StringLengthsBackwards,
    "syllables": Syllables,
    "wallis-pi": WallisPi,
}

__problem_set_ext = {
    "small-or-large-string": SmallOrLargeString,
    "median-string-length": MedianStringLength,
    "small-or-large-median": SmallOrLargeMedian,
}


def program_synth(problem, search="GA", npop=1000, ngen=300, nproc=False, seed=None, **kwargs):
    if __problem_set.get(problem):
        problem = __problem_set.get(problem)
    elif __problem_set_ext.get(problem):
        problem = __problem_set_ext.get(problem)
    else:
        raise Exception(f"Cannot find problem {problem}.")

    problem = problem(seed=seed)

    est = PushEstimator(
        spawner=problem.spawner,
        search=search,
        population_size=npop,
        max_generations=ngen,
        push_config=problem.push_config,
        error_threshold=problem.error_threshold,
        penalty=problem.penalty,
        max_genome_size=problem.max_genome_size,
        initial_genome_size=problem.initial_genome_size,
        last_str_from_stdout=problem.last_str_from_stdout,
        parallelism=nproc,
        verbose=2,
        **kwargs
    )

    start = time.time()
    est.fit(*(problem.train))
    end = time.time()

    print("========================================")
    print("post-evolution stats")
    print("========================================")
    print("Runtime: ", end - start)
    test_score = np.sum(est.score(*(problem.test)))
    print("Test error:", test_score)

    return est
