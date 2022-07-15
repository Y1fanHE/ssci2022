problem="small-or-large"
last="median-string-length"
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
    python run7r.py $problem $search $npop $ngen $nproc $seed >> $problem/$seed.log
done