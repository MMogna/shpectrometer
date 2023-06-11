import subprocess

CMD_CPU_MODEL = r"grep -m 1 'model name' /proc/cpuinfo | cut -d ':' -f2"
CMD_GET_CORES = r"lscpu | grep 'Core(s) per socket: ' | cut -d ':' -f2"
CMD_GET_THREADS = r"lscpu | grep '^CPU(s): ' | cut -d ':' -f2"
CMD_CPU_FREQ = r"lscpu | grep MHz | cut -d ':' -f2"

def get_cpu_model():
    output = subprocess.run(CMD_CPU_MODEL,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().rstrip().strip()


def get_cores():
    output = subprocess.run(CMD_GET_CORES,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().rstrip().strip()


def get_threads():
    output = subprocess.run(CMD_GET_THREADS,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().rstrip().strip()


def get_frequency():
    output = subprocess.run(CMD_CPU_FREQ,
                            shell=True,
                            stdout=subprocess.PIPE)
    output = output.stdout.decode().split()
    output = [float(f) for f in output]
    output = [f"{f/1000:.2f}GHz" if f>1000 else f"{f:.2f}MHz" for f in output]
    return output


def print_cpu_info():
    freq = get_frequency()
    output = ""
    output += f"Model: {get_cpu_model()}\n"
    output += f"Topology: {get_cores()} cores/{get_threads()} threads\n"
    output += f"Frequency: {freq[0]} (min. {freq[2]}, max. {freq[1]})\n"
    return output


if __name__ == "__main__":
    print(print_cpu_info())
