
# Launches ProgCE $3 times (run) on all datasets in an input folder
# and places output of each run in a subfolder in the output folder
#
# Note: this script must be run from the folder containing run_CE_on_JDD.sh !!!
#
# Example:
#   cd /auto/vberry/GH/PhyloNet/Simulations/run_progCE_on_sim_JDD
#   ./runCE-all-1k-10k-10times.sh ABC-111-network/jdd_CE_1k_SNP ABC-111-network/resultats_1k
#

if [ $# -ne 3 ] ; then 
    echo "Usage: $0 input_JDD_folder output_folder nb_runs_each_JDD" ;
    exit 1 ;
fi
if ! [ -d "$1" ] ; then
    echo "$1 is not a (input) folder" ;
    exit 2 ;
fi
if ! [ -d "$2" ] ; then
    echo "$2 is not a (output) folder" ;
    exit 3 ;
fi

WORK_DIR=`pwd`
#echo $WORK_DIR

cd $1
IN_FOLDER=`pwd` # get absolute path for input FOLDER
cd $WORK_DIR
cd $2
OUT_FOLDER=`pwd` # idem for output folder
cd $WORK_DIR

echo $IN_FOLDER
echo $OUT_FOLDER

for r in $(seq 1 $3) ; do  
  # make a run -> in a separate folder for each run, as otherwise output files erase one another
  if ! [ -d $OUT_FOLDER/run$r ] ; then
       mkdir $OUT_FOLDER/run$r ;
  fi
  cd $OUT_FOLDER/run$r ; # go to output folder to run progCE from here
  for f in $IN_FOLDER/*.xml ; do
      # get the JDD number from the file name
      j=`basename $f .xml | awk -F "-" '{print $NF}'` 
      #
      # Note the -l to ask to run on fischerXX nodes: to make all computations on similar nodes
      # Note the -cwd flag below that asks to run from here
      qsub -cwd  -l "hostname=fischer*" -N CE-j$j-r$r $WORK_DIR/run_CE_one_JDD.sh -j$j-r$r $f ;
  done
done
cd $WORK_DIR # comes back to where we where at the start of the script
