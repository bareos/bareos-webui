# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebuiSeleniumTest(unittest.TestCase):
    def setUp(self):
        d = DesiredCapabilities.FIREFOX
        d['loggingPrefs'] = { 'browser':'ALL' }
        fp = webdriver.FirefoxProfile()
        fp.set_preference('webdriver.log.file', os.getcwd() + '/firefox_console')
        self.driver = webdriver.Firefox(capabilities=d,firefox_profile=fp)
        self.driver.implicitly_wait(4)
        self.base_url = "http://%s" % targethost
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def test_bareos(self):
        driver = self.driver
        # on windows we have a different baseurl
        if os.getenv('DIST') == "windows":
            driver.get(self.base_url + "/")
        else:
            driver.get(self.base_url + "/bareos-webui/")
            
        Select(driver.find_element_by_name("director")).select_by_visible_text("localhost-dir")
        driver.find_element_by_name("consolename").clear()
        driver.find_element_by_name("consolename").send_keys(username)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_link_text("English").click()
        driver.find_element_by_id("submit").click()
        driver.find_element_by_xpath("//a[contains(@href, '/bareos-webui/director/')]").click()
        driver.find_element_by_xpath("//a[contains(@href, '/bareos-webui/director/messages')]").click()
        driver.find_element_by_xpath("//a[contains(@href, '/bareos-webui/schedule/')]").click()
        driver.find_element_by_xpath("//a[contains(@href, '/bareos-webui/schedule/status/')]").click()
        driver.find_element_by_xpath("//a[contains(@href, '/bareos-webui/storage/')]").click()
        driver.find_element_by_xpath("//a[contains(@href, '/bareos-webui/client/')]").click()
        driver.find_element_by_xpath("//a[contains(@href, '/bareos-webui/restore/')]").click()
        driver.find_element_by_css_selector("a.dropdown-toggle").click()
        driver.find_element_by_link_text("Logout").click()
        
    def test_webui_selenium(self):
        driver = self.driver
        driver.get(self.base_url + "/bareos-webui/auth/login")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_xpath("//form[@id='login']/div/div/div/div/div[2]/div/ul/li[2]/a/span").click()
        driver.find_element_by_name("consolename").clear()
        driver.find_element_by_name("consolename").send_keys(username)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_link_text("English").click()
        driver.find_element_by_xpath("//input[@id='submit']").click()
        driver.find_element_by_link_text("Restore").click()
        driver.find_element_by_css_selector("a[href*='restore']").click()
        driver.find_element_by_xpath("//a[contains(text(),'/')]/parent::li/i").click()
        driver.find_element_by_xpath("//a[contains(@title, 'usr/')]/parent::li/i").click()
        driver.find_element_by_xpath("//a[contains(@title, 'sbin/')]/parent::li/i").click()
        driver.find_element_by_xpath("//a[@id='464_anchor']/i").click()
        driver.find_element_by_id("submit").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Are you sure[\s\S]$")
        driver.find_element_by_css_selector("a.dropdown-toggle").click()
        driver.find_element_by_link_text("Logout").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":

    # get username from environment if set
    # otherwise use defaults
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    if not username:
        username = "admin"
    if not password:
        password = "secret"
    
    dateiId = "464_anchor"
    
    targethost = os.environ.get('VM_IP')
    if not targethost:
        targethost = "10.20.240.49"
    unittest.main()