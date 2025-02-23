import os
import cv2

string = " `.,-':<>;+!*/?%&98#"
coef = 255 / (len(string) - 1)

image = cv2.imread('C:\\Users\\dev\\Desktop\\Python\\main.py\\venv\\ZeroAnonymous\\anonymous_mask.png')
height, width, channels = image.shape


max_width = 125  

aspect_ratio = height / width
new_width = max_width
new_height = int(aspect_ratio * new_width * 0.55) 


resized_image = cv2.resize(image, (new_width, new_height))

gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)


for y in range(0, new_height, 2): 
    s = ""
    for x in range(0, new_width, 1):  
        try:
            
            s += string[len(string) - int(gray_image[y, x] / coef) - 1]
        except IndexError:
            pass
    if s:  
        print(s)

'''
    Функции для цветного вывода
'''

def print_green(text):
    print(f"\033[92m{text}\033[0m")

def print_red(text):
    print(f"\033[91m{text}\033[0m")

'''
    Определение дистрибутива Linux
'''

def get_linux_distro():
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"')
    except FileNotFoundError:
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
            print_green(f"{program_name} has been installed successfully.")
        else:
            print_red(f"Failed to install {program_name}.")
    else:
        print_red("Unsupported Linux distribution. Please install the program manually.")

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
            print_green(f"[+] {program} installed")
        else:
            print_red(f"[-] {program} not installed")
            missing_programs.append(program)
    
    if missing_programs:
        print("\nThe following programs are absent in the system:")
        for program in missing_programs:
            print_red(f" - {program}")
        
        choice = input("\nDo you want to install the missing programs? (y/n): ").lower()
        if choice == "y":
            for program in missing_programs:
                install_program(program)
        else:
            print_red("Please install the missing programs manually to continue.")
    else:
        print_green("\nAll necessary programs are installed.")

'''
    Основная функция
'''

if __name__ == "__main__":
    program_to_check = ["tor", "nmap", "curl", "wget", "macchanger", "bleachbit"]
    check_program(program_to_check)
