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
    stdin, stdout, stderr = ssh.exec_command("sudo yum -y install gcc")
    stdin, stdout, stderr = ssh.exec_command("git checkout spacy-functions")
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
            https://{}@github.com/{}/{}.git".format(
                git_user_id, git_repo_owner, git_repo_name)
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)

        # if git repo already exists, pull
        if b'already exists' in stderr.read():
            cd_and_pull_repo = "cd {}; git pull".format(git_repo_name)
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


def deploy_model(ssh):
    """Pull model from S3"""
    if aws_access_key_id and aws_secret_access_key:
        stdin, stdout, stderr = ssh.exec_command("mkdir .aws")
        if b"File exists" not in stderr.read():
            stdin, stdout, stderr = ssh.exec_command("touch .aws/credentials")
            stdin, stdout, stderr = ssh.exec_command("echo [default] >> \
                .aws/credentials")
            stdin, stdout, stderr = ssh.exec_command("echo aws_access_key_id = \
                {} >> .aws/credentials".format(aws_access_key_id))
            stdin, stdout, stderr = ssh.exec_command("echo aws_secret_access_key = \
                {} >> .aws/credentials".format(aws_secret_access_key))
            stdin, stdout, stderr = ssh.exec_command(
                "rm -rf ~/{}/models".format(git_repo_name))
            stdin, stdout, stderr = ssh.exec_command(
                "mkdir ~/{}/models".format(git_repo_name))
        else:
            stdin, stdout, stderr = ssh.exec_command(
                "rm -rf ~/{}/models".format(git_repo_name))
            stdin, stdout, stderr = ssh.exec_command(
                "mkdir ~/{}/models".format(git_repo_name))
        stdin, stdout, stderr = ssh.exec_command("~/.conda/envs/msds603/bin/python /home/{}/ \
            {}/code/pull_model_from_s3.py".format(user, git_repo_name))
        print(stdout.read())
        ssh.exec_command("tar -xzf *.gz -C ~/{}/models".format(git_repo_name))


def main():
    """Connect to a specified ec2 instance and create/update a \
        conda environment"""
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    git_clone(ssh)
    create_or_update_environment(ssh)
    deploy_model(ssh)
    logout(ssh)


if __name__ == '__main__':
    main()
