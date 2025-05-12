#!/usr/bin/zsh 

### Job Parameters 
#SBATCH --qos=normal
#SBATCH --mem=10000
#SBATCH --partition=c23ms
#SBATCH --time=24:00:00         # Run time of 24 hours
#SBATCH --job-name=eval         # Sets the job name
#SBATCH --output=stdout.txt     # redirects stdout and stderr to stdout.txt
#SBATCH --account=thes1934      # Replace with your project-id or delete the line

### Program Code
export CONDA_ROOT=$HOME/miniforge3
source $CONDA_ROOT/etc/profile.d/conda.sh
export PATH="$CONDA_ROOT/bin:$PATH"
conda activate sparkle

python convergence_eval_par10.py
