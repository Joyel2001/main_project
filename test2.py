from lib2to3.pgen2 import driver
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
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)
        theme=driver.find_element(By.CSS_SELECTOR,"a[href*='login2_page']")
        theme.click()
        time.sleep(4)
        theme=driver.find_element(By.CSS_SELECTOR,"a[href='/loginn']")
        theme.click()
        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("Joy32")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("12045#CEah")
        submit_button = driver.find_element(By.CSS_SELECTOR, "#btn_login")
        submit_button.click()
        browse=driver.find_element(By.CSS_SELECTOR,"a[href='/feedback/94/']")
        browse.click()
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, 2900);")
        time.sleep(5)
        browse=driver.find_element(By.CSS_SELECTOR,"label[for='star3']")
        browse.click()
        elem = driver.find_element(By.NAME, "message")
        elem.send_keys("Good")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(1)
        



if __name__ == '__main__':
    import unittest
    unittest.main()
