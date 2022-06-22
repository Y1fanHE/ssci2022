problem="small-or-large"
search="GA"
npop=1000
ngen=300
nproc=60

mkdir $problem

for seed in $(seq 1001 1025)
do
    python run.py $problem $search $npop $ngen $nproc $seed >> $problem/$seed.log
done