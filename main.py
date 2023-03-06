# selenium imports
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# cdm
from webdriver_manager.chrome import ChromeDriverManager

# commom imports
from time import sleep
import os

# typing imports
from typing import List

# sugar imports
from colorama import Fore, init

# startups
init(autoreset=True)
os.environ['WDM_LOG_LEVEL'] = '0'

def get_current_hour_and_minute() -> str:
    from datetime import datetime
    return datetime.now().strftime("%H:%M")

def write_to_file(filename: str, data: str):
    with open(filename, 'a') as file:
        file.write(f"{data}\n")

def main(phone_list: List[str]) -> None:
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # change the path to your chrome user data path
    options.add_argument(r'--user-data-dir=C:\Users\ederm\AppData\Local\Google\Chrome\User Data')
    # select the profile that has whatsapp web logged in (qrcode scanned)
    options.add_argument('--profile-directory=Profile 32')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com/")
    sleep(15)


    for number in phone_list:
        driver.execute_script(f"link = document.createElement('a');")
        driver.execute_script(f"link.href = 'https://wa.me/55{number}?text=Ola';")
        driver.execute_script(f'document.body.appendChild(link);')
        driver.execute_script(f'link.click();')
        sleep(4)

        try:
            error_flag = driver.execute_script(f'return document.querySelector("#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div.f8jlpxt4.iuhl9who").innerText')

            if error_flag == 'O número de telefone compartilhado através de url é inválido.':
                print(f"{get_current_hour_and_minute()} {number}{Fore.RED} é um whatsapp invalido")
                write_to_file('invalids.txt', number)   
                driver.execute_script(f"document.querySelector('#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div.f8jlpxt4.iuhl9who').remove();")     
            else:
                raise Exception()
        except:
            print(f"{get_current_hour_and_minute()} {number}{Fore.GREEN} é um whatsapp valido")
            write_to_file('valids.txt', number)

    driver.close()


if __name__ == '__main__':
    print(f"[@]{Fore.YELLOW} Digite o nome do arquivo.")
    filename: str = input(">>>")

    if not filename.endswith('.txt'):
        filename += '.txt'
    
    stdin_list: List[str] = []
    
    for line in open(filename, "r").readlines():
        stdin_list.append(line.strip())
    
    main(phone_list=stdin_list)