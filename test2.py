from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()

    def test_02_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)
        dark=driver.find_element(By.CSS_SELECTOR,"a[href='/loginn']")
        dark.click()
        time.sleep(1)
        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("admin1")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("12045#CEah")
        submit_button = driver.find_element(By.CSS_SELECTOR, "#btn_login")
        submit_button.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a[href='/booking-chart/'] > .hide-menu")
        browse.click()
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 150);")
        time.sleep(2)
        view=driver.find_element(By.CSS_SELECTOR,"a[href='/user-list/'] > .hide-menu")
        view.click()
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1)
        chaps=driver.find_element(By.CSS_SELECTOR,"option[value='customer']")
        chaps.click()
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)


    # Add more test methods as needed

if __name__ == '__main__':
    import unittest
    unittest.main()