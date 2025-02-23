import os
import cv2
import requests
import numpy as np
from io import BytesIO

'''
    Функции для цветного вывода
'''
def print_green(text):
    print(f"\033[92m{text}\033[0m")

def print_red(text):
    print(f"\033[91m{text}\033[0m")

'''
    Загрузка изображения по URL
'''
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        image_data = BytesIO(response.content)  # Преобразование в поток байтов
        image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)  # Декодирование изображения
        return image
    except requests.exceptions.RequestException as e:
        print_red(f"[-] Image loading error: {e}")
        return None

'''
    Преобразование изображения в ASCII-арт
'''
def convert_image_to_ascii(image):
    if image is None:
        print_red("[-] Error: Image didn't load.")
        return

    # Символы для ASCII-арта (от темного к светлому)
    string = " `.,-':<>;+!*/?%&98#"
    coef = 255 / (len(string) - 1)

    # Получение размеров изображения
    height, width, _ = image.shape

    # Максимальная ширина для ASCII-арта
    max_width = 125

    # Сохранение пропорций и изменение размера
    aspect_ratio = height / width
    new_width = max_width
    new_height = int(aspect_ratio * new_width * 0.55)  # Умножение на 0.55 для коррекции пропорций

    # Изменение размера изображения
    resized_image = cv2.resize(image, (new_width, new_height))

    # Преобразование в черно-белое
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Генерация ASCII-арта
    for y in range(0, new_height, 2):  # Шаг 2 для уменьшения высоты
        s = ""
        for x in range(0, new_width, 1):
            try:
                # Нормализация значения пикселя
                pixel_value = gray_image[y, x]
                index = min(max(int(pixel_value / coef), 0), len(string) - 1)
                s += string[index]
            except IndexError:
                pass
        if s:  # Печать только непустых строк
            print(s)

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
    # URL изображения
    image_url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.1C0HFAqfm-4XIkbT_F93GgHaHa%26pid%3DApi&f=1&ipt=e9cd9c577acd19a4ccbc5cf1428e871eb06e209289701d3ee7b78444d0a093e0&ipo=images"
    
    # Загрузка изображения
    image = load_image_from_url(image_url)
    
    # Преобразование изображения в ASCII-арт
    if image is not None:
        convert_image_to_ascii(image)
    
    # Проверка и установка необходимых программ
    program_to_check = ["tor", "nmap", "curl", "wget", "macchanger", "bleachbit"]
    check_program(program_to_check)