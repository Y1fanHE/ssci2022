# SSCI 2022

## Problems from PSB1

### Small or Large

Given an integer n, print "small" if n < 1000 and "large" if n >= 2000 (and
nothing if 1000 <= n < 2000).

Solution:

```
("large" input_0 str_dup_times input_0 str_stack_depth str_split_on_str str_dup "small" int_div str_rot str_yank print_str)

Human partition
-----
Subprogram 1: ("large" input_0 str_dup_times)
Subprogram 2: (input_0 str_stack_depth)
Subprogram 3: (str_split_on_str str_dup "small")
Subprogram 4: (int_div str_rot)
Subprogram 5: (str_yank print_str)
```

### Compare String Lengths

Given three strings n1, n2, and n3, return true if len(n1) < len(n2) < len(n3),
and false otherwise.

Solution:

```
(input_0 str_length exec_is_empty input_1 str_length exec_do_range () input_2
str_head str_length int_lt)

Human partition
-----
Subprogram 1: (input_0 str_length exec_is_empty)
Subprogram 2: (input_1 str_length)
Subprogram 3: (exec_do_range ())
Subprogram 4: (input_2 str_head str_length)
Subprogram 5: (int_lt)
```

### Median

Given 3 integers, print their median.

Solution:

```
(input_0 input_2 int_max input_0 input_2 int_min input_1 int_max int_min
print_int)

Human partition
-----
Subprogram 1: (input_0 input_2)
Subprogram 2: (int_max)
Subprogram 3: (int_min)
Subprogram 4: (input_1 int_max int_min)
Subprogram 5: (print_int)
```

## Composite Problems in Experiment I

### Composite 01: Small or Large String

Given a string n, print "small" if len(n) < 100 and "large" if len(n) >= 200
(and nothing if 100 <= len(n) < 200).

### Composite 02: Median String Length

Given 3 strings, print the median of their lengths.

### Composite 03: Small or Large Median

Given 4 integers a, b, c, d, print "small" if median(a,b,c) < d and "large" if
median(a,b,c) > d (and nothing if median(a,b,c) = d).

## Sequence of Problems in Experiment II

- Median (`run4.sh`)
- Compare String Lengths (`run5.sh`)
- Small or Large (`run6.sh`)
- Median String Length (`run7.sh`)
- Small or Large Median (`run8.sh`)
- Small or Large String (`run9.sh`)

## Methods

1. PushGP + Even partitions (EP) + ARM
2. PushGP + Human partitions (HP) + ARM
3. PushGP

## Parameters

- Evaluation number: 1000 x 300
- Partition number: 5
- Replacement rate: 0.1
- Adaptation rate: 0.5
- Repetition: 25

# Scripts and Data

## Get Started

Before run the scripts, you need to install a modified version of `pyshgp`.

```sh
git clone https://github.com/Y1fanHE/pyshgp
cd pyshgp
pip install .
cd ..
```

You also need to download data files for PSB1 problems.

```sh
git clone https://github.com/thelmuth/program-synthesis-benchmark-datasets.git
cd program-synthesis-benchmark-datasets
chmod a+x decompress
./decompress
cd ..
```

Clone this repository and place benchmark dataset in the right places.

```sh
git clone https://github.com/Y1fanHE/ssci2022
cd ssci2022
ln -s ../program-synthesis-benchmark-datasets/datasets psb
```

Download data files for composite problems from [xxx]().

```sh
tar xvf psbext.tar
gunzip -r -v psbext
```

Now, you are able to run the experiments.

## Original PushGP

Edit parameters in `run.sh` and run the script.

```sh
./run.sh
```

Or edit Python code in `run2.py` with `replacement_rate=0.0` and `adaptation_rate=0.0`.

```python
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
```

Then, edit parameters in `run2.sh` and run the script.

```sh
./run2.sh
```

## PushGP+EP+ARM

Unzip the corresponding files in `arm_data/archive` (usually named as `[problem name]-r0.1-a0.5.tar`). Copy `run2.py` and `run2.sh` to the root directory of this project.

```sh
cp arm_data/archive/[problem name]-r0.1-a0.5.tar .
tar xvf [problem name]-r0.1-a0.5.tar
cp [problem name]-r0.1-a0.5/run2* .
```

Then, run the script.

```sh
./run2.sh
```

**NOTICE:** you may need solutions from other problems to run this method. Please read the code and find the corresponding `.sol` files and copy it to the correct position.

## PushGP+HP+ARM

Unzip the corresponding files in `arm_data/archive` (usually named as `[problem name]-r0.1-a0.5-h.tar`). Copy `run3.py` and `run3.sh` to the root directory of this project.

```sh
cp arm_data/archive/[problem name]-r0.1-a0.5-h.tar .
tar xvf [problem name]-r0.1-a0.5-h.tar
cp [problem name]-r0.1-a0.5-h/run3* .
```

Then, run the script.

```sh
./run3.sh
```

**NOTICE:** you may need solutions from other problems to run this method. Please read the code and find the corresponding `.sol` files and copy it to the correct position.

## PushGP+EP+ARM in Experiment II

Run the following scripts sequentially.

```sh
./run4.sh && ./run5.sh && ./run6.sh && ./run7.sh && ./run8.sh && ./run9.sh
```

## Data Files

The data is archived in `.tar` files with names as follows.

```txt
[problem name]-[method].tar

methods
----------
               -> PushGP
r0.0-a0.0      -> PushGP
r0.1-a0.5      -> PushGP+EP+ARM in Experiment I
r0.1-a0.5-h    -> PushGP+HP+ARM in Experiment I
r0.1-a0.5-kdps -> PushGP+EP+ARM in Experiment II
```

Please download the data file by [xxx]().

## Analytical and Plotting script

Please check the jupyter notebook and other files in `arm_data`.