problem="small-or-large-median"
search="RGA"
npop=1000
ngen=300
nproc=60

mkdir $problem

for seed in $(seq 1001 1025)
do
    python run3.py $problem $search $npop $ngen $nproc $seed >> $problem/$seed.log
    gzip $problem/$seed.hst
done