#!{sys.executable} -m pip install --upgrade --no-cache-dir pysimplegui
#!{sys.executable} -m pip install --upgrade --no-cache-dirpip install PyInstaller
#Importing the data extractor scripts
import sys
sys.path.insert(0, 'C:\\Users\\AU451FE\\OneDrive - EY\\Desktop\\Python\\Hearthstone_Archmage\\Scripts')

#Other useful packages
import time
import datetime
import pandas as pd
import numpy as np
import re #String search
import os
import PySimpleGUI as sg

class GraphicalArchmage:
    '''Docstring here
    '''
    def __init__(self):
        pass

    def open_init_w(self):
        #Text
        col1 = sg.Column([[sg.Frame(layout = [[sg.Text('\nWelcome to the Hearthstone Archmage\n', size = (60,3),
                                        font = ('Courier, 35'), background_color = 'lightblue', justification = 'center')]],
                                   title = '', background_color = 'black')]], justification = 'center')
        col2 = sg.Column([[sg.Frame(layout = [[sg.Text('Specifiy the type of activity\n you wish to do', size = (60,2),
                                        font = ('Courier, 20'), justification = 'center')]],
                                   title = '', background_color = 'black')]], justification = 'center')        
        #Activities
        col3 = sg.Column([[sg.Frame('',
                        [[sg.Button('Get data', key = '-GET-DATA-', size = (25,5), font = 20, pad = (50,50)),
                            sg.Button('Build a deck', key = '-BUILD-DECK-', size = (25,5), font = 20, pad = (50,50))],
                        [sg.Button('Explore data', key = '-EXPLORE-DATA-', size = (25,5), font = 20, pad = (50,50)),
                            sg.Button('Pick/ban\n advisor', key = '-PICK-BAN-', size = (25,5), font = 20, pad = (50,50))]])]],
                                 background_color = 'black', justification = 'center')
        #Options and help
        tech_col = sg.Column([[sg.Text('\n\n')],
                [sg.Column([[sg.Button('Settings', key = '-SETTINGS-'),
                             sg.Button('Help', key = '-HELP1-'),
                             sg.Button('Quit')]],
                                        size=(155,45))]], justification = 'right') 

        layout = [[col1],
                  [col2],
                  [col3],
                  [tech_col]]
        
        sg.theme('LightGrey1')
        sg.set_options(font=("Arial", 10))
        
        return sg.Window('Hearthstone Archmage', layout, size = (1080, 820), finalize=True)
    
    def open_get_data_w(self):
        col1 = sg.Column([[sg.Frame(layout = [[sg.Text('Data Extraction', size = (60,1),
                                        font = ('Courier, 25'), background_color = 'lightyellow', justification = 'center')]],
                                    title = '', background_color = 'blue')]], justification = 'center')
        
        #Driver and folder selection
        col2 = sg.Column([[sg.Frame('',
                                   [[sg.Text('Select the driver:', size = (20,1)),
                                     sg.Button('Here', size = (4,1), key = '-DRIVER-PATH-'),
                                     sg.Text('-', size=(3,1), key='-DRIVER-PATH-OK-', justification = 'center')],
                                    [sg.Text('Select a folder to store data:', size = (20,1)),
                                     sg.Button('Here', size = (4,1), key = '-DECK-FOLDER-'),
                                     sg.Text('-', size=(3,1), key='-DECK-FOLDER-OK-', justification = 'center')]])]]
                          ,justification = 'left')
        
        col3 = sg.Column([[sg.Frame(layout=[
    [sg.Text('Extract data for:', size = (31,1), justification = 'center')],
    [sg.Text('', size = (11,1)), sg.Radio('All', 'class_sel_1', default=True, size=(10,1), key = '-EXTRACT-ALL-')],  
    [sg.Radio('Demon Hunter', 'class_sel_1', size=(12,1), key = '-EXTRACT-DEMON-HUNTER-'),
     sg.Radio('Druid', 'class_sel_1', size=(11,1), key = '-EXTRACT-DRUID-')],
    [sg.Radio('Hunter', 'class_sel_1', size=(12,1), key = '-EXTRACT-HUNTER-'),
     sg.Radio('Mage', 'class_sel_1', size=(11,1), key = '-EXTRACT-MAGE-')],
    [sg.Radio('Paladin', 'class_sel_1', size=(12,1), key = '-EXTRACT-PALADIN-'),
     sg.Radio('Priest', 'class_sel_1', size=(11,1), key = '-EXTRACT-PRIEST-')],
    [sg.Radio('Rogue', 'class_sel_1', size=(12,1), key = '-EXTRACT-ROGUE-'),
     sg.Radio('Shaman', 'class_sel_1', size=(11,1), key = '-EXTRACT-SHAMAN-')],
    [sg.Radio('Warlock', 'class_sel_1', size=(12,1), key = '-EXTRACT-WARLOCK-'),
     sg.Radio('Warrior', 'class_sel_1', size=(11,1), key = '-EXTRACT-WARRIOR-')]],
                                   title='',title_color='black')]], justification = 'left')
        
        
        col4 = sg.Column([[sg.Frame(layout = [
    [sg.Text('Specify an archetype:', size = (17,1)),
     sg.Radio('Yes', 'archetype_selection', enable_events = True, key = '-SELECT-ARCHETYPE-YES-'),
     sg.Radio('No', 'archetype_selection', default = True, enable_events = True, key = '-SELECT-ARCHETYPE-NO-')],       
     [sg.Column([[sg.Text('', size = (5,3))]]
                , visible=True, key='-SELECT-ARCHETYPE-0-'),
      sg.Column([[sg.Text('Name:', size = (5,1)),
                 sg.I(size=(20, 1), key = '-EXTRACT-ARCHETYPE-'), sg.Submit('OK', size = (3,1), key = '-SUBMIT-ARCHETYPE-')],
                 [sg.Text('', size = (29,1), key = '-ARCHETYPE-CONFIRMATION-')]]
                , visible = False, key = '-SELECT-ARCHETYPE-1-')]],
                                   title = '')]], justification = 'left')
        
        
        col2_4 = sg.Column([[col2],
                  [col3],
                  [col4]], justification = 'top')
        
        col5 = (sg.Column([[sg.Frame(layout = [
            [sg.Text('HSreplay Scraper')],
            [sg.Output(size = (102,21), background_color = 'White')],
            [sg.Column([[sg.Button('Run', size = (4,1), key = '-EXTRACT-DATA-RUN-'),
                         sg.Button('Stop', size = (4,1), key = '-EXTRACT-DATA-STOP-')]], justification = 'right')]],
                                    title = '')]],justification = 'left'))
        
        
        #Column template
        #col5 = (sg.Column([[sg.Frame(layout = [
        #    []], 
        #                            title = '')]],justification = 'left'))        
        
        
        tech_col = sg.Column([[sg.Text('')],
                [sg.Column([[sg.Button('Settings', key = '-SETTINGS-'),
                             sg.Button('Help', key = '-HELP2-'),
                             sg.Button('Back', key = '-BACK-')]],
                                        size=(165,45))]], justification = 'right')
        
        layout = [[col1],  #Block1 
                  [col2_4, col5],
                  [tech_col]] #Block3
        
        #sg.theme('DarkBlue5')
        
        return sg.Window('Data extraction', layout, size = (1080, 820), finalize=True)
    
    
    def open_build_deck_w(self):
        col1 = sg.Column([[sg.Frame(layout = [[sg.Text('Deck Building', size = (60,1),
                                        font = ('Courier, 25'), background_color = 'lightyellow', justification = 'center')]],
                                    title = '', background_color = 'yellow')]], justification = 'center') 
        
        tech_col = sg.Column([[sg.Text('\n\n')],
                [sg.Column([[sg.Button('Settings', key = '-SETTINGS-'),
                             sg.Button('Help', key = '-HELP3-'),
                             sg.Button('Back', key = '-BACK-')]],
                                        size=(165,45))]], justification = 'right')         
        layout = [[col1],
                 [tech_col]]
        
        return sg.Window('Deck building', layout, size = (1080, 820), finalize=True)
        
       
    def open_explore_data_w(self):
        col1 = sg.Column([[sg.Frame(layout = [[sg.Text('Data Exploration', size = (60,1),
                                        font = ('Courier, 25'), background_color = 'lightyellow', justification = 'center')]],
                                    title = '', background_color = 'lightgreen')]], justification = 'center') 
        
        #Folder selection
        col2 = sg.Column([[sg.Frame('',
                                   [[sg.Text('Select the folder with raw data:', size = (24,1)),
                                     sg.Button('Here', key = '-DECK-FOLDER-'),
                                     sg.Text('-', size=(3,1), key='-DECK-FOLDER-OK-', justification = 'center')],
                                     [sg.Text('Select a folder for output storage:', size = (24,1)),
                                     sg.Button('Here', key = '-ANALYSIS-PATH-'),
                                     sg.Text('-', size=(3,1), key='-ANALYSIS-PATH-OK-', justification = 'center')]])]]
                          ,justification = 'left')        

        tech_col = sg.Column([[sg.Text('\n\n')],
                [sg.Column([[sg.Button('Settings', key = '-SETTINGS-'),
                             sg.Button('Help', key = '-HELP4-'),
                             sg.Button('Back', key = '-BACK-')]],
                                        size=(165,45))]], justification = 'right')        
        layout = [[col1],
                  [col2],
                 [tech_col]]
        
        return sg.Window('Data exploration', layout, size = (1080, 820), finalize=True)
    
    
    def open_pick_ban_w(self):
        col1 = sg.Column([[sg.Frame(layout = [[sg.Text('Pick/ban advisor', size = (60,1),
                                        font = ('Courier, 25'), background_color = 'lightyellow', justification = 'center')]],
                                    title = '', background_color = 'red')]], justification = 'center') 
        
        tech_col = sg.Column([[sg.Text('\n\n')],
                [sg.Column([[sg.Button('Settings', key = '-SETTINGS-'),
                             sg.Button('Help', key = '-HELP5-'),
                             sg.Button('Back', key = '-BACK-')]],
                                        size=(165,45))]], justification = 'right')
        layout = [[col1],
                 [tech_col]]
        
        return sg.Window('Pick/ban advisor', layout, size = (1080, 820), finalize=True)
    
    def get_help_window(self, key):
        if key == '-HELP1-':
            sg.popup('This help should help you understand how to navigate the application', title = 'Help')
        elif key == '-HELP2-':
            sg.popup('This help should help you understand how to extract data into your computer', title = 'Help')        
        elif key == '-HELP3-':
            sg.popup('This help should help you understand how to build your deck using statistics', title = 'Help')    
        elif key == '-HELP4-':
            sg.popup('This help should help you understand how to explore data efficiently', title = 'Help')
        elif key == '-HELP5-':
            sg.popup('This help should help you understand how to use the pick/ban advisor ', title = 'Help')            
           
        return None
    
    def select_folder(self, key):
        if key == '-DECK-FOLDER-':
            deck_folder = sg.popup_get_folder('Select the deck folder', title = 'Select')

        elif key == '-ANALYSIS-PATH-':
            analysis_path = sg.popup_get_folder('Select the analysis path', title = 'Select')
            
        try:
            deck_folder
        except NameError:
            deck_folder = None
            
        try:
            analysis_path
        except NameError:
            analysis_path = None            
        
        return deck_folder, analysis_path
    
    def select_file(self, key):
        if key == '-DRIVER-PATH-':
            driver_path = sg.popup_get_file('Select the driver', title = 'Select')
            
        try:
            driver_path
        except NameError:
            driver_path = None
        
        return driver_path

    def run_extraction(self, driver_path, deck_folder, class_name, extract_arch = False, archetype_name = None, 
                       minimized = False):
        from DataExtractor import DataExtractor
        DE = DataExtractor(driver_path, deck_folder, minimized)
        if extract_arch == True:
            if archetype_name in [None, '']:
                print('Please specify the archetype name if you wish to extract archetype data.')
            elif class_name == 'All':
                print('Please select the correct class if you wish to extract archetype data.')
            elif ((class_name in archetype_name) or ('Other' in archetype_name)) == False:
                print('Check whether the selected class matches the archetype.')                
            else:
                DE.archetype_to_excel(class_name, archetype_name)
        elif extract_arch == False:
            if class_name != 'All':
                print(f'Extracting data for {class_name} and subsequent classes.')
                skip = class_codes_list.get(class_name)
                DE.get_all_data(classes_skip = skip)
            else:
                DE.get_all_data(classes_skip = 0)

        return None
        
        
    
    def analyze(self):  
        class_names_list = ['All', 'Demon Hunter', 'Druid', 'Hunter', 'Mage', 'Paladin',
                       'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']
        class_codes_list = {'Demon Hunter' : 1, 'Druid' : 2, 'Hunter' : 3, 'Mage' : 4, 'Paladin' : 5,
                       'Priest' : 6, 'Rogue' : 7 , 'Shaman' : 8, 'Warlock' : 9, 'Warrior' : 10}
        class_tags_list = ['-EXTRACT-ALL-', '-EXTRACT-DEMON-HUNTER-', '-EXTRACT-DRUID-', '-EXTRACT-HUNTER-',
                           '-EXTRACT-MAGE-', '-EXTRACT-PALADIN-', '-EXTRACT-PRIEST-', '-EXTRACT-ROGUE-',
                           '-EXTRACT-SHAMAN-', '-EXTRACT-WARLOCK-', '-EXTRACT-WARRIOR-']
        help_list = ['-HELP1-', '-HELP2-', '-HELP3-', '-HELP4-', '-HELP5-']
        archetype_tag = ['-SELECT-ARCHETYPE-NO-', '-SELECT-ARCHETYPE-YES-']

        init_w, get_data_w, build_deck_w, explore_data_w, pick_ban_w = self.open_init_w(), None, None, None, None
        
        while True:
            window, event, values = sg.read_all_windows()
            #print(event)
            #print(values)
            
            #Window closure
            if event == sg.WINDOW_CLOSED or event == '-BACK-' or event == 'Quit':
                if window == get_data_w:    #Close get_data_w and marked as closed
                    get_data_w.close()
                    get_data_w = None  
                elif window == build_deck_w:    #Close build_deck_w and marked as closed
                    build_deck_w.close()
                    build_deck_w = None
                elif window == explore_data_w:    #Close explore_data_w and marked as closed
                    explore_data_w.close()
                    explore_data_w = None
                elif window == pick_ban_w:    #Close pick_ban_w and marked as closed
                    pick_ban_w.close()
                    pick_ban_w = None                        
                elif window == init_w:
                    if get_data_w != None:    
                        get_data_w.close()
                    elif build_deck_w != None:
                        build_deck_w.close()
                    elif explore_data_w != None:
                        explore_data_w.close()
                    elif pick_ban_w != None:
                        pick_ban_w.close()
                    window.close()    #Close all other open windows and then the initial window itself
                    break

            #Folder and file selection        
            elif event == '-DECK-FOLDER-':
                deck_folder = self.select_folder(event)[0]
                if deck_folder == None:
                    window['-DECK-FOLDER-OK-'].update('x')
                else:
                    window['-DECK-FOLDER-OK-'].update('OK!')
                   
            elif event == '-ANALYSIS-PATH-':
                analysis_path = self.select_folder(event)[1]
                if analysis_path == None:
                    window['-ANALYSIS-PATH-OK-'].update('x')
                else:
                    window['-ANALYSIS-PATH-OK-'].update('OK!')
                
            elif event == '-DRIVER-PATH-':
                driver_path = self.select_file(event)
                if driver_path == None:
                    window['-DRIVER-PATH-OK-'].update('x')
                else:
                    window['-DRIVER-PATH-OK-'].update('OK!')                
            
            #Settings
            elif event == '-SETTINGS-':
                pass #define this in case of need
            
            #Defining functions shared across windows
            elif event in help_list:
                self.get_help_window(event)
                
                
            #Functions for Get Data window
            elif event in archetype_tag:
                for i in range(2):
                    window[f'-SELECT-ARCHETYPE-{i}-'].update(visible=values[archetype_tag[i]])
                window['-ARCHETYPE-CONFIRMATION-'].update('')
                    
            elif event == '-SUBMIT-ARCHETYPE-':
                if values['-EXTRACT-ARCHETYPE-'] in ['', None]:
                    window['-ARCHETYPE-CONFIRMATION-'].update('Please specify a valid deck.')
                else:    
                    archetype_name = values['-EXTRACT-ARCHETYPE-']
                    window['-EXTRACT-ARCHETYPE-'].update('')
                    window['-ARCHETYPE-CONFIRMATION-'].update(archetype_name + ' selected.')
                    
            elif event == '-EXTRACT-DATA-RUN-':  
                for c in class_tags_list:
                    if values[c] == True:
                        class_name = class_names_list[class_tags_list.index(c)]
                extract_arch = values['-SELECT-ARCHETYPE-YES-']
                minimized = False
                try:
                    archetype_name
                except:
                    archetype_name = None
                try:
                    driver_path, deck_folder
                except:
                    print('Please specify the path to a driver and a folder where the output should be stored.')
                else:
                    self.run_extraction(driver_path, deck_folder, class_name, extract_arch, archetype_name,
                                        minimized)
            
            elif event == '-EXTRACT-DATA-STOP-':
                pass

            
            #Extra window opening
            elif event == '-GET-DATA-'and get_data_w == None:
                get_data_w = self.open_get_data_w()
            elif event == '-BUILD-DECK-'and build_deck_w == None:
                build_deck_w = self.open_build_deck_w()
            elif event == '-EXPLORE-DATA-' and explore_data_w == None:
                explore_data_w = self.open_explore_data_w()
            elif event == '-PICK-BAN-'and pick_ban_w == None:
                pick_ban_w = self.open_pick_ban_w()
            
        return None
        
GA = GraphicalArchmage()        
GA.analyze()