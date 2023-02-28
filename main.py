from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import os

filename = 'list.txt'

os.environ['WDM_LOG_LEVEL'] = '0'
number_list = []

file = open(filename, "r")

for line in file.readlines():
    number_list.append(line.strip())

options = Options()
options.add_argument(r'--user-data-dir=C:\Users\ederm\AppData\Local\Google\Chrome\User Data')
options.add_argument('--profile-directory=Profile 32')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service(ChromeDriverManager().install())


def write_to_file(filename: str, data: str):
    with open(filename, 'a') as file:
       file.write(data)
       file.write('\n')

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com/")
sleep(10)


for number in number_list:
    driver.execute_script(f"link = document.createElement('a');")
    driver.execute_script(f"link.href = 'https://wa.me/55{number}?text=Ola';")
    driver.execute_script(f'document.body.appendChild(link);')
    driver.execute_script(f'link.click();')
    sleep(3)

    try:
        validator = driver.execute_script(f'return document.querySelector("#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div.f8jlpxt4.iuhl9who").innerText')

        if validator == 'O número de telefone compartilhado através de url é inválido.':
            print(f"{number} é um whatsapp invalido")
            write_to_file('invalid.txt', number)        
        else:
            raise Exception('Whatsapp valido')
    except:
        print(f"{number} é um whatsapp valido")
        write_to_file('valid.txt', number)

    finally:
        driver.execute_script(f'window.location.reload();')
        sleep(5)


driver.quit()