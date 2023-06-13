import subprocess

CMD_SLOTS = r"dmidecode --type 17 | grep '^[[:space:]]Size:' | cut -d ':' -f2"
CMD_RAM_SPEED = r"dmidecode --type 17 | grep -m 1 'Speed:' | cut -d ':' -f2"
CMD_ECC = r"dmidecode --type memory | grep -m 1 'Error Correction Type: ' | cut -d ':' -f2"
CMD_TYPE = r"dmidecode --type memory | grep -m 1 '^[[:space:]]Type: ' | cut -d ':' -f2"


def get_ram_type():
    output = subprocess.run(CMD_TYPE,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().strip().rstrip()


def get_ecc_presence():
    output = subprocess.run(CMD_ECC,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().strip().rstrip()


def get_ram_slots():
    output = subprocess.run(CMD_SLOTS,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().strip().replace(' ','').split('\n')


def get_ram_speed():
    output = subprocess.run(CMD_RAM_SPEED,
                            shell=True,
                            stdout=subprocess.PIPE)
    return output.stdout.decode().strip().rstrip()


def print_ram_info():
    slots = ["0GB" if s == "NoModuleInstalled" else s for s in get_ram_slots()]
    sizes = [int(s.replace("GB",'0')) for s in slots]
    output = ""
    output += f"Size: {sum(sizes)}GB\n"
    output += f"Slots setup: {' - '.join(slots)}\n\n"
    output += f"ECC type: {get_ecc_presence()}\n"
    output += f"RAM type: {get_ram_type()}\n"
    output += f"RAM Speed: {get_ram_speed()}\n"
    return output


if __name__ == "__main__":
    print(print_ram_info())