from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from time import sleep
import pandas as pd
from tqdm import tqdm
from packs.credly_links import scrap_links

def scrap_free(paratroops,add_list):
    print("geting para links")
    temp_list_free = []
    if len(add_list) > 0:
      temp_list = add_list
    else:
      try:
        df = pd.read_csv(r'file_add.csv')
        temp_list = df.iloc[:,0].tolist()
      except:
        print("Couldn't find file.")
        exit("Dead Process")
    print("\nChecking driver in catch or Downloading it ...")
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
    driver.maximize_window()
    for i in tqdm(temp_list, position=0, leave=True):
        driver.get(i)
        try:
            cost_exist = driver.find_elements_by_xpath("/html/body/main/div[1]/div/div/div[2]/div[1]/ul/li/span[2]")
            for x in cost_exist:
                # to check available attributes in element
                # attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', x)
                # print(attrs)
                print(x.get_attribute("innerText"))
                if x.get_attribute("innerText") in paratroops:
                    print("\n",x.get_attribute("innerText")," link: ",i)
                    temp_list_free.append(i)
        except:
            print("Cost not found.")
    print("Closing browser")
    driver.close()
    try:
      if len(temp_list_free) > 0:
        df = pd.DataFrame(list(set(temp_list_free)))
        df.to_csv('para_list.csv', index=False, header=False)
        print("links saved in para_list file")
    except:
      print("Couldn't save file")
    return temp_list_free 

print(scrap_free(['Free','Paid'],scrap_links('example@gmail.com','password',26)))
# other options are here:(choose any one)

# Validation
# Foundational
# Months
# Learning
# Intermediate
# Hours
# Experience
# Free
# Advanced