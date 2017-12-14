# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException, WebDriverException, ElementNotInteractableException
import unittest, time, re, sys, os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



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
        
    def broken_test_login(self):
        driver = self.driver
        driver.get(self.base_url + "/bareos-webui/auth/login")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_link_text("localhost-dir").click()
        driver.find_element_by_name("consolename").clear()
        driver.find_element_by_name("consolename").send_keys("admin")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("secret")
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.click_element_and_wait("//form[@id='login']/div[4]/div/div/div/div[2]/div/ul/li[2]/a/span")
        driver.find_element_by_id("submit").click()
        self.click_element_and_wait("//ul[2]/li[3]/a")
        self.click_and_wait("/bareos-webui/auth/logout")
 
    
    def test_menue(self): #delete 'deactivated_' to activate the test
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
        
        self.click_and_wait("/bareos-webui/director/")
        self.click_and_wait("/bareos-webui/schedule//")
        self.click_and_wait("/bareos-webui/schedule/status/")
        self.click_and_wait("/bareos-webui/storage/")
        self.click_and_wait("/bareos-webui/client/")
        self.click_and_wait("/bareos-webui/restore/")
        time.sleep(t)
        driver.find_element_by_css_selector("a.dropdown-toggle").click()
        driver.find_element_by_link_text("Logout").click()
        
    def test_restore(self):
        path.spit('/')
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
        time.sleep(t)
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        driver.find_element_by_link_text("bareos-fd").click()
        driver.find_element_by_xpath("//a[contains(text(),'/')]/parent::li/i").click()
        time.sleep(t)
        driver.find_element_by_xpath("//a[contains(@title, 'usr/')]/parent::li/i").click()
        time.sleep(t)
        driver.find_element_by_xpath("//a[contains(@title, 'sbin/')]/parent::li/i").click()
        time.sleep(t)
        driver.find_element_by_xpath("//a[@id='464_anchor']/i").click()
        time.sleep(t)
        driver.find_element_by_id("submit").click()
        time.sleep(t)
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Are you sure[\s\S]$")
        time.sleep(t)
        driver.find_element_by_css_selector("a.dropdown-toggle").click()
        time.sleep(t)
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
        while (url not in self.driver.current_url) and i<10:
            try:
                self.driver.find_element_by_xpath(xpath).click()
            except NoSuchElementException or ElementNotInteractableException:
                print "error %s" % i
            time.sleep(1)
            i=i+1
            if(i==10):
                print "Generated timeout."
                return False
        timer = time.time() - start_time
        print url + " loaded after %s seconds." % timer
        
    # Works like click_and_wait but also
    # works with non-url's - the xpath
    # must be given as argument when calling.
    def click_element_and_wait(self, what):
        i=0
        while i<4:
            try:
                self.driver.find_element_by_xpath(what).click()
            except ElementNotInteractableException:
                print "error %s" % i
            time.sleep(1)
            i=i+1
            if(i==4):
                print "Timeout while loading %s ." % what
        print "Element loaded after %s seconds." %i
    
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
    restorefile = os.environ.get('RESTOREFILE')
    if not restorefile:
        restorefile = '/usr/sbin/bconsole'
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