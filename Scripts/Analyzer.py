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
import warnings


#Silence the deprecation warning when minimizing the external drivers
warnings.filterwarnings('ignore', category=DeprecationWarning)



class DeckAnalyzer:
    '''
    Insert the path to the driver and link for the deck hsreplay website and get an analysis of said deck
    
    Redownload the driver here if the version is outdated
    https://chromedriver.chromium.org/
    '''
    def __init__(self, driver_path, deck_code, minimized = True):
        self.driver_path = driver_path
        self.deck_code = deck_code
        self.minimized = minimized
        self.title = deck_code
        #self.title = self.driver.title.split()[:-2]     #Define the title of the deck
        #self.title = ' '.join([str(item) for item in self.title])
    
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
        
    def open_website(self, information):
        '''Put in the information you wish to extract and open a website with a website containing said information
        '''
        self.open_driver()
        if information == 'Overview':
            self.driver.get(f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD&tab=overview')
        elif information == 'Card info':
            self.driver.get(f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD')
        else:
            raise Exception(f'The desired information is not specified properly.')
        
        self.driver.maximize_window()

        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_class_name('css-flk0bs'))
            self.driver.find_element_by_class_name('css-flk0bs').click()
        except TimeoutException:
            raise Exception('The privacy window has not shown up; try running the script again')

        return None
        
    def get_card_info(self):
        '''
        Get the card mana count, name and card count as a list called 'cards'
        '''
        self.open_website('Card info')
        data = self.driver.find_elements_by_class_name('table-row-header')
        cards = []
        for d in data:
            info = d.text
            txt = info.rsplit('\n')
            if len(txt) == 3:
                mana_cost = int(txt[0])
                card_name = txt[2]
                card_count = int(txt[1].replace('★', '1'))

                row = [mana_cost, card_name, card_count]
                cards.append(row)
            elif len(txt) == 2:
                mana_cost = int(txt[0])
                card_name = txt[1]
                card_count = 1
                
                row = [mana_cost, card_name, card_count]
                cards.append(row)
            else:
                raise Exception('Error - the scraper is not reading the card information properly')
                
        self.driver.quit()
        return cards
    
    def get_further_info(self):
        '''
        Get the remaining statistics about the cards in the deck and return these as a list called 'further_info'
        '''
        self.open_website('Card info')           
        
        data = self.driver.find_elements_by_class_name('table-cell')
        further_info = []
        for f in range(int(len(data)/6)):
            mull_wr = data[0+6*f].text.replace('▼', '').replace('▲', '')
            per_kept = data[1+6*f].text
            drawn_wr = data[2+6*f].text.replace('▼', '').replace('▲', '')
            played_wr = data[3+6*f].text.replace('▼', '').replace('▲', '')
            turns_held = float(data[4+6*f].text)
            turns_played = float(data[5+6*f].text)
            
            row = [mull_wr, per_kept, drawn_wr, played_wr, turns_held, turns_played]
            further_info.append(row)
    
        self.driver.quit()    
        return further_info
    
    
    def get_card_info_df(self):
        '''
        Analyze the mulligan guide page of the deck and store this information in a data frame
        '''
        print(f'Generating the card info for deck {self.title}')
        card_info = self.get_card_info()
        print(f'Card info obtained')
        further_info = self.get_further_info()
        print(f'Further info obtained')
        df_card = pd.DataFrame(card_info, columns = ['Mana Cost', 'Card Name', 'Card Count'])
        df_further = pd.DataFrame(further_info, columns = ['Mulligan WR', 'Kept', 'Drawn WR', 
                                                           'Played WR', 'Turns Held', 'Turns Played'])
        
        df = pd.concat([df_card, df_further], axis = 1)
        print(f'Final data frame generated')
        return df
    
    
    def get_overview_df(self):
        '''
        Analyze the overview page of the deck and store this information in a data frame
        '''
        print(f'Generating the overview')
        self.open_website('Overview')
        
        data = self.driver.find_elements_by_xpath("//tr/td[2]")
        
        overview = []
        overview.append(self.deck_code)
        for d in data:
            text = d.text.replace('▼', '').replace('▲', '')
            overview.append(text)
        
        #Add sample size manually
        sample_size = int(self.driver.find_element_by_xpath("//*[@id='deck-container']/div/aside/section/ul/li[1]/span").text.replace(' games', '').replace(',',''))
        overview.append(sample_size)
        
        overview = [overview]
        
        df = pd.DataFrame(overview, columns = ['Deck Code', 'Match Duration', 'Turns', 'Turn Duration', 'Overall Winrate',
                                               'vs. Demon Hunter', 'vs. Druid', 'vs. Hunter',
                                               'vs. Mage', 'vs. Paladin', 'vs. Priest', 'vs. Rogue',
                                               'vs. Shaman', 'vs. Warlock', 'vs. Warrior', 'Sample Size'])
        
        self.driver.quit()
        return df
    
    def write_to_excel(self, today = date.today().strftime("%m-%d")):
        df1 = self.get_overview_df()
        df2 = self.get_card_info_df()
        
        with pd.ExcelWriter(f'C:/Users/AU451FE/OneDrive - EY/Desktop/Python/HSreplay_Scraper/Data Frames/{self.title} {today}.xlsx') as writer:
            df1.to_excel(writer, sheet_name = 'Overview')
            df2.to_excel(writer, sheet_name = 'Card_Info')
