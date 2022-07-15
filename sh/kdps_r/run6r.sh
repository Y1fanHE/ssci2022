problem="median-string-length"
last="small-or-large-median"
search="RGA"
npop=1000
ngen=300
nproc=60

cp subprogram.arch subprogram.arch.bp
cp summary.csv summary.csv.bp

python postprocess.py $last

mkdir $problem

for seed in $(seq 1001 1025)
do
    python run6r.py $problem $search $npop $ngen $nproc $seed >> $problem/$seed.log
done