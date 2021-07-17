from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import string
from tqdm import tqdm

def scrap_links(credit0,credit1,alpha=26):
    if alpha > 26: alpha = 26
    temp_list = []
    print("\nChecking driver in catch or Downloading it ...")
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
    # chrome_options.add_argument('--headless')
    driver.get("https://www.credly.com/users/sign_in")

    WebDriverWait(driver, timeout=3)
    username=driver.find_element_by_name("email") 
    username.send_keys(credit0) 
    password =driver.find_element_by_name("password") 
    password.send_keys(credit1) 
    login_button = driver.find_element_by_xpath("//button[@type='submit']")    
    login_button.click()
    sleep(5)
    vm_button = driver.find_element_by_xpath('//*[@id="website-header"]/div[4]/div/nav/div[1]') 
    vm_button.click() 
    sleep(1)
    # print("fetching data...")
    for key in tqdm(string.ascii_lowercase[:alpha],position=0, leave=True):
        try:
            # print("for key ",key)
            searchbar=driver.find_element_by_id("search_input_2")
            searchbar.send_keys(Keys.BACKSPACE) 
            searchbar.send_keys(key) 
            sleep(3)
            vm_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[1]/nav/div[2]/ul/li[2]') 
            vm_button.click() 
            sleep(2)
            cfreq_source = driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/a")
            for x in cfreq_source:
                # to check available attributes in element
                # attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', x)
                # print(attrs)
                temp_list.append(x.get_attribute('href'))
                # print(x.get_attribute('href'))
            sleep(3)
        except NoSuchElementException as ex:
            print("Content not found!\nErr: ",ex)

    try:
        df = pd.DataFrame(temp_list)
        df.to_csv('file_add.csv', index=False, header=False)
    except:
        print("Couldn't save file")
    print("quiting driver ...")
    driver.quit()
    return temp_list

# print(scrap_links('sandeepyadav1478@gmail.com','qwer1478tyui',1))