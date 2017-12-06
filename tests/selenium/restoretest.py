# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException, WebDriverException, ElementNotInteractableException, InvalidSelectorException
import unittest, time, re, sys, os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC




class WebuiSeleniumTest(unittest.TestCase):
    def setUp(self):
        d = DesiredCapabilities.FIREFOX
        d['loggingPrefs'] = { 'browser':'ALL' }
        fp = webdriver.FirefoxProfile()
        fp.set_preference('webdriver.log.file', os.getcwd() + '/firefox_console')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(4)
        self.base_url = "http://%s" % targethost
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def test_restore(self):        
        
        # LOGGING IN:
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
        self.click_and_wait("/bareos-webui/restore/")
        
        
        # SELECTING CLIENT:
        # Selects the correct client
        self.click_element_and_wait("(//button[@type='button'])[3]")
        self.click_element_and_wait("//form[@id='restore']/div/div/p/div/div/ul/li/a")
        time.sleep(t)
        
        
        # CLICK ON FILE VIA CSS (broken):
        # Clicks on css element and waits
        # for them to load.
        # driver.find_element_by_css_selector("i.jstree-icon.jstree-ocl").click()
        # time.sleep(3)
        # driver.find_element_by_css_selector("#-39 > i.jstree-icon.jstree-ocl").click()
        # time.sleep(3)
        # driver.find_element_by_css_selector("#-13 > i.jstree-icon.jstree-ocl").click()
        # time.sleep(3)
        # driver.find_element_by_css_selector("#620_anchor > i.jstree-icon.jstree-checkbox").click()
        # time.sleep(3)
        # self.click_css_and_wait("-39", "jstree-ocl")
        # self.click_css_and_wait("-13", "jstree-ocl")
        # self.click_css_and_wait("620_anchor", ".jstree-checkbox")     
        
        
        # CLICK ON FILE VIA XPATH-POSITION
        # to be replaced by click_element_and_wait
        
        driver.find_element_by_xpath("//i").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li/ul/li/i").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li/ul/li/ul/li/i").click()
        time.sleep(3)
        driver.find_element_by_xpath("//li[6]/a/i").click()
        
        
        # CONFIRMATION:
        # Clicks on 'submit'
        self.click_element_and_wait("//input[@id='submit']")
        # Confirms alert that has text "Are you sure ?"
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Are you sure[\s\S]$")
        
        
        # LOGOUT:
        # Opens the dropdown menue and chooses logout        
        driver.find_element_by_link_text(username).click()
        time.sleep(2)
        driver.find_element_by_link_text("Logout").click()
        
        
        
    
    def click_and_wait(self, what):
        # current time is catched
        start_time = time.time()
        i=0
        # the url to compare the current url against
        url=self.base_url + what
        # xpath-reference is generated
        xpath="//a[contains(@href, '%s')]" % what
        # while the url is not the desired url
        # try to click on the xpath element
        # until the time is more than 10 seconds
        # and displays the time the test took.
        while (url not in self.driver.current_url) or i<10:
            try:
                self.driver.find_element_by_xpath(xpath).click()
            except (NoSuchElementException, ElementNotInteractableException) as e:
                print "error %s" % i
            time.sleep(1)
            i=i+1
            if(i==10):
                print "Generated timeout."
                return False
        timer = time.time() - start_time
        print url + " loaded after %s seconds." % timer
        
    # Works like click_and_wait but also
    # works with non-url's: the xpath
    # must be given as argument when calling.
    def click_element_and_wait(self, what):
        i=0
        while i<6 or False:
            try:
                self.driver.find_element_by_xpath(what)
            except (ElementNotInteractableException, NoSuchElementException) as e:
                print "Error: %s of 6" % i
            else:
                 time.sleep(1)
                 print "Try %s succeeded" % what
                 self.driver.find_element_by_xpath(what).click()
                 return True
            time.sleep(1)
            i=i+1
            if(i==6):
                print "Timeout while loading %s ." % what
        print "Element loaded after %s seconds." %i

    def click_css_and_wait(self, what, where):
        print what
        i=0
        css = "#%s > i.jstree-icon." % what
        css = css + "%s" % where
        print css
        while i<4:
            try:
                self.driver.find_element_by_css_selector(css).click()
            except InvalidSelectorException:
                print "error %s" % (i+1)
                time.sleep(1)
            i=i+1
            if(i==4):
                print "Timeout while loading %s ." % css
        print "Element loaded after %s seconds." %i
        
    def wait_for_jQuery(self):
        i=0
        while (self.driver.execute_script("return jQuery.active == 0") and i<10):
            print "loading..."
            time.sleep(1)
            i=i+1
            if i==10:
                return False
        return True
        
    def wait_for_element(self, what):
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, what))
        )            
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
    t = 3
    targethost = os.environ.get('VM_IP')
    if not targethost:
        targethost = "10.20.240.49"
    unittest.main()