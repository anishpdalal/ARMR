echo "Uninstalling sciSpacy Models"
pip uninstall -y en-core-sci-md
pip uninstall -y en-ner-bc5cdr-md
echo "Exporting environment"
conda env export --no-builds > environment.yml
echo "Reinstalling sciSpacy Models"
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.1.0/en_core_sci_md-0.1.0.tar.gz
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.1.0/en_ner_bc5cdr_md-0.1.0.tar.gz