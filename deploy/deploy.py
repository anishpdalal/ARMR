import paramiko
from os.path import expanduser
from user_definition import *


# ## Assumption : Anaconda, Git (configured)

def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    stdin, stdout, stderr = \
        ssh.exec_command("conda env create -f "
                         "~/{}/environment.yml".format(git_repo_name))

    if b'already exists' in stderr.read():
        stdin, stdout, stderr = \
            ssh.exec_command("conda env update -f "
                             "~/{}/environment.yml".format(git_repo_name))


def git_clone(ssh):
    # ---- HOMEWORK ----- #
    stdin, stdout, stderr = ssh.exec_command("git --version")

    if b"" is stderr.read():
        git_clone_command = "git clone https://github.com/" + \
                            git_repo_owner + "/" + git_repo_name + ".git"
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)

        # if git repo already exists, pull
        if b'already exists' in stderr.read():
            cd_and_pull_repo = "cd " + git_repo_name + "; git pull"
            stdin, stdout, stderr = ssh.exec_command(cd_and_pull_repo)


def start_cron_tab(ssh):
    ssh.exec_command("crontab -r")
    cronline = "* * * * * ~/.conda/envs/msds603/bin/python /home/ec2-user/" + \
               git_repo_name + "/deploy/calculate_driving_time.py"
    ssh.exec_command(
        "crontab -l | { cat; echo \"" + cronline + "\"; } | crontab -")


def logout(ssh):
    stdin, stdout, stderr = ssh.exec_command("logout")
    ssh.close()


def main():
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    git_clone(ssh)
    create_or_update_environment(ssh)
    start_cron_tab(ssh)


if __name__ == '__main__':
    main()
