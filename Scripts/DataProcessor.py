#Importing the data extractor scripts
import sys
sys.path.insert(0, 'C:\\Users\\AU451FE\\OneDrive - EY\\Desktop\\Python\\Hearthstone_Archmage\\Scripts')

#import Extractors
#from UltimateExtractor import UltimateExtractor as UE

#Other useful packages
import time
import datetime
import pandas as pd
import numpy as np
import re #String search
import os

driver_path = r'C:\Users\AU451FE\OneDrive - EY\Desktop\Python\Hearthstone_Archmage\chromedriver'
deck_folder = r'C:\Users\AU451FE\OneDrive - EY\Desktop\Python\Hearthstone_Archmage\Data Frames'
analysis_path = r'C:\Users\AU451FE\OneDrive - EY\Desktop\Python\Hearthstone_Archmage\Data Frames\Analyzed'

#driver_path = r'C:\Users\hso20\Python\HSreplay_scraper\chromedriver'
#deck_folder = r'C:\Users\hso20\Python\HSreplay_scraper\Data Frames'
#analysis_path = r'C:\Users\hso20\Python\HSreplay_scraper\Data Frames\Analyzed'

class DataProcessor:
    '''Transform the extracted data to be used in further analysis and modelling.
    '''
    def __init__(self, deck_folder, analysis_path):
        '''The constructor for DataProcessor class.
        
        :attributes:
        - deck_folder (str): The path to the folder where the generated data is stored. Input folder.
        - analysis_path (str): The path to the folder where the processed data should be stored. Output folder.
        
        :usage:
            P = DataProcessor(driver_path = driver_path, analysis_path = analysis_path)  
        '''
        self.deck_folder = deck_folder
        self.analysis_path = analysis_path
        
    def percentage_to_float(self, number):
        '''Input a number or a series of numbers and transform these to float or a series of floats.
        
        :args:
        - number (str or series): The data which should be transformed to float.
        
        :usage:
            self.percentage_to_float('69.8%')
            
        :returns:
        - number (float or series of floats): The input transformed into float or a series of floats.
        '''
        try:
            number = number.str.strip('%').astype(float)/100 #For series
        except AttributeError:
            number = float(number.strip('%'))/100 #For single numbers
        
        return number
    
    def load_data(self, date, deck = None, class_name = None):
        '''Specify the date and a deck name or a class, then load the data from the data repository and return
            this data as either a data frame or a list of data frames, along with the deck keys in similar form.
            Lastly, return names of the decks in a list.
            
        :args:
        - date (str): A date from which to load the data.
        - class_name (str): A class or a list of classes for which to load the data.
        - deck (str): A deck for which to load the data for. If set to None, load the data for all decks.
        
        :usage:
            self.load_data('07-01', deck = 'Rogue - Miracle Rogue')
            ~
            self.load_data('07-01', class_name = 'Rogue')            
            ~
            self.load_data('07-01')
            
        :returns:
        - data (pd.DataFrame or list): Either a pandas data frame (if deck is specified) or a list of these
            data frames, which contain all deck information.
        - data_keys (list): Either a list or a nested list of deck data sheet names, which serve
            to further extract data from individual sheets.
        - deck_names (string or list): Names of decks included in loaded data. Returned either as a string
            if a single deck is analyzed, or as a list, if multiple decks are analyzed.
        '''
        deck_folder_date = f'{self.deck_folder}/{date}'.replace('/', '\\') 
        file_paths = list()
        file_names = list()
        for (dirpath, dirnames, filenames) in os.walk(deck_folder_date):
            file_paths += [os.path.join(dirpath, file) for file in filenames]
            file_names += [re.search(f'(.+) ', file).group(1) for file in filenames]
            
        #Load a single deck    
        if deck != None:
            deck = deck.title()
            file_index = file_names.index(deck)
            data = pd.read_excel(file_paths[file_index], sheet_name = None)
            
            data_keys = list()
            [data_keys.append(key) for key in data]
            
            deck_names = deck
        
        #Load all decks for a specified class
        elif class_name != None:
            if type(class_name) == list:
                class_name = [c.title() for c in class_name]
            else:
                class_name = class_name.title()
            class_names = []
            class_names += [re.search(f'(.+) -', file).group(1) for file in file_names]
            
            data = []
            data_keys = []
            deck_names = []
            for i in range(len(class_names)):
                if class_names[i] in class_name:
                    temp = pd.read_excel(file_paths[i], sheet_name = None)
                    data.append(temp)
                    temp_keys = list()
                    [temp_keys.append(key) for key in temp]
                    data_keys.append(temp_keys)
                    deck_names.append(file_names[i]) 
        
        #Load all decks
        else:
            data = []
            data_keys = []
            for file in file_paths:
                temp = pd.read_excel(file, sheet_name = None)
                data.append(temp)
                
                temp_keys = list()
                [temp_keys.append(key) for key in temp]
                data_keys.append(temp_keys)
                
            deck_names = file_names
                
        return data, data_keys, deck_names
    
    def analyze_deck_winrates(self, date, deck = None, class_name = None):
        '''Specify a date and a deck name or a class for which to analyze win rates and
                return these as a pandas data frame.
            Said table contains the deck name and win rates both weighted and unweighted against all classes.
            
        :args:
        - date (str): The day for which to analyze the win rates.
        - class_name (str): A class for which to analyze the win rates.
        - deck (str): The deck for which to analyze the win rates.
        
        :usage:
            self.analyze_deck_winrates('07-01', deck = 'Rogue - Miracle Rogue')
            ~
            self.analyze_deck_winrates('07-01', class_name = 'Rogue')            
            ~
            self.analyze_deck_winrates('07-01')
            
        :returns:
        - data_output (pd.DataFrame): A pandas data frame or a list of data frames,
            containing the deck name and win rates both weighted and unweighted against all classes.
            
        :note:
        - The deck name must be passed in a predefined format (e.g., Rogue - Miracle Rogue),
            apart from capitalization, which does need to be correct.
        '''
        data, data_keys, deck_names = self.load_data(date = date, deck = deck, class_name = class_name)

        if type(deck_names) == list:
            data_output = []
            deck_count = 0
            for d in data:
                overview = d.get('Overview')
                win_rates = overview.loc[:, 'Overall Winrate':'vs. Warlock'].apply(lambda x: self.percentage_to_float(x))
                sample_size = overview.loc[:, 'Sample Size']

                #Unweighted win rates
                WR_unweighted = win_rates.apply(np.mean, axis = 0)

                #Weighted win rates
                weights = sample_size/sum(sample_size)
                temp = win_rates.apply(lambda x: x*weights)
                WR_weighted = temp.apply(np.sum, axis = 0)
            
                deck_name = deck_names[deck_count]
                deck_count += 1
                temp = pd.DataFrame({'Deck Name': deck_name,
                                    'Unweighted Win Rate': WR_unweighted,
                                    'Weighted Win Rate' : WR_weighted})
                
                temp = temp.reset_index()
                temp = temp.set_index('Deck Name')
                temp = temp.rename(columns = {'index' : 'Versus'})                
                
                data_output.append(temp)
                
        else:
            overview = data.get('Overview')
            win_rates = overview.loc[:, 'Overall Winrate':'vs. Warlock'].apply(lambda x: self.percentage_to_float(x))
            sample_size = overview.loc[:, 'Sample Size']

            #Unweighted win rates
            WR_unweighted = win_rates.apply(np.mean, axis = 0)

            #Weighted win rates
            weights = sample_size/sum(sample_size)
            temp = win_rates.apply(lambda x: x*weights)
            WR_weighted = temp.apply(np.sum, axis = 0)
            
            temp = pd.DataFrame({'Deck Name': deck_names,
                                    'Unweighted Win Rate': WR_unweighted,
                                    'Weighted Win Rate' : WR_weighted})
            
            temp = temp.reset_index()
            temp = temp.set_index('Deck Name')
            data_output = temp.rename(columns = {'index' : 'Versus'})
        
        return data_output
    
    def prepare_winrates_df(self, date, deck = None, class_name = None):
        '''Specify a date and a deck name or a class for which to prepare the win rate data frames for and
                return these as two separate pandas data frames, unweighted and weighted by sample size.
            These contain information on win rates of all archetypes overall and against all classes.
            
        :args:
        - date (str): The day for which to prepare the win rate data frames for.
        - class_name (str): A class for which to prepare the win rate data frames for.    
        - deck (str): The deck for which to prepare the win rate data frames for.
        
        :usage:
            self.prepare_winrates_df('07-01', deck = 'Rogue - Miracle Rogue')
            ~
            self.prepare_winrates_df('07-01', class_name = 'Rogue')
            ~            
            self.prepare_winrates_df('07-01')
            
        :returns:
        - data_u (pd.DataFrame): A pandas data frame containing the unweighted win rates against all classes.
        - data_w (pd.DataFrame): A pandas data frame containing the weighted win rates against all classes.
            
        :note:
        - The deck name must be passed in a predefined format (e.g., Rogue - Miracle Rogue),
            apart from capitalization, which does need to be correct.
        '''
    
        temp = self.analyze_deck_winrates(date = date, deck = deck, class_name = class_name)
        
        #Unweighted data frame
        data_u = pd.DataFrame()
        for i in range(len(temp)):
            one_deck = temp[i]
            pivot_deck = pd.pivot_table(data = one_deck, values = 'Unweighted Win Rate',
                                        index = 'Deck Name', columns = 'Versus')
            data_u = pd.concat([data_u, pivot_deck], axis = 0)
                    
        #Weighted data frame
        data_w = pd.DataFrame()
        for i in range(len(temp)):
            one_deck = temp[i]
            pivot_deck = pd.pivot_table(data = one_deck, values = 'Weighted Win Rate',
                                        index = 'Deck Name', columns = 'Versus')
            data_w = pd.concat([data_w, pivot_deck], axis = 0)
            
        return data_u, data_w
                
    def win_rates_to_excel(self, date, weighted = True, deck = None, class_name = None):
        '''Specify a date and a deck name, along with variables win_rates and weighted and create an excel file for data
            satisfying said parameters.
            
        :args:
        - date (str): The day for which to create the excel file for.
        - win_rates (bool): If true, create an excel file containing information about deck win rates.
            If false, create an excel file containing data for further analysis and modelling.
        - weighted (True): If true, use weighted win rates when creating the win rates excel.
            If false, use unweighted win rates.
        - deck (str): The deck for which to create the excel file for.
        - class_name (str): Name of the class for which to create the excel file for.

        :usage:
            self.win_rates_to_excel(date = '07-01', win_rates = True, weighted = True, deck = 'Rogue - Miracle Rogue')
            ~
            self.win_rates_to_excel(date = '07-01', processed = True, class_name = 'Rogue')
            
        :returns:
        - None: Creates an excel file with specified parameters at the predefined path.
            
        :note:
        - The deck name must be passed in a predefined format (e.g., Rogue - Miracle Rogue),
            apart from capitalization, which does need to be correct.            
        '''
        data_u, data_w = self.prepare_winrates_df(date = date, deck = deck, class_name = class_name)
        if weighted == True:
            path = f'{analysis_path}/Unweighted win rates.xlsx'.replace('/', '\\') 
            data_u.to_excel(path)
        else:
            path = f'{analysis_path}/Weighted rates.xlsx'.replace('/', '\\') 
            data_w.to_excel(path)
            
        return None
    
    def prepare_model_df(self, date, processed = True, deck = None, class_name = None, WR_against = 'All'):
        '''Specify a date, a win rate type and a deck name or a class for which to prepare the model data frame
            for and return this as a pandas data frame.
            This contains all information about the specified deck or all decks which are avilable
                on the hsreplay.net website.
            
        :args:
        - date (str): The day for which to prepare the model data frame for.
        - class_name (str): A class for which to prepare the model data frame for.  
        - processed (bool): If true, process the data for modelling.        
        - deck (str): The deck for which to prepare the model data frame for.
        - WR_against (str): The type of win rate which to use as a dependent variable in the models.        
        
        :usage:
            self.prepare_model_df('07-01', deck = 'Rogue - Miracle Rogue')
            ~
            self.prepare_model_df('07-01', class_name = 'Rogue', WR_against = 'Druid')
            ~            
            self.prepare_model_df('07-01', processed = False)
            
        :returns:
        - df (pd.DataFrame): A pandas data frame containing the data from hsreplay.net to be used in further analysis and modelling.
            
        :note:
        - The deck name must be passed in a predefined format (e.g., Rogue - Miracle Rogue),
            apart from capitalization, which does need to be correct.
        - The 'WR_type' is a categorical variable, which takes on 11 categories - 'All' and names of the
            10 classes in the game. If set to all, use as a dependent variable the overall win rate of the 
            decks in the data set.
        '''
        
        data, data_keys, deck_names = self.load_data(date = date, deck = deck, class_name = class_name)
        
        #Loading the data
        temp1 = pd.DataFrame()
        temp2 = pd.DataFrame()
        
        for d in data:
            for i in d:
                card_info = d[i]
                if i == 'Overview':
                    temp1 = temp1.append(card_info)
                else:
                    temp2 = temp2.append(card_info)
        
        temp = temp1.merge(temp2)
        
        
        #Processing the data to be used in further modelling
        if processed == True:
            winrate_cols = ['Overall Winrate', 'vs. Demon Hunter', 'vs. Druid', 'vs. Hunter', 'vs. Mage',
                            'vs. Paladin', 'vs. Priest', 'vs. Rogue', 'vs. Shaman', 'vs. Warlock', 'vs. Warrior',
                            'Mulligan WR', 'Kept', 'Drawn WR', 'Played WR']
            
            temp[winrate_cols] = temp[winrate_cols].apply(lambda x: self.percentage_to_float(x))
            
            if WR_against == 'All':
                WR_type = 'Overall Winrate'
            else:
                WR_type = f'vs. {WR_against}'
                
            new_cols = ['Class', 'Deck Name', 'Deck Code', 'Date', 'Sample Size', WR_type]
            df = temp[new_cols]

            #Getting dummy variables for all the cards
            dummies = pd.get_dummies(temp['Card Name']).apply(lambda x: x*temp['Card Count'])
            df = pd.concat([df, dummies], axis = 1)

        
        
        return df

    
    def model_data_to_excel(self, date, processed = True, deck = None, class_name = None, WR_against = 'All'):
        '''Specify a date and a deck name, along with a variable 'processed' and create an excel file for data
            satisfying said parameters.
            
        :args:
        - date (str): The day for which to create the excel file for.
        - processed (bool): If true, process the data for modelling when creating the model data excel.
        - deck (str): The deck for which to create the excel file for.
        - class_name (str): Name of the class for which to create the excel file for.
        - WR_against (str): The type of win rate which to use as a dependent variable in the models.          

        :usage:
            self.model_data_to_excel(date = '07-01', processed = True, deck = 'Rogue - Miracle Rogue')
            ~
            self.model_data_to_excel(date = '07-01', processed = True, class_name = 'Rogue', WR_against = 'Hunter')
            
        :returns:
        - None: Creates an excel file with specified parameters at the predefined path.
            
        :note:
        - The deck name must be passed in a predefined format (e.g., Rogue - Miracle Rogue),
            apart from capitalization, which does need to be correct.            
        - The 'WR_type' is a categorical variable, which takes on 11 categories - 'All' and names of the
            10 classes in the game. If set to all, use as a dependent variable the overall win rate of the 
            decks in the data set.            
        '''
        data = self.prepare_model_df(date = date, processed = processed, deck = deck, class_name = class_name,
                                        WR_against = WR_against)

        if deck != None:
            path = f'{analysis_path}/Model data {deck} vs. {WR_against}.xlsx'.replace('/', '\\') 
            data.to_excel(path, index = False)          
        elif class_name != None:
            path = f'{analysis_path}/Model data {class_name} vs. {WR_against}.xlsx'.replace('/', '\\') 
            data.to_excel(path, index = False)        
        else:
            path = f'{analysis_path}/Model data All vs. {WR_against}.xlsx'.replace('/', '\\') 
            data.to_excel(path, index = False)              
    
        return None