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
        dark=driver.find_element(By.CSS_SELECTOR,"a[href='/loginn']")
        dark.click()
        time.sleep(1)
        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("Staff1")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("12045#CEah")
        submit_button = driver.find_element(By.CSS_SELECTOR, "#btn_login")
        submit_button.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a[href='/booking-chart/'] > .hide-menu")
        browse.click()
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 150);")
        time.sleep(1)
        view=driver.find_element(By.CSS_SELECTOR,"a[href='/booking_list/'] > .hide-menu")
        view.click()
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1)
        chaps=driver.find_element(By.CSS_SELECTOR,"option[value='Workshop on Managing Solid Waste']")
        chaps.click()
        time.sleep(1)
        time.sleep(1)
        chap = driver.find_element(By.CSS_SELECTOR, "button[style*='background-color: #007bff; color: #fff; border: none;']")
        chap.click()
        time.sleep(3)
        options = driver.find_element(By.CSS_SELECTOR, "option[value='']")
        options.click()
        options.click()
        time.sleep(1)
        select=driver.find_element(By.CSS_SELECTOR, "button[style*='background-color: #007bff; color: #fff; border: none;']")
        select.click()
        time.sleep(1)
        

    # Add more test methods as needed

if __name__ == '__main__':
    import unittest
    unittest.main()