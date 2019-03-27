# ARMOR
Automated Medical Transcription

## Initial Setup
1. conda env create -f environment.yml

2. source activate app

3. pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.1.0/en_core_sci_md-0.1.0.tar.gz

4. pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.1.0/en_ner_bc5cdr_md-0.1.0.tar.gz

## Export Environment
1. chmod u+x export-conda-env.sh (Run only once)

2. ./export-conda-env.sh

## Authors
Anish Dalal, Nicole Kacirek, Sarah Melancon, Darren Thomas, and Tyler Ursuy