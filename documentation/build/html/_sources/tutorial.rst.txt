Tutorial
========
1. On your local machine, run git clone https://github.com/MSDS698/ARMR.git
2. run `conda env create -f environment.yml` from command line to get required packages
3. run `conda activate armr` in terminal
4. cd ARMR/code
5. update variables ec2_address and key_file in user_definition.py
6. run `python deploy.py` in terminal
7. go to the EC2 public IP address in your browser
8. register if you are a new user
9. login with your credentials
10. upload audio file (must be a .wav file) and create medical record number
11. submit audio file
11. review and make appropriate edits
12. submit
13. repeat steps 10-12 as necessary
14. logout