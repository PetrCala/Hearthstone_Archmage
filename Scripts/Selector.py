#Installing packages onto the device
#!{sys.executable} -m pip install -U selenium

import sys

#Python scripts for web scraping
sys.path.insert(0, 'C:\\Users\\AU451FE\\OneDrive - EY\\Desktop\\Python\\HSreplay_scraper\\Scripts')
from Analyzer import DeckAnalyzer as DA

#External browser Selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Other useful packages

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


class DeckSelector:
    '''Define the class and archetype of a deck at hsreplay.net and return the analysis of the decks of said archetype
        featured on that website
        
        deck_class = name of the class in quotes (e.g. 'Druid')
        deck_archetype = code for the archetype in quotes (e.g. '372')
    '''
    def __init__(self, driver_path, deck_class, deck_archetype, minimized = True):
        self.driver_path = driver_path
        self.deck_archetype = deck_archetype
        self.deck_class = deck_class.upper()    #Converting the deck_class into upper case
        self.minimized = minimized
        self.url = f'https://hsreplay.net/decks/#playerClasses={self.deck_class}&gameType=RANKED_STANDARD&archetypes={self.deck_archetype}'

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
        
    def get_codes(self):
        '''Return codes of the decks  in a list for a certain archetype
        '''
        self.open_driver()  
        
        self.driver.get(self.url) 
        self.driver.maximize_window()      #Maximize the window

        #Closing the privacy settings window
        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_class_name('css-flk0bs'))
            self.driver.find_element_by_class_name('css-flk0bs').click()
        except TimeoutException:
            raise Exception('The privacy window has not shown up; try running the script again')
        
        
        #Looks for the codes of the specified archetype
        list_decks = self.driver.find_elements_by_class_name('deck-tile')
        
        codes = []
        for l in list_decks:
            link = l.get_attribute('href')

            try:
                m = re.search('decks/(.+?)/#game', link).group(1)

            except AttributeError:
                print(f'The entered URL is invalid')
                break
            codes.append(m)

        self.codes = codes    
        print('The codes are stored under the variable codes')
        
        #Get the archetype name
        self.archetype_name = self.driver.find_element_by_xpath('//*[@id="decks-container"]/main/div[3]/section/ul/li[2]/a/div/div[1]/h3').text
        self.driver.quit()
        
        return None
    
    def get_overviews_df(self):
        '''Return a data frame with an overview of all decks of a given archetype
        '''
        self.get_codes()
        overviews_df = pd.DataFrame()
        for c in self.codes:
            D = DA(self.driver_path, c)
            df = D.get_overview_df()
            overviews_df = pd.concat([overviews_df, df], axis = 0)
            
            deck_position = self.codes.index(c) + 1
            print(f'Generated data for {deck_position}/{len(self.codes)} decks of archetype {self.archetype_name}')
            
        overviews_df = overviews_df.reset_index(drop = True)
        return overviews_df
    
    def write_to_excel(self, today = date.today().strftime("%m-%d")):
        df = self.get_overviews_df()
        
        with pd.ExcelWriter(f'C:/Users/AU451FE/OneDrive - EY/Desktop/Python/HSreplay_Scraper/Data Frames/{self.archetype_name} {today}.xlsx') as writer:
            df.to_excel(writer, sheet_name = 'Overview')

