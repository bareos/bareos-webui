# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re, sys, os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

start_time = time.time()

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
        
    def test_login(self):
        driver = self.driver
        driver.get(self.base_url + "/bareos-webui/auth/login")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_link_text("localhost-dir").click()
        driver.find_element_by_name("consolename").clear()
        driver.find_element_by_name("consolename").send_keys("admin")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("secret")
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//form[@id='login']/div[4]/div/div/div/div[2]/div/ul/li[2]/a/span").click()
        driver.find_element_by_id("submit").click()
        self.click_element_and_wait("//ul[2]/li[3]/a")
 
    
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
        i=0
        url=self.base_url + what #Eine URL zum Vergleich mit der momentanen wird generiert
        dest="//a[contains(@href, '%s')]" % what #Die XPATH-Referenz wird generiert
        while (url not in self.driver.current_url) and i<10:
            time.sleep(1) #Falls die URL nicht der Erwartung entspricht -> warte eine Sekunde
            self.driver.find_element_by_xpath(dest).click() #Klicke erneut auf die URL
            i=i+1 #Addiere 1 zum Laufzeitzähler der gleichzeitig als Abbruchkriterium dient
            if(i==10):
                print "Timeout beim laden generiert." #Falls i zu diesem Zeitpunkt 10 beträgt wird es keine weitere Ausführung geben ->Timeout
        print url + " nach %s Sekunden geladen." %i #In der Konsole wird angezeigt wie schnell die URL geladen wurde
        
    def click_element_and_wait(self, what): #Erklärt sich durch click_and_wait
        i=0
        while i<4:
            time.sleep(1)
            self.driver.find_element_by_xpath(what).click()
            i=i+1
            if(i==4):
                print "Timeout beim laden von %s generiert." % what
        print "Element nach %s Sekunden geladen." %i    
    
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