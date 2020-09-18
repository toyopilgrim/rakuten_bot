import argparse
import os
import signal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

parser = argparse.ArgumentParser(description='Log in to Rakuten.')
parser.add_argument('-u', '--user-id', type=str, required=True, dest='user_id')
parser.add_argument('-p', '--password', type=str, required=True, dest='password')
parser.add_argument('-i', '--item-page', type=str, required=True, dest='item_page')

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
print('Process start')

try:
    args = parser.parse_args()
    url = "https://grp02.id.rakuten.co.jp/rms/nid/loginfwdi"
    driver.get(url)
    driver.save_screenshot("before_login.png")
    print("Before login")
    driver.implicitly_wait(2)

    driver.find_element_by_id("loginInner_u").send_keys(args.user_id)
    driver.find_element_by_id("loginInner_p").send_keys(args.password)
    driver.save_screenshot("login.png")
    print("Logging in")
    driver.find_element_by_css_selector('input[type="submit"][class="loginButton"]').click()

    wait = WebDriverWait(driver, 10)

    driver.save_screenshot('after_login.png')
    print("Logined successfully")

    # TODO:add scheduling
    print("Loading item page")
    driver.get(args.item_page)
    driver.save_screenshot('item_page.png')
    
    elemntCart = driver.find_element_by_class_name('new_addToCart')
    driver.execute_script("arguments[0].click();", elemntCart)
    driver.save_screenshot('cart.png')

    print("Added to cart")

except Exception as e:
    print(e)

finally:
    print('Finished')

    driver.stop_client()
    driver.close()
    driver.quit()
