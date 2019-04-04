import paramiko
from os.path import expanduser
from user_definition import *


# ## Assumption : Anaconda, Git (configured)

def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    """Connect to a specified ec2 instance"""
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    """Generate or update an enviornment.yml file with all dependencies"""
    stdin, stdout, stderr = \
        ssh.exec_command("conda env create -f "
                         "~/{}/environment.yml".format(git_repo_name))

    if b'already exists' in stderr.read():
        stdin, stdout, stderr = \
            ssh.exec_command("conda env update -f "
                             "~/{}/environment.yml".format(git_repo_name))


def git_clone(ssh):
    """Clones specified repo if not present, otherwise \
        updates repo via git pull command"""
    stdin, stdout, stderr = ssh.exec_command("git --version")

    if b"" is stderr.read():
        git_clone_command = "git clone \
            https://dianewoodbridge@github.com/MSDS698/ARMR.git"
        # git_clone_command = "git clone \
        # https://nkacirek1@github.com/MSDS698/ARMR.git"
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)

        # if git repo already exists, pull
        if b'already exists' in stderr.read():
            cd_and_pull_repo = "cd ARMR; git pull"
            stdin, stdout, stderr = ssh.exec_command(cd_and_pull_repo)


def start_cron_tab(ssh):
    """Calculates driving time periodically"""
    ssh.exec_command("crontab -r")
    cronline = "* * * * * ~/.conda/envs/msds603/bin/python /home/ec2-user/" + \
        "ARMR/code/calculate_driving_time.py"
    ssh.exec_command(
        "crontab -l | { cat; echo \"" + cronline + "\"; } | crontab -")


def logout(ssh):
    """Close ssh connection"""
    stdin, stdout, stderr = ssh.exec_command("logout")
    ssh.close()


def main():
    """Connect to a specified ec2 instance and create/update a \
        conda environment"""
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    git_clone(ssh)
    create_or_update_environment(ssh)
    start_cron_tab(ssh)
    logout(ssh)


if __name__ == '__main__':
    main()
