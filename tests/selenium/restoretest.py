# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException, WebDriverException, ElementNotInteractableException, InvalidSelectorException, ElementNotVisibleException
import unittest, time, re, sys, os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys





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
        
        
        driver = self.driver
        # LOGGING IN:
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
        
        # CHANGING TO RESTORE TAB:
        self.wait_for_url("/bareos-webui/restore/")
        
        
        time.sleep(2)
        # SELECTING CLIENT:
        # Selects the correct client
        self.wait_for_element(By.XPATH, "//p/div/button").click()
        self.wait_for_element(By.CSS_SELECTOR, "span.text").click()
             
        
        # FILE-SELECTION:
        # Clicks on file and navigates through the tree
        # by using the arrow-keys.
        self.wait_for_element(By.XPATH, "//a[contains(text(),'/')]").send_keys(Keys.ARROW_RIGHT)
        self.wait_for_element(By.XPATH, "//a[contains(text(),'etc/')]").send_keys(Keys.ARROW_RIGHT)
        self.wait_for_element(By.XPATH, "//a[contains(text(),'bareos/')]").send_keys(Keys.ARROW_RIGHT)
        self.wait_for_element(By.XPATH, "//a[contains(text(),'bconsole.conf')]").click()
        # send_keys(Keys.ENTER)

        # CONFIRMATION:
        # Clicks on 'submit'
        self.wait_for_element(By.XPATH, "//input[@id='submit']").click()
        # Confirms alert that has text "Are you sure ?"
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Are you sure[\s\S]$")

        # LOGOUT:
        self.wait_for_element(By.LINK_TEXT, username).click()
        self.wait_for_element(By.LINK_TEXT, "Logout").click()
                
    # This Method clicks and URL and waits
    # until the URL matches the desired URL.
    def wait_for_url(self, what):
        start_time = time.time()
        i=0
        # the url to compare the current url against
        url=self.base_url + what
        print url
        # xpath-reference is generated
        xpath="//a[contains(@href, '%s')]" % what
        # while the url is not the desired url
        # try to click on the xpath element
        # until the time is more than 10 seconds
        # and displays the time the test took.
        while (url not in self.driver.current_url) and i<10:
            try:
                self.driver.find_element_by_xpath(xpath)
            except (NoSuchElementException, ElementNotInteractableException) as e:
                print "error %s" % i
            else:
                time.sleep(1)
                print "Try %s succeeded" % what
                self.driver.find_element_by_xpath(xpath).click()
                return True
            time.sleep(1)
            i=i+1
            if(i==10):
                print "Generated timeout."
                return True
        timer = time.time() - start_time
        print url + " loaded after %s seconds." % timer

    def wait_for_element(self, by, value):
        i=10
        element=None
        while i>0 and element is None:
            try:
                tmp_element = self.driver.find_element(by, value)
                if tmp_element.is_displayed():
                    element = tmp_element
            except ElementNotInteractableException:
                print "Waiting since %s sec" % i
                time.sleep(1)
            except NoSuchElementException:
                print "NSE Waiting ince %s sec" % i                
                time.sleep(1)
            except ElementNotVisibleException:
                print "NSE Waiting ince %s sec" % i                
                time.sleep(1)
            i=i-1
                
        if(i==0):
            print "Timeout while loading %s ." % value
        else:
            print "Element loaded after %s seconds." %i
            print element
        return element

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

    # get attributes from environment if set
    # otherwise use defaults
    restorefile = os.environ.get('RESTOREFILE')
    if not restorefile:
        restorefile = '/usr/sbin/bconsole'
    client = os.environ.get('CLIENT')
    if not client:
        client = "  bareos-fd"
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