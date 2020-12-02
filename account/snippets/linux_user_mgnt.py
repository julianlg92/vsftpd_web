import subprocess


class UserCreationError(Exception):
    """
    Custom exception for Linux user creation
    """
    pass


class PasswdChangeError(Exception):
    """
    Custom exception for Linux user password change
    """
    pass


def user_creation(username, label=''):
    """
    Linux user creation.

    :param username:
    :param label:
    :return:
    """

    # Consider change shell to ftp only, not bash
    # use -s /bin/nologin for user locking at creation
    command = subprocess.run(
        ['useradd', '-c', label, '-m', '-s', '/bin/nologin', username], capture_output=True)
    if command.returncode != 0:
        raise UserCreationError


def user_passwd_change(username, password):
    proc = subprocess.run(
        f'echo {username}:{password} | chpasswd', stdout=subprocess.PIPE, shell=True)

    if proc.returncode != 0:
        raise PasswdChangeError


def user_enable(username):
    pass
