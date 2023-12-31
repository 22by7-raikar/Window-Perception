!/bin/bash

#SBATCH --mail-user=apairaikar@wpi.edu
#SBATCH --mail-type=ALL

#SBATCH -J test_cuda
#SBATCH --output=slurm_outputs/cuda_test_out_%j.out
#SBATCH --error=slurm_outputs/cuda_test_err_%j.err

#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem=64G
#SBATCH --gres=gpu:1
#SBATCH -C A100
#SBATCH -p short
#SBATCH -t 9:00:00

python3 train.py --epochs 25 --batch-size 16

