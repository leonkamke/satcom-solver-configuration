#!/bin/bash

# Define Maven home directory
M2_HOME="$HOME/maven/apache-maven-3.9.9"
export M2_HOME=$HOME/maven/apache-maven-3.9.6
export PATH=$M2_HOME/bin:$PATH

export JAVA_HOME=$HOME/java/openlogic-openjdk-17.0.14+7-linux-x64
export PATH=$JAVA_HOME/bin:$PATH

# module load Python/3.10.4

# source venv/bin/activate

# Apply changes to the current session
source ~/.bashrc

conda activate master-thesis
