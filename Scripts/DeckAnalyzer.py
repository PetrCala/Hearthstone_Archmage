#The core of the method
#!{sys.executable} -m pip install -U selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#Other useful packages
import sys
from bs4 import BeautifulSoup
import requests
import time
from datetime import date
import datetime
import pandas as pd
import numpy as np


class DeckAnalyzer:
    '''
    Insert the path to the driver and link for the deck hsreplay website and get an analysis of said deck
    
    Redownload the driver here if the version is outdated
    https://chromedriver.chromium.org/
    '''
    def __init__(self, driver_path, deck_code):
        self.deck_code = deck_code
        self.driver = webdriver.Chrome(executable_path = driver_path)
        self.driver.get(f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD')
        
        self.driver.maximize_window()      #Maximize the window
        
        self.title = self.driver.title.split()[:-2]     #Define the title of the deck
        self.title = ' '.join([str(item) for item in self.title])
        
        print("Waiting for the privacy settings window to pop up")       #Agree to the privacy settings
        time.sleep(1.5)

        try:
            agree = self.driver.find_element_by_class_name('css-flk0bs')
            agree.click()
        except:
            pass
        print("Privacy settings window closed")
        
    def get_card_info(self):
        '''
        Get the card mana count, name and card count as a list called 'cards'
        '''
        if not self.driver.current_url == f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD':
            self.driver.get(f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD')
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
                print('Error - the scraper is not reading the card information properly')
                break

        return cards
    
    def get_further_info(self):
        '''
        Get the remaining statistics about the cards in the deck and return these as a list called 'further_info'
        '''
        if not self.driver.current_url == f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD':
            self.driver.get(f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD')
            
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

        return further_info
    
    
    def get_card_info_df(self):
        '''
        Analyze the mulligan guide page of the deck and store this information in a data frame
        '''
        print(f'Generating the card info for deck {self.title}')
        card_info = self.get_card_info()
        further_info = self.get_further_info()
        df_card = pd.DataFrame(card_info, columns = ['Mana Cost', 'Card Name', 'Card Count'])
        df_further = pd.DataFrame(further_info, columns = ['Mulligan WR', 'Kept', 'Drawn WR', 
                                                           'Played WR', 'Turns Held', 'Turns Played'])
        df = pd.concat([df_card, df_further], axis = 1)
        
        return df
    
    
    def get_overview_df(self):
        '''
        Analyze the overview page of the deck and store this information in a data frame
        '''
        print(f'Generating the overview for deck {self.title}')
        if not self.driver.current_url == f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD&tab=overview':
            self.driver.get(f'https://hsreplay.net/decks/{self.deck_code}/#gameType=RANKED_STANDARD&tab=overview')
            
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
        return df
    
    def write_to_excel(self, today = date.today().strftime("%m-%d")):
        df1 = self.get_overview_df()
        df2 = self.get_card_info_df()
        
        with pd.ExcelWriter(f'C:/Users/AU451FE/OneDrive - EY/Desktop/Python/HSreplay Scraper/Data Frames/{self.title} {today}.xlsx') as writer:
            df1.to_excel(writer, sheet_name = 'Overview')
            df2.to_excel(writer, sheet_name = 'Card_Info')
