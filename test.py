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
        theme=driver.find_element(By.CSS_SELECTOR,"a[href*='login2_page']")
        theme.click()
        time.sleep(4)
        theme=driver.find_element(By.CSS_SELECTOR,"a[href='/loginn']")
        theme.click()
        time.sleep(4)
        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("joy32")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("12045#CEah")
        submit_button = driver.find_element(By.CSS_SELECTOR, "#btn_login")
        submit_button.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a[href='/ecomerce_index/']")
        browse.click()
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 150);")
        time.sleep(2)
        # view=driver.find_element(By.CSS_SELECTOR,"a.nav-link.dropdown-toggle[data-bs-toggle='dropdown']")
        # view.click()
        # time.sleep(2)
        # chaps=driver.find_element(By.CSS_SELECTOR,"a.dropdown-item[href='/view_cart/']")
        # chaps.click()
        # driver.execute_script("window.scrollBy(0, 300);")
        # time.sleep(1)
        
        chaps=driver.find_element(By.CSS_SELECTOR,"a.nav-item.nav-link[href='/order_page/']")
        chaps.click()
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        chaps=driver.find_element(By.CSS_SELECTOR,"a[href='/order/3/']")
        chaps.click()
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 300);")
        browse=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-primary[href='/order_page/']")
        browse.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a.navbar-brand[href='/']")
        browse.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a.btn[href='/user_profile_view']")
        browse.click()
        time.sleep(2)
        



        # submit_button = driver.find_element(By.CSS_SELECTOR, "button.buy--btn")
        # submit_button.click()




    # Add more test methods as needed

if __name__ == '__main__':
    import unittest
    unittest.main()