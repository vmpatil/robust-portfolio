# DIR=~/Documents/Vrishabh
# mkdir $DIR/LOGS

##------------------------- Tuesday April 30 10:09 PM
DIR=~/Documents/Vrishabh
num_sectors=10
T=30
num_years=30

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -m > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_monthly.txt

##------------------------- 

DIR=~/Documents/Vrishabh
num_sectors=12
T=30
num_years=30

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -m > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_monthly.txt

##------------------------- 

DIR=~/Documents/Vrishabh
num_sectors=17
T=30
num_years=30

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -m > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_monthly.txt

##-------------------------

DIR=~/Documents/Vrishabh
num_sectors=5
T=120
num_years=10

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -d > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_daily.txt

##-------------------------

DIR=~/Documents/Vrishabh
num_sectors=5
T=260
num_years=10

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -d > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_daily.txt

##-------------------------

DIR=~/Documents/Vrishabh
num_sectors=10
T=120
num_years=10

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -d > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_daily.txt

##-------------------------

DIR=~/Documents/Vrishabh
num_sectors=10
T=260
num_years=10

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -d > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_daily.txt

##-------------------------

DIR=~/Documents/Vrishabh
num_sectors=12
T=120
num_years=10

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -d > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_daily.txt

##-------------------------

DIR=~/Documents/Vrishabh
num_sectors=12
T=260
num_years=10

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -d > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_daily.txt

##-------------------------

DIR=~/Documents/Vrishabh
num_sectors=17
T=120
num_years=10

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -d > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_daily.txt

##-------------------------

DIR=~/Documents/Vrishabh
num_sectors=17
T=260
num_years=10

INPREFIX=$DIR
OUTPREFIX=$DIR

chmod +x $DIR/portfolio_simulate_optimize.py

$DIR/portfolio_simulate_optimize.py $INPREFIX $OUTPREFIX $num_sectors $T $num_years -d > $DIR/LOGS/log_${num_sectors}_${T}_${num_years}_daily.txt

##-------------------------