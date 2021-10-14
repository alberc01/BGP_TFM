from selenium import webdriver
import os 
import time
import platform

_SO_VAR =platform.system()
_CURR_DIR = os.path.abspath(os.getcwd())

def get_chromeDriver():
    if _SO_VAR == "Windows":
        chromedriver = _CURR_DIR + "chromedriver_win32\\chromedriver.exe"
    elif _SO_VAR == "Linux":
        chromedriver = _CURR_DIR + "chromedriver_linux64/chromedriver.exe"

    os.environ["webdriver.chrome.driver"] = chromedriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=chromedriver,options=chrome_options)
    return driver



# # comunidades a recopilar
# comunidades = ['Madrid', 'Navarra', 'Andalucía', 'Cataluña', 'País Vasco', 'La Rioja', 'Aragón', 'Galicia' ]
# # años a investigar
# anio = list(range(1995,2020))

# # escribir aquí el código
# # def PIBcomunidades(anio,data):
# pib = []
# com = []
# data = []
# wata = []
# mata = []
# for a in anio :
#     url = 'https://datosmacro.expansion.com/pib/espana-comunidades-autonomas?anio='+ str(a)
#     driver.get(url)
#     driver.delete_all_cookies()
#     pibCapita = driver.find_element_by_id("didomi-notice-agree-button")
#     pibCapita.click()
#     pibCapita = driver.find_element_by_id("tabgdpapc")
#     pibCapita.click()
#     time.sleep(3)
#     comun = driver.find_elements_by_xpath("//table[@id='tbPC']/tbody/tr/td[1]/a")
#     pib = driver.find_elements_by_xpath("//table[@id='tbPC']/tbody/tr/td[3]")
#     for i in range(len(comun)):
#         aux = comun[i].text
#         data += [[aux.replace(' [+]',''), a, formatea(pib[i].text)]]