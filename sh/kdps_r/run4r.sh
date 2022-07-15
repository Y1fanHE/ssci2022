problem="small-or-large-string"
search="GA"
npop=1000
ngen=300
nproc=60

mkdir $problem

for seed in $(seq 1001 1025)
do
    python run4r.py $problem $search $npop $ngen $nproc $seed >> $problem/$seed.log
done