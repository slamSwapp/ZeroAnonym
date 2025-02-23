import os

'''
    Определение дистрибутива Linux
'''
def get_linux_distro():
    with open("/etc/os-release", "r") as f:
        for line in f:
            if line.startswith("ID="):
                return line.strip().split("=")[1].strip('"')
    return None

'''
    Определение пакетного менеджера
'''
def get_package_manager():
    distro = get_linux_distro()
    if distro in ["ubuntu", "debian"]:
        return "apt"
    elif distro in ["fedora", "rhel", "centos"]:
        return "dnf"
    elif distro == "arch":
        return "pacman"
    elif distro == "opensuse":
        return "zypper"
    else:
        return None

'''
    Установка программы
'''
def install_program(program_name):
    package_manager = get_package_manager()
    if package_manager:
        print(f"Installing {program_name} using {package_manager}...")
        if os.system(f"sudo {package_manager} install -y {program_name}") == 0:
            print(f"{program_name} has been installed successfully.")
        else:
            print(f"Failed to install {program_name}.")
    else:
        print("Unsupported Linux distribution. Please install the program manually.")

'''
    Проверка наличия программы
'''
def is_program_installed(program_name):
    return os.system(f"which {program_name}") == 0

'''
    Проверка списка программ
'''
def check_program(program_list):
    missing_programs = []
    for program in program_list:
        if is_program_installed(program):
            print(f"[+] {program} installed")
        else:
            print(f"[-] {program} not installed")
            missing_programs.append(program)
    
    if missing_programs:
        print("\nThe following programs are absent in the system:")
        for program in missing_programs:
            print(f" - {program}")
        
        choice = input("\nDo you want to install the missing programs? (y/n): ").lower()
        if choice == "y":
            for program in missing_programs:
                install_program(program)
        else:
            print("Please install the missing programs manually to continue.")
    else:
        print("\nAll necessary programs are installed.")

'''
    Основная функция
'''
if __name__ == "__main__":
    program_to_check = ["tor", "nmap", "curl", "wget", "macchanger", "bleachbit"]
    check_program(program_to_check)