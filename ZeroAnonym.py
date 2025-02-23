import os
import cv2
import requests
import numpy as np
from io import BytesIO

'''
    Functions for color output
'''
def print_green(text):
    print(f"\033[92m{text}\033[0m")

def print_red(text):
    print(f"\033[91m{text}\033[0m")

'''
    URL image load
'''
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP errors check
        image_data = BytesIO(response.content)  # Baytte transformation
        image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)  # Image decoding
        return image
    except requests.exceptions.RequestException as e:
        print_red(f"[-] Image loading error: {e}")
        return None

'''
    Image conversion into ASCII-art
'''
def convert_image_to_ascii(image):
    if image is None:
        print_red("[-] Error: Image didn't load.")
        return

    # Symbols for ASCII-Art(from dark to bright)
    string = " `.,-':<>;+!*/?%&98#"
    coef = 255 / (len(string) - 1)

    #Obtaining the size of the image
    height, width, _ = image.shape

    # Max width for ASCII-Art
    max_width = 125

    # Preservation of proportions and change in size
    aspect_ratio = height / width
    new_width = max_width
    new_height = int(aspect_ratio * new_width * 0.55)  # Multiplication by 0.55 to correct proportions

    # Changing the size of the image
    resized_image = cv2.resize(image, (new_width, new_height))

    # Transformation into black and white
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Генерация ASCII-арта
    for y in range(0, new_height, 2):  # Step 2 to reduce the height
        s = ""
        for x in range(0, new_width, 1):
            try:
                # Normalization of the pixel value
                pixel_value = gray_image[y, x]
                index = min(max(int(pixel_value / coef), 0), len(string) - 1)
                s += string[index]
            except IndexError:
                pass
        if s:  # Printing only non -empty lines
            print(s)

'''
    Determination of the Linux distribution
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
    Determination of the package manager
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
    Installing program
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
    Checking the availability of the program
'''
def is_program_installed(program_name):
    return os.system(f"which {program_name}") == 0

'''
    Checking the list of programs
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
    # image URL 
    image_url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.1C0HFAqfm-4XIkbT_F93GgHaHa%26pid%3DApi&f=1&ipt=e9cd9c577acd19a4ccbc5cf1428e871eb06e209289701d3ee7b78444d0a093e0&ipo=images"
    
    # loading image
    image = load_image_from_url(image_url)
    
    # mage transformation into ASCII-Art
    if image is not None:
        convert_image_to_ascii(image)
    
    # Checking and installing the necessary programs
    program_to_check = ["tor", "nmap", "curl", "wget", "macchanger", "bleachbit"]
    check_program(program_to_check)
