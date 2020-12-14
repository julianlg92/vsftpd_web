import subprocess


class UserCreationError(Exception):
    """
    Custom exception for Linux user creation
    """
    pass


class UserEditionError(Exception):
    """
    Custom exception for Linux user password change
    """
    pass


class UserDeleteError(Exception):
    """
    Custom exception for Linux user delete
    """
    pass


def user_modify_or_create(username, password, label='', modify=False):
    """
    Linux user creation.

    :param username:
    :param label:
    :return:
    """

    if modify:
        if password != '':
            pass_command = subprocess.run(
                f'echo {username}:{password} | sudo chpasswd', stdout=subprocess.PIPE, shell=True)
            if pass_command.returncode != 0:
                raise UserEditionError
        mod_command = subprocess.run('sudo usermod -c "' + label + '" ' + username, capture_output=True, shell=True)

        if mod_command.returncode != 0:
            raise UserEditionError
    else:
        # Consider change shell to ftp only, not bash
        # use -s /bin/nologin for user locking at creation
        useradd_command = subprocess.run(
            "sudo useradd -c '" + label +
            "' -m -s /usr/sbin/nologin -p $(echo '" + password +
            "' | openssl passwd -1 -stdin) " + username,
            capture_output=True, shell=True)
        disable_command = subprocess.run(
            'sudo usermod -L ' + username, capture_output=True, shell=True)

        if useradd_command.returncode != 0 or disable_command.returncode != 0:
            raise UserCreationError


def user_enable(username):
    enable_command = subprocess.run(f'sudo usermod -U {username}', shell=True, capture_output=True)

    if enable_command.returncode != 0:
        raise UserDeleteError


def user_delete(username):
    userdel_command = subprocess.run(
        'sudo userdel -f ' + username, capture_output=True, shell=True)

    if userdel_command.returncode != 0:
        raise UserDeleteError
