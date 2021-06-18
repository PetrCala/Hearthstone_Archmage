import sys

#Define the folder with the python scripts for web scraping in order to import these scripts
sys.path.insert(0, 'C:\\Users\\AU451FE\\OneDrive - EY\\Desktop\\Python\\HSreplay_scraper\\Scripts')
from Analyzer import DeckAnalyzer as DA
from Selector import DeckSelector as DS

#External browser Selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Other useful packages
import sys
from bs4 import BeautifulSoup
import requests
import time
from datetime import date
import datetime
import pandas as pd
import numpy as np
import re #String search
import warnings

#Silence the deprecation warning when minimizing the external drivers
warnings.filterwarnings('ignore', category=DeprecationWarning)


class ArchetypeExtractor:
    '''Extract the class names and archetype codes for all avilable archetypes on the hsreplay.net website and
        store these in a data frame under the name 'archetype_codes.xlsx'
    '''
    def __init__(self, driver_path, minimized = True):
        self.driver_path = driver_path
        self.minimized = minimized
    
    def open_driver(self):
        '''Open an empty driver with the specified driver path
        '''
        if self.minimized == True:
            options = webdriver.ChromeOptions()
            options.set_headless(True) 
            self.driver = webdriver.Chrome(self.driver_path,options=options) 
        else:
            self.driver = webdriver.Chrome(self.driver_path)
            
        return None
    
    def open_website(self):
        '''Put in the information you wish to extract and open a website with a website containing said information
        '''
        self.open_driver()
        self.driver.get(f'https://hsreplay.net/decks')

        self.driver.maximize_window()

        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_class_name('css-flk0bs'))
            self.driver.find_element_by_class_name('css-flk0bs').click()
        except TimeoutException:
            raise Exception('The privacy window has not shown up; try running the script again')

        return None

    
    def get_archetypes(self):
        self.open_website()
        
        #Get the classes as a list of the html elements
        classes = self.driver.find_elements_by_xpath('//*[@id="player-class-filter"]/div/div[1]/span/div/img')
        
        df = pd.DataFrame()
        for c in classes:
            class_name = c.get_attribute('alt').lower()
            c.click()   #Go to the website of the class

            
            #Here goes the command to wait until the page loads
            archetype_names = self.driver.find_elements_by_xpath('//*[@id="player-class-filter"]/div/div[2]/div/ul/li/span')
            archetypes = []
            for a in archetype_names:
                arch_name = a.text
                a.click()
                url = A.driver.current_url
                arch_code = re.search('archetypes=(.+)', url).group(1)
                a.click()
                row = [class_name, arch_name, arch_code]
                archetypes.append(row)
                
            df = df.append(archetypes)
            
        df = df.reset_index(drop = True)
        self.driver.quit()
        
        return df
