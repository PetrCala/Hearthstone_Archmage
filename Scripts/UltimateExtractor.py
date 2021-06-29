#Installing packages onto the device
#!{sys.executable} -m pip install -U selenium

import sys

#Define the folder with the python scripts for web scraping in order to import these scripts
#sys.path.insert(0, 'C:\\Users\\hso20\\Python\\HSreplay_scraper\\Scripts')
sys.path.insert(0, 'C:\\Users\\AU451FE\\OneDrive - EY\\Desktop\\Python\\HSreplay_scraper\\Scripts')
from Analyzer import DeckAnalyzer as DA
from Selector import DeckSelector as DS
from Extractor import ArchetypeExtractor as AE

#External browser Selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
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
from os import path as path_os

#Silence the deprecation warning when minimizing the external drivers
warnings.filterwarnings('ignore', category=DeprecationWarning)

#driver_path = 'C:/Users/hso20/Python/HSreplay_scraper/chromedriver'
driver_path = 'C:/Users/AU451FE/OneDrive - EY/Desktop/Python/HSreplay_scraper/chromedriver'
deck_folder = 'C:/Users/AU451FE/OneDrive - EY/Desktop/Python/HSreplay_scraper/Data Frames/'
#deck_folder = 'C:/\Users/hso20/Python/HSreplay_scraper/Data Frames/'


