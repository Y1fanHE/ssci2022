problem="compare-string-lengths"
last="median"
search="RGA"
npop=1000
ngen=300
nproc=60

python postprocess.py $last

mkdir $problem

for seed in $(seq 1001 1025)
do
    python run5r.py $problem $search $npop $ngen $nproc $seed >> $problem/$seed.log
done