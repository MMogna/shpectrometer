import subprocess

CMD_HOSTNAME = r"cat /proc/sys/kernel/hostname"
CMD_KERNEL = r"uname -r"
CMD_OS_NAME = r'cat /etc/*-release | grep "PRETTY_NAME" | sed "s/PRETTY_NAME=//g"'

def get_hostname():
    output = subprocess.run(CMD_HOSTNAME,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().strip()


def get_kernel_version():
    output = subprocess.run(CMD_KERNEL,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().strip()


def get_os_name():
    output = subprocess.run(CMD_OS_NAME,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().strip().replace('"','')


def print_host_info():
    output = ""
    output += f"OS Name: {get_os_name()}\n"
    output += f"Kernel info: {get_kernel_version()}\n"
    output += f"Hostname: {get_hostname()}"
    return output


if __name__ == "__main__":
    print(print_host_info())