class UltimateAnalyzer:
    '''Return data on all or some decks from the hsreplay website as a data frame.

        :attributes:
        - driver_path (str): The path to the driver, which the class uses to scrape data.
        - minimized (bool): Open the driver in a visible mode if true. Open it hidden if false.
        
        :usage:
            U = UltimateAnalyzer(driver_path = driver_path, minimized = True)  
    '''
    def __init__(self, driver_path, deck_folder, minimized = False):
        '''
        The constructor for UltimateAnalyzer class.
        
        :attributes:
        - driver_path (str): The path to the driver, which the class uses to scrape data.
        - deck_folder (str): The path to the folder where the generated data should be stored.
        - minimized (bool): Open the driver in a visible mode if true. Open it hidden if false.
        
        :warning:
        - Using a headless (minimized) browser will result in a substantial CPU usage increase.
        '''
        self.driver_path = driver_path
        self.deck_folder = deck_folder
        self.minimized = minimized

    def open_driver(self):
        '''Open an empty driver with the specified driver path.

        :returns:
        - None: An open empty driver.
        '''
        if self.minimized == True:
            options = webdriver.ChromeOptions()
            options.set_headless(True) 
            self.driver = webdriver.Chrome(self.driver_path,options=options) 
        else:
            self.driver = webdriver.Chrome(self.driver_path)

        return None
    
    def open_website(self, link = f'https://hsreplay.net/decks'):
        '''Insert a link and open a website using said link.
                
        :args:
        - link (str): The link to open the website on. Set to f'https://hsreplay.net/decks' by default.
        
        :usage:
            self.open_website(f'https://hsreplay.net/decks')
            
        :returns:
        - None: An open website using a specified link.
        
        '''
        self.open_driver()
        self.driver.get(link)

        self.driver.maximize_window()

        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_class_name('css-flk0bs'))
            self.driver.find_element_by_class_name('css-flk0bs').click()
        except TimeoutException:
            raise Exception('The privacy window has not shown up; try running the script again')

        print('Website successfuly opened')    
        return None
    
    def get_card_info(self):
        '''Analyze the mulligan guide page of a deck and store this information in a data frame.
        
        :assumptions:
        - An already opened driver with a window containing the mulligan guide information.

        :usage:
            (self.open_website(specify_link_here)) -> self.get_card_info()
            
        :returns:
        - df (pd.DataFrame): A data frame containing data about the cards from a given deck.
        '''
        #Generating the card names data
        card_names = self.driver.find_elements_by_class_name('table-row-header')
        cards = []
        for c in card_names:
            info = c.text
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

        #Generating the card details data
        data = self.driver.find_elements_by_class_name('table-cell')
        further_info = []
        for d in range(int(len(data)/6)):
            try:
                mull_wr = data[0+6*d].text.replace('▼', '').replace('▲', '')
                per_kept = data[1+6*d].text
                drawn_wr = data[2+6*d].text.replace('▼', '').replace('▲', '')
                played_wr = data[3+6*d].text.replace('▼', '').replace('▲', '')
                turns_held = float(data[4+6*d].text)
                turns_played = float(data[5+6*d].text)
            
                row = [mull_wr, per_kept, drawn_wr, played_wr, turns_held, turns_played]
            except ValueError:
                print('Some cards in this deck contain missing data')
                row = []
                
            further_info.append(row)

        #Concatenating the two data frames together    
        df_card = pd.DataFrame(cards, columns = ['Mana Cost', 'Card Name', 'Card Count'])
        df_further = pd.DataFrame(further_info, columns = ['Mulligan WR', 'Kept', 'Drawn WR', 
                                                           'Played WR', 'Turns Held', 'Turn Played'])
        
        df = pd.concat([df_card, df_further], axis = 1)
        
        return df

        
    def get_overview(self):
        '''Analyze the overview page of a deck and store this information in a data frame.
        
        :assumptions:
        - An already opened driver with a window containing the overview information.

        :usage:
            (self.open_website(specify_link_here)) -> self.get_overview()
            
        :returns:
        - df (pd.DataFrame): A data frame containing an overview a given deck. (e.g., deck code, win rates, game sample size)
        '''
        data = self.driver.find_elements_by_xpath("//tr/td[2]")
        url = self.driver.current_url
        code = re.search('decks/(.+?)/#tab', url).group(1)
        
        overview = []
        overview.append(code)
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

    
    def get_archetype_data(self, class_name, arch_name):
        '''Specify the name for the archetype and return the data from the hsreplay website for t given archetype
        
        :args:
        - class_name (str): Name of the class.
        - arch_name (str): Name of the archetype.

        :usage:
            self.driver.get_archetype_data(class_name = 'Rogue', arch_name = 'Miracle Rogue')
            
        - The method is case sensitive. An wrongly formatted input returns error.
                         
        :returns:
        - data_frames (pandas.DataFrame): A data frame containing data for the given archetype.
        '''
        #Pre-processing and identifying the data        
        class_codes = {'Demon Hunter' : 1, 'Druid' : 2, 'Hunter' : 3, 'Mage' : 4, 'Paladin' : 5,
                       'Priest' : 6, 'Rogue' : 7 , 'Shaman' : 8, 'Warlock' : 9, 'Warrior' : 10}
       
        class_index = class_codes.get(class_name)
        
        if class_index == None:
            raise Exception('The class name is not correctly specified (e.g. Demon Hunter, Warlock, etc.)')
        else:
            pass
            
        
        #The actual process
        self.open_website()
        
        #Open the page for the specified archetype
        u = WebDriverWait(self.driver, 8)
        u.until(EC.presence_of_element_located((By.CLASS_NAME,"deck-tile")))
        
        xpath_class = f'//*[@id="player-class-filter"]/div/div[1]/span[{class_index}]/div/img'
        x = self.driver.find_element_by_xpath(xpath_class)
        x.click()
        
        
        xpath_arch = f'//*[@id="player-class-filter"]/div/div[2]/div/ul/li/span[text() = "{arch_name}"]'
        y = U.driver.find_element_by_xpath(xpath_arch)
        y.click()
        
        deck_amount = len(self.driver.find_elements_by_xpath('//*[@id="decks-container"]/main/div[3]/section/ul/li/a'))
                
        #Generate the card info for each of the decks of a given archetype
        data_frames = []
        
        overviews_df = pd.DataFrame()
        
        for d in range(deck_amount):
            u = WebDriverWait(self.driver, 8)
            u.until(EC.presence_of_element_located((By.CLASS_NAME,"deck-tile")))

            index = d + 2
            xpath_deck = f'//*[@id="decks-container"]/main/div[3]/section/ul/li[{index}]/a'
            l = self.driver.find_element_by_xpath(xpath_deck)
            l.click()

            u.until(EC.presence_of_element_located((By.CLASS_NAME,"sort-header__title")))   

            card_info = self.get_card_info()
            data_frames.append(card_info)

            #Switch to overview
            overview_button = self.driver.find_element_by_id('tab-overview')
            overview_button.click()

            u.until(EC.presence_of_element_located((By.CLASS_NAME,"winrate-cell")))

            overview = self.get_overview()
            overviews_df = overviews_df.append(overview)

            deck_position = d + 1
            print(f'Generated data for {deck_position}/{deck_amount} decks of archetype {arch_name}')
            self.driver.back()
        
        data_frames.insert(0, overviews_df)  
        self.driver.quit()
        
        return data_frames
    
        
    def archetype_to_excel(self, class_name, arch_name):
        '''Specify the class name, archetype name and folder path
        and return an excel file with all informations about said archetype in said folder
        
        :args:
        - class_name (str): Name of the class.
        - arch_name (str): Name of the archetype.
        
        :usage:
            self.archetype_to_excel(class_name = 'Rogue', archetype = 'Miracle Rogue',
            'path' = )
        
        
        '''
        today = date.today().strftime("%m-%d")
        path_partial = f'{self.deck_folder}{today}'
        
        #Assert the existence of a folder into which to add the data
        if not path_os.exists(path_partial):
            os.makedirs(path_partial)
            print(f'Creating a folder {today} where the data will be stored')
        
        #Get the archetype data
        df = self.get_archetype_data(class_name, arch_name)
        
        #Get the number of data frames to write into excel
        sheet_n = len(df)    

        #Write these data frames into excel
        path = f'{path_partial}/{class_name} - {arch_name} {today}.xlsx'
        with pd.ExcelWriter(path) as writer:
             for i in range(sheet_n):
                    df[i].to_excel(writer, sheet_name = f'{i}', index = False)


        return df
    
    def get_all_data(self, classes_skip = 0):
        '''Return all the data from the hsreplay website as several data frames.
        The data is chronologically collected in the order:
        Demon Hunter, Druid, Hunter, Mage, Paladin, Priest, Rogue, Shaman, Warlock, Warrior.
        
        :args:
        - classes_skip (int): Define how many classes to skip when collecting the data.
        '''
        today = date.today().strftime("%m-%d")
        path_partial = f'{self.deck_folder}{today}'

        #Assert the existence of a folder into which to add the data
        if not path_os.exists(path_partial):
            os.makedirs(path_partial)
            print(f'Creating a folder {today} where the data will be stored')
                    
        self.open_website()
        
        #Get the classes as a list of the html elements
        u = WebDriverWait(self.driver, 8)
        u.until(EC.presence_of_element_located((By.CLASS_NAME,"deck-tile")))
        
        classes_len = len(self.driver.find_elements_by_xpath('//*[@id="player-class-filter"]/div/div[1]/span/div/img'))
        for c in range(classes_len):
            index = c + classes_skip + 1
            xpath_class = f'//*[@id="player-class-filter"]/div/div[1]/span[{index}]/div/img'
            c = self.driver.find_element_by_xpath(xpath_class)
            
            class_name = c.get_attribute('alt').lower()
            c.click()   #Go to the website of the class

            
            archetype_length = len(self.driver.find_elements_by_xpath('//*[@id="player-class-filter"]/div/div[2]/div/ul/li/span'))
            for a in range(archetype_length):
                index = a + 1
                xpath_arch = f'//*[@id="player-class-filter"]/div/div[2]/div/ul/li[{index}]/span'
                k = self.driver.find_element_by_xpath(xpath_arch)
                k.click()
                
                data_frames = []
                arch_name = k.text
                
                url = U.driver.current_url
                arch_code = re.search('archetypes=(.+)', url).group(1)

                overviews_df = pd.DataFrame()

                deck_amount = len(self.driver.find_elements_by_xpath('//*[@id="decks-container"]/main/div[3]/section/ul/li/a'))
                
                #Generate the card info for each of the decks of a given archetype
                for d in range(deck_amount):
                    u = WebDriverWait(self.driver, 8)
                    u.until(EC.presence_of_element_located((By.CLASS_NAME,"deck-tile")))
                
                    index = d + 2
                    xpath_deck = f'//*[@id="decks-container"]/main/div[3]/section/ul/li[{index}]/a'
                    l = self.driver.find_element_by_xpath(xpath_deck)
                    l.click()
                           
                    u.until(EC.presence_of_element_located((By.CLASS_NAME,"sort-header__title")))   
                        
                    card_info = self.get_card_info()
                    data_frames.append(card_info)

                    #Switch to overview
                    overview_button = self.driver.find_element_by_id('tab-overview')
                    overview_button.click()

                    u.until(EC.presence_of_element_located((By.CLASS_NAME,"winrate-cell")))
                    
                    overview = self.get_overview()
                    overviews_df = overviews_df.append(overview)

                    deck_position = d + 1
                    print(f'Generated data for {deck_position}/{deck_amount} decks of archetype {arch_name}')
                    self.driver.back()
                    

                u = WebDriverWait(self.driver, 8)
                u.until(EC.presence_of_element_located((By.CLASS_NAME,"deck-tile")))
                
                k = self.driver.find_element_by_xpath(xpath_arch)
                k.click()

                #Add the overview data frame to the beginning of the list
                data_frames.insert(0, overviews_df)
                
                #Get the number of data frames to write into excel
                sheet_n = len(data_frames)    

                #Write these data frames into excel
                path = f'{path_partial}/{class_name} - {arch_name} {today}.xlsx'
                with pd.ExcelWriter(path) as writer:
                    for i in range(sheet_n):
                        data_frames[i].to_excel(writer, sheet_name = f'{i}', index = False)

        self.driver.quit()
        
        return data_frames