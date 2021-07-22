#External browser Selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Other useful packages
import sys
from datetime import date
import pandas as pd
import numpy as np
import re
import warnings
import os

#Silence the deprecation warning when minimizing the external drivers
warnings.filterwarnings('ignore', category=DeprecationWarning)

class DataExtractor:
    '''Extract data from the hsreplay.net website for either some or all archetypes in the game.
    '''
    def __init__(self):
        '''
        The constructor for DataExtractor class. 
        '''
        #Defining file paths
        self.base_path = re.search(f'(.+)Hearthstone_Archmage', os.getcwd()).group(1)\
            + 'Hearthstone_Archmage'
        script_path = self.base_path + '\Scripts'
        if script_path not in sys.path:
            sys.path.insert(0, script_path) 
               
        self.driver_path = f'{self.base_path}\chromedriver'
        self.deck_folder = f'{self.base_path}\Data Frames'
        self.analysis_path = f'{self.base_path}\Analyzed' 

    def open_driver(self):
        '''Open an empty driver with the specified driver path.

        :returns:
        - None: An open empty driver.
        '''
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

        print('Website successfully opened')    
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
        url = self.driver.current_url
        
        name_of_class = self.driver.find_element_by_xpath('//*[@id="deck-container"]/div/aside/ul/li[1]/a').text
        try:
            name_of_deck = self.driver.find_element_by_xpath('//*[@id="deck-container"]/div/aside/ul/li[2]/span/a').text
        except:
            name_of_deck = 'Other'
        code = re.search('decks/(.+?)/', url).group(1)
        date_of_deck = date.today()
        
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

                row = [name_of_class, name_of_deck, code, date_of_deck, mana_cost, card_name, card_count]
                cards.append(row)
            elif len(txt) == 2:
                mana_cost = int(txt[0])
                card_name = txt[1]
                card_count = 1

                row = [name_of_class, name_of_deck, code, date_of_deck, mana_cost, card_name, card_count]
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
        df_card = pd.DataFrame(cards, columns = ['Class', 'Deck Name', 'Deck Code', 'Date',
                                                 'Mana Cost', 'Card Name', 'Card Count'])
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
        
        name_of_class = self.driver.find_element_by_xpath('//*[@id="deck-container"]/div/aside/ul/li[1]/a').text
        try:
            name_of_deck = self.driver.find_element_by_xpath('//*[@id="deck-container"]/div/aside/ul/li[2]/span/a').text
        except:
            name_of_deck = 'Other'
        code = re.search('decks/(.+?)/', url).group(1)
        date_of_deck = date.today()

        overview = [name_of_class, name_of_deck, code, date_of_deck]
        for d in data:
            text = d.text.replace('▼', '').replace('▲', '')
            overview.append(text)
        
        #Add sample size manually
        sample_size = int(self.driver.find_element_by_xpath("//*[@id='deck-container']/div/aside/section/ul/li[1]/span").text.replace(' games', '').replace(',',''))
        overview.append(sample_size)
        
        overview = [overview]
        
        df = pd.DataFrame(overview, columns = ['Class', 'Deck Name', 'Deck Code', 'Date', 
                                               'Match Duration', 'Turns', 'Turn Duration', 'Overall Winrate',
                                               'vs. Demon Hunter', 'vs. Druid', 'vs. Hunter',
                                               'vs. Mage', 'vs. Paladin', 'vs. Priest', 'vs. Rogue',
                                               'vs. Shaman', 'vs. Warlock', 'vs. Warrior', 'Sample Size'])

        return df

    
    def get_archetype_data(self, class_name, arch_name):
        '''Specify the name for the archetype and return the data from the hsreplay website for the given archetype.
        
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
        class_name = class_name.title()
        arch_name = arch_name.title()     
                
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
        y = self.driver.find_element_by_xpath(xpath_arch)
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

            try:
                u.until(EC.presence_of_element_located((By.CLASS_NAME,"sort-header__title")))  

                card_info = self.get_card_info()
                data_frames.append(card_info)
            except:
                print('This deck is missing card data')
                pass

            #Switch to overview
            overview_button = self.driver.find_element_by_id('tab-overview')
            overview_button.click()
            
            try:
                u.until(EC.presence_of_element_located((By.CLASS_NAME,"winrate-cell")))

                overview = self.get_overview()
                overviews_df = overviews_df.append(overview)
            except:
                print('This deck is missing overview data')
                pass

            deck_position = d + 1
            print(f'Extracted data for {deck_position}/{deck_amount} decks of archetype {arch_name}')
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
        class_name = class_name.title()
        arch_name = arch_name.title()
        
        today = date.today().strftime("%m-%d")
        path_partial = f'{self.deck_folder}/{today}'
        
        #Assert the existence of a folder into which to add the data
        if not os.path.exists(path_partial):
            os.makedirs(path_partial)
            print(f'Creating a folder {today} where the data will be stored')
        
        #Get the archetype data
        df = self.get_archetype_data(class_name, arch_name)
        
        #Get the number of data frames to write into excel
        sheet_n = len(df)    

        #Write these data frames into excel
        path = f'{self.deck_folder}/{today}/{class_name} - {arch_name} {today}.xlsx'
        with pd.ExcelWriter(path) as writer:
             for i in range(sheet_n):
                if i == 0:
                    df[i].to_excel(writer, sheet_name = 'Overview', index = False)
                else:
                    index = i - 1
                    temp = df[0].reset_index()
                    deck_code = temp.loc[index, 'Deck Code']
                    df[i].to_excel(writer, sheet_name = f'{deck_code}', index = False)
        print('All done')
                    
        return df
    
    def get_all_data(self, classes_skip = 0):
        '''Return all the data from the hsreplay website as several data frames.
        The data is chronologically collected in the order:
        Demon Hunter, Druid, Hunter, Mage, Paladin, Priest, Rogue, Shaman, Warlock, Warrior.
        
        :args:
        - classes_skip (int): Define how many classes to skip when collecting the data.
        '''
        today = date.today().strftime("%m-%d")
        path_partial = f'{self.deck_folder}/{today}'

        #Assert the existence of a folder into which to add the data
        if not os.path.exists(path_partial):
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
            
            class_name = c.get_attribute('alt').title()
            c.click()   #Go to the website of the class

            
            archetype_length = len(self.driver.find_elements_by_xpath('//*[@id="player-class-filter"]/div/div[2]/div/ul/li/span'))
            for a in range(archetype_length):
                index = a + 1
                xpath_arch = f'//*[@id="player-class-filter"]/div/div[2]/div/ul/li[{index}]/span'
                k = self.driver.find_element_by_xpath(xpath_arch)
                k.click()
                
                data_frames = []
                arch_name = k.text.title()
                
                url = self.driver.current_url
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
                           
                    try:
                        u.until(EC.presence_of_element_located((By.CLASS_NAME,"sort-header__title")))  

                        card_info = self.get_card_info()
                        data_frames.append(card_info)
                    except:
                        print('This deck is missing card data')
                        pass 

                    #Switch to overview
                    overview_button = self.driver.find_element_by_id('tab-overview')
                    overview_button.click()

                    try:
                        u.until(EC.presence_of_element_located((By.CLASS_NAME,"winrate-cell")))

                        overview = self.get_overview()
                        overviews_df = overviews_df.append(overview)
                    except:
                        print('This deck is missing overview data')
                        pass

                    deck_position = d + 1
                    print(f'Extracted data for {deck_position}/{deck_amount} decks of archetype {arch_name}')
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
                        if i == 0:
                            data_frames[i].to_excel(writer, sheet_name = 'Overview', index = False)
                        else:
                            index = i - 1
                            temp = data_frames[0].reset_index()
                            deck_code = temp.loc[index, 'Deck Code']
                            data_frames[i].to_excel(writer, sheet_name = f'{deck_code}', index = False)

        self.driver.quit()
        print('All done')
        
        return data_frames