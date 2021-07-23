#!{sys.executable} -m pip install --upgrade --no-cache-dir pysimplegui
#!{sys.executable} -m pip install --upgrade --no-cache-dirpip install PyInstaller
import sys
import datetime
import pandas as pd
import numpy as np
import re
import os
import PySimpleGUI as sg

class GraphicalArchmage:
    '''Create a GUI for data extraction and exploration.
    '''
    def __init__(self, driver_path = None, deck_folder = None, analysis_path = None):
        '''The constructor for the GraphicalArchmage class.
        '''
        #Defining file paths
        self.base_path = re.search(f'(.+)Hearthstone_Archmage', os.getcwd()).group(1)\
            + 'Hearthstone_Archmage'
        script_path = self.base_path + '\Scripts'
        if script_path not in sys.path:
            sys.path.insert(0, script_path)

        if driver_path == None:
            self.driver_path = f'{self.base_path}\chromedriver'
        else:
            driver_path = driver_path
        if deck_folder == None:
            self.deck_folder = f'{self.base_path}\Data Frames'
        else:
            self.deck_folder = deck_folder
        if analysis_path == None:
            self.analysis_path = f'{self.base_path}\Data Frames\Analyzed' 
        else:
            self.analysis_path = analysis_path

        #Various tools
        self.today = datetime.date.today().strftime('%m-%d')

        #General tags
        self.class_names_list = ['All', 'Demon Hunter', 'Druid', 'Hunter', 'Mage', 'Paladin',
                       'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']
        self.class_codes_list = {'Demon Hunter' : 1, 'Druid' : 2, 'Hunter' : 3, 'Mage' : 4, 'Paladin' : 5,
                       'Priest' : 6, 'Rogue' : 7 , 'Shaman' : 8, 'Warlock' : 9, 'Warrior' : 10}

        #Tags across windows
        self.help_list = ['-HELP1-', '-HELP2-', '-HELP3-', '-HELP4-', '-HELP5-']
        self.window_tags_list = ['GD', 'DE']
        self.submit_archetype_list = ['-GD-SUBMIT-ARCHETYPE-', '-DE-SUBMIT-ARCHETYPE-']
        
        #GD tags
        self.archetype_tag = ['-GD-SELECT-ARCHETYPE-NO-', '-GD-SELECT-ARCHETYPE-YES-']
        
        #DE tags
        self.de_select_tag = ['-CLASS-WR-', '-ARCH-WR-', '-CLASS-CP-', '-ARCH-CP-']
        self.de_select_win = ['-DE-SELECT-CLASS-', '-DE-SELECT-ARCHETYPE-']

    def generate_var_tag_list(self, key_tag):
        '''Define a key tag and return a list containing f strings for said tag and
            all classes.   

        Args:
            key_tag (str): The tag which shall be used in the f string.

        Returns:
            var_tag_list (list): A list containing f strings for said tag and 
                all classes.
        '''
        var_tag_list = [f'-{key_tag}-ALL-', f'-{key_tag}-DEMON-HUNTER-', f'-{key_tag}-DRUID-', f'-{key_tag}-HUNTER-',
                           f'-{key_tag}-MAGE-', f'-{key_tag}-PALADIN-', f'-{key_tag}-PRIEST-', f'-{key_tag}-ROGUE-',
                           f'-{key_tag}-SHAMAN-', f'-{key_tag}-WARLOCK-', f'-{key_tag}-WARRIOR-']

        return var_tag_list

    def generate_class_elements(self, el_type, key_tag, size, enable_events = False, group_tag = None,
                                start = 1, end = 10):
        '''Input the type of element you want to generate, its key tag, size and several other specifications
                and return a list of these elements.

        Args:
            el_type (str): The type of element that should be generated. Can be either 'Checkbox' or 'Radio'.
            key_tag (str): The key tag that should be used for the class.
            size (str): Size of the output, should be a tuple in a bracket.
            enable_events (bool, optional): If true, the output element will have enabled elements. Defaults to False.
            group_tag (str, optional): The group tag that should be used. Defaults to None.
            start (int, optional): The index of a class from which to generate the elements. Defaults to 1.
            end (int, optional): The index of a class until which to generate the elements. Defaults to 10.

        Usage:
            self.generate_class_elements(el_type = 'Radio', key_tag = 'DE', enable_events = True,
                group_tag = 'radio1', start = 3, end = 10)

        Returns:
            output (list): A list of the elements defined by set parameters.
        '''
        
        end = end + 1
        var_tag_list = self.generate_var_tag_list(key_tag)

        if el_type.title() == 'Radio':
            output = [sg.Radio(self.class_names_list[i], group_tag, enable_events = enable_events, size = size,
                               default = (i==0), key = var_tag_list[i]) for i in range(start, end)]
        elif el_type.title() == 'Checkbox':
            output = [sg.Checkbox(self.class_names_list[i], enable_events = enable_events, size = size,
                                  key = var_tag_list[i]) for i in range(start, end)]

        return output
    
        #self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE', group_tag = 'de_sel_1', size = (10,1),
        #                                 enable_events = False, start = 1, end = 10)

    def open_init_w(self):
        '''Open the initial window of the GUI.

        Returns:
            sg.Window: An sg window for display of the initial menu.
        '''
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
        '''Open the Get Data window of the GUI.

        Returns:
            sg.Window: An sg window containing the elements for the Get Data page.
        '''
        col1 = sg.Column([[sg.Frame(layout = [[sg.Text('Data Extraction', size = (60,1),
                                        font = ('Courier, 25'), background_color = 'lightyellow', justification = 'center')]],
                                    title = '', background_color = 'blue')]], justification = 'center')
        
        #Driver and folder selection
        col2 = sg.Column([[sg.Frame('',
                                   [[sg.Text('Select the driver:', size = (20,1)),
                                     sg.Text('✔', size=(3,1), key='-DRIVER-PATH-OK-', justification = 'center'),
                                     sg.Button('Here', size = (4,1), key = '-DRIVER-PATH-')],
                                    [sg.Text('Select a folder to store data:', size = (20,1)),
                                     sg.Text('✔', size=(3,1), key='-DECK-FOLDER-OK-', justification = 'center'),
                                     sg.Button('Here', size = (4,1), key = '-DECK-FOLDER-')]])]]
                          ,justification = 'left')
        
        col3 = sg.Column([[sg.Frame(layout=[
        [sg.Text('Extract data for:', size = (31,1), justification = 'center')],
        [sg.Text('', size = (11,1)), sg.Radio('All', 'class_sel_1',
                    default=True, size=(10,1), key = '-EXTRACT-ALL-')],  
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
        sg.Radio('Yes', 'archetype_selection', enable_events = True, key = '-GD-SELECT-ARCHETYPE-YES-'),
        sg.Radio('No', 'archetype_selection', default = True, enable_events = True, key = '-GD-SELECT-ARCHETYPE-NO-')],       
        [sg.Column([[sg.Text('', size = (5,3))]]
                    , visible=True, key='-SELECT-ARCHETYPE-0-'),
        sg.Column([[sg.Text('Name:', size = (5,1)),
                    sg.I(size=(20, 1), key = '-GD-ARCHETYPE-NAME-'),
                    sg.Submit('OK', size = (3,1), key = '-GD-SUBMIT-ARCHETYPE-')],
                    [sg.Text('', size = (29,1), key = '-GD-ARCHETYPE-CONFIRMATION-')]]
                    , visible = False, key = '-SELECT-ARCHETYPE-1-')]],
                                    title = '')]], justification = 'left')
        
        
        col2_4 = sg.Column([[col2],
                  [col3],
                  [col4]], justification = 'left')
        
        col5 = (sg.Column([[sg.Frame(layout = [
            [sg.Text('HSreplay Scraper')],
            [sg.Output(size = (102,21), background_color = 'White')],
            [sg.Column([[sg.Button('Run', size = (4,1), key = '-EXTRACT-DATA-RUN-'),
                         sg.Button('Stop', size = (4,1), key = '-EXTRACT-DATA-STOP-')]], justification = 'right')]],
                                    title = '')]],justification = 'left'))
        
        
        #Column template
        #col5 = sg.Column([[sg.Frame(layout = [
        #    []], 
        #                            title = '')]],justification = 'left')        
        
        
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
             sg.Text('✔', size=(3,1), key='-DECK-FOLDER-OK-', justification = 'center'),
             sg.Button('Here', size = (4,1), key = '-DECK-FOLDER-')],
             [sg.Text('Select a folder for output storage:', size = (24,1)),
             sg.Text('✔', size=(3,1), key='-ANALYSIS-PATH-OK-', justification = 'center'),
              sg.Button('Here', size = (4,1), key = '-ANALYSIS-PATH-')]])]]
                          ,justification = 'left')        

        col3 = sg.Column([[sg.Frame(layout = [
            [sg.Text('Select what you wish to explore:', size = (35,1), justification = 'center')],
            [sg.Radio('Class win rate', 'data_expl_1', enable_events = True, 
                      default = True, size=(32,1), key = '-CLASS-WR-')],
            [sg.Radio('Archetype win rate', 'data_expl_1', enable_events = True, 
                      size=(32,1), key = '-ARCH-WR-')],
            [sg.Radio('Class card performance', 'data_expl_1', enable_events = True, 
                      size=(32,1), key = '-CLASS-CP-')],
            [sg.Radio('Archetype card performance', 'data_expl_1', enable_events = True, 
                      size=(32,1), key = '-ARCH-CP-')]], 
                                    title = '')]],justification = 'left')  
        
        #Class_archetype selection 
        col4 = sg.Column([[sg.Frame(layout = [
            [sg.Column([[sg.Text('Use data for:', size = (34,1), justification = 'center')],
             [sg.Text('', size = (12,1)), sg.Checkbox('All', size=(12,1), key = '-DE-ALL-')],
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE', size = (12,1), start = 1, end = 2),
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE', size = (12,1), start = 3, end = 4),        
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE', size = (12,1), start = 5, end = 6),
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE', size = (12,1), start = 7, end = 8),                             
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE', size = (12,1), start = 9, end = 10)]
                ,visible=True, key='-DE-SELECT-CLASS-'),
             #Archetype column
            sg.Column([[sg.Text('Use data for:', size = (34,1), justification = 'center')],
                        [sg.Text('Archetype:', size = (8,1)),
                        sg.I(size=(21, 1), key = '-DE-ARCHETYPE-NAME-'),
                        sg.Submit('OK', size = (3,1), key = '-DE-SUBMIT-ARCHETYPE-')],
                        [sg.Text('', size = (34,1), key = '-DE-ARCHETYPE-CONFIRMATION-')],
                        [sg.Text('', size = (34, 7))]]
                            ,visible = False, key = '-DE-SELECT-ARCHETYPE-')],
            [sg.Column([[sg.Text('Analyze win rate against:', size = (34,1), justification = 'center')],
             [sg.Text('', size = (12,1)), sg.Checkbox('All', size=(12,1), key = '-DE-VS-ALL-')],
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE-VS', size = (12,1), start = 1, end = 2),
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE-VS', size = (12,1), start = 3, end = 4),        
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE-VS', size = (12,1), start = 5, end = 6),
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE-VS', size = (12,1), start = 7, end = 8),                             
             self.generate_class_elements(el_type = 'Checkbox', key_tag = 'DE-VS', size = (12,1), start = 9, end = 10)])]
                    ], title = '')
                            ]], justification = 'left')
        
        #Date selection
        col5 = sg.Column([[sg.Frame(layout = [
            [sg.Text('Select the analysis date:', size = (18,1)),
             sg.Text(f'{self.today}', size = (6,1),
                    key = '-CAL-DATE-TEXT-', justification = 'center'),
             sg.Button('Select', size = (7,1), key = '-CAL-DATE-')]], 
                                    title = '')]],justification = 'left')
        
        #Output and the technical column
        col6 = sg.Column([[sg.Frame(layout = [
            [sg.Text('Data Exploration')],
            [sg.Output(size = (100,21), background_color = 'White')],
            [sg.Column([[sg.Button('Explore', size = (6,1), key = '-EXPLORE-PERF-RUN-')]], justification = 'right')]],
                                    title = '')]],justification = 'left')
        
        col7 = sg.Column([[sg.Text('', size = (100, 15))]], justification = 'left')
             
            
        tech_col = sg.Column(
            [[sg.Text('',size = (65,1)),
             sg.Button('Settings', key = '-SETTINGS-'),
             sg.Button('Help', key = '-HELP4-'),
             sg.Button('Back', key = '-BACK-')]], justification = 'left')
        

        col2_5 = sg.Column([[col2],
          [col3],
          [col4],
          [col5]], justification = 'left')  
            
        col6_t = sg.Column([[col6],
                  [col7],
                  [tech_col]], justification = 'left') 
        

        layout = [[col1],
                  [col2_5, col6_t]]
        
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
        '''Specify a key and open a help window for the respective sg window.

        Args:
            key (str): A key to specify the help window.

        Usage:
            self.get_help_window(key = '-HELP1-')

        Returns:
            None: Opens a help window.
        '''
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
        '''Specify a key and open a popup that returns and saves the path to the
        desired folder.

        Args:
            key (str): A key specifying which type of folder should be selected.

        Usage:
            self.select_folder(key = '-DECK-FOLDER-')

        Returns:
            deck_folder, analysis_path (str): Paths to the respective folders.
            Defaults to None.
        '''
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
        '''Specify a key and open a popup that returns and saves the path to the
        desired file.

        Args:
            key (str): A key specifying which file should be selected.

        Usage:
            self.select_file(key = '-DRIVER-PATH-')

        Returns:
            driver_path (str): Paths to the desired file. Defaults to None.
        '''        
        if key == '-DRIVER-PATH-':
            driver_path = sg.popup_get_file('Select the driver', title = 'Select')
            
        try:
            driver_path
        except NameError:
            driver_path = None
        
        return driver_path

    #Methods for the Get Data window
    def run_extraction(self, driver_path, deck_folder, class_name = None, extract_arch = False,
                        archetype_name = None, minimized = False):
        '''Specify the driver path, the folder for storing data and optionally a class name,
        whether an archetype should be extracted, what its name should be and whether
        this extraction should run minimized and extract data for these parameters.

        Args:
            driver_path (str): A path to the driver.
            deck_folder (str): A path to the deck where the data should be stored.
            class_name (str): A name of the class for which to extract the data.
            Defaults to None.
            extract_arch (bool, optional): If True, a specific archetype will be
                used in the data extraction. Defaults to False.
            archetype_name (str, optional): Name of the archetype for which
                to extract the data. Defaults to None.
            minimized (bool, optional): If true, the extraction will run minimized.
                Defaults to False. Setting to True is deprecated.

        Usage:
            self.run_extraction(driver_path, deck_folder, class_name = 'Rogue',
                extract_arch = False, archetype_name = None, minimized = False)

        Returns:
            None: Extracts the data from hsreplay.net.
        '''
        from DataExtractor import DataExtractor
        DE = DataExtractor(driver_path, deck_folder, minimized)
        if extract_arch == True:
            if archetype_name in [None, '']:
                return 'Please specify the archetype name if you wish to extract archetype data.'
            elif class_name == 'All':
                return 'Please select the correct class if you wish to extract archetype data.'
            elif ((class_name in archetype_name) or ('Other' in archetype_name)) == False:
                return 'Check whether the selected class matches the archetype.'
            else:
                return DE.archetype_to_excel(class_name, archetype_name)
        elif extract_arch == False:
            if class_name not in  ['All', None]:
                print(f'Extracting data for {class_name} and subsequent classes.')
                skip = self.class_codes_list.get(class_name)
                return DE.get_all_data(classes_skip = skip)
            else:
                return DE.get_all_data(classes_skip = 0)
        
        
    #Methods for the Data Exploration window    
    def explore_performance(self, explore, deck_folder, analysis_path, analysis_date,
        extract_arch_de, class_for = None, class_against = None, archetype_name = None):
        '''Select the type of exploration,
        folder with data, the path where the analysis output should
        be stored, the analysis date, whether or not to extract archetype and
        optionally the class for which and against which to analyze the data
        along with the archetype name and return the analyzed data.

        Args:
            explore (str): Which type of exploration to perform. (WR or CP) 
            deck_folder (str): The path to the folder where data folders are stored.
            analysis_path (str): The path to the folder where the analysis output
                should be stored.
            analysis_date (str): Date for which to conduct the analysis.
            extract_arch_de (bool): If True, perform the analysis for an archetype.
            class_for (str, optional): The class or a list of classes for which to
            perform the analysis. Defaults to None.
            class_against (str, optional): The class or a list of classes for which
                to perform the analysis against. Defaults to None.
            archetype_name (str, optional): Name of the archetype for which to
                perform the analysis. Defaults to None.

        Usage:
            self.explore_wr(epxlore = 'WR'deck_folder, analysis_path, '07-09',
            extract_arch_de = False, class_for = ['Mage', 'Hunter'],
            class_against = ['Rogue', 'Warrior'])

        Returns:
            temp (pd.DataFrame): The analyzed data.

        Note:
            Setting the extract_arch_de to True will override the optional arguments
                apart from archetype_name, which then needs to be specified.
            If class_for/class_against contain 'All' or are set to None, all classes
                are then considered for analysis. In the class_against case this
                leads to the inclusion of 'Overall Winrate' in the output.
        '''
        if not explore in ['WR', 'CP']:
            return 'Please select the correct type of exploration - Win Rate (WR) \
            or Card Performance (CP).'
        from DataProcessor import DataProcessor
        DP = DataProcessor(deck_folder, analysis_path)
        folder_date = f'{deck_folder}\{analysis_date}'
        if not os.path.exists(folder_date):
            return f'There is no data avilable for date {analysis_date}.'
        elif explore == 'WR':
            if extract_arch_de == True:
                if archetype_name in [None, '']:
                    return 'Please specify the archetype name if you wish to extract archetype data.'
                else:
                    temp = DP.prepare_winrates_df(date = analysis_date, deck = archetype_name,
                        WR_against = class_against)
                    return temp[0]
            elif extract_arch_de == False:
                archetype_name = None
                temp = DP.prepare_winrates_df(date = analysis_date, deck = archetype_name,
                    class_name = class_for, WR_against = class_against)
                return temp[0]
        elif explore == 'CP':
            if extract_arch_de == True:
                if archetype_name in [None, '']:
                    return 'Please specify the archetype name if you wish to extract archetype data.'
                else:
                    temp = DP.prepare_card_df(date = analysis_date, deck = archetype_name,
                        WR_against = class_against)
                    return temp
            elif extract_arch_de == False:
                archetype_name = None
                temp = DP.prepare_card_df(date = analysis_date, deck = archetype_name,
                        class_name = class_for, WR_against = class_against)
                return temp                 
    
    #The main method
    def analyze(self):  
        '''The main method for generating the GUI. Return None.

        Returns:
            None: Creates the GUI for as long as the code is running.
        '''
        init_w, get_data_w, build_deck_w, explore_data_w, pick_ban_w = self.open_init_w(), None, None, None, None

        while True:
            window, event, values = sg.read_all_windows()
            print(event)
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
                if driver_path == None or 'driver.exe' not in driver_path:
                    window['-DRIVER-PATH-OK-'].update('x')
                else:
                    window['-DRIVER-PATH-OK-'].update('OK!')                
            
            #Settings
            elif event == '-SETTINGS-':
                pass #define this in case of need
            
            #Defining functions shared across windows
            elif event in self.help_list:
                self.get_help_window(event)
                
            elif event in self.submit_archetype_list:
                w_tag = self.window_tags_list[self.submit_archetype_list.index(event)]
                if values[f'-{w_tag}-ARCHETYPE-NAME-'] in ['', None]:
                    window[f'-{w_tag}-ARCHETYPE-CONFIRMATION-'].update('Please specify a valid deck.')
                else:    
                    archetype_name = values[f'-{w_tag}-ARCHETYPE-NAME-'].title()
                    window[f'-{w_tag}-ARCHETYPE-NAME-'].update('')
                    window[f'-{w_tag}-ARCHETYPE-CONFIRMATION-'].update(archetype_name + ' selected.')
                    
            #Functions for Get Data window
            elif event in self.archetype_tag:
                for i in range(2):
                    window[f'-SELECT-ARCHETYPE-{i}-'].update(visible=values[self.archetype_tag[i]])
                window['-GD-ARCHETYPE-CONFIRMATION-'].update('')

            elif event == '-EXTRACT-DATA-RUN-':  
                extract_tags_list = self.generate_var_tag_list('EXTRACT')
                for c in extract_tags_list:
                    if values[c] == True:
                        class_name = self.class_names_list[extract_tags_list.index(c)]
                extract_arch = values['-GD-SELECT-ARCHETYPE-YES-']
                minimized = False
                try:
                    archetype_name
                except:
                    archetype_name = None
                try:
                    driver_path
                except:
                    driver_path = self.driver_path  
                try:
                    deck_folder
                except:
                    deck_folder = self.deck_folder
                finally:
                    self.run_extraction(driver_path, deck_folder, class_name, extract_arch, archetype_name,
                                        minimized)
            
            elif event == '-EXTRACT-DATA-STOP-':
                pass

            #Functions for Data Exploration window
            
            elif event in self.de_select_tag:
                de_bool = True in [values['-CLASS-WR-'], values['-CLASS-CP-']]
                window[self.de_select_win[0]].update(visible = de_bool)
                window[self.de_select_win[1]].update(visible = not de_bool)
                
            elif event == '-CAL-DATE-':
                analysis_date = sg.popup_get_date(no_titlebar=False, begin_at_sunday_plus=1)
                try:
                    analysis_date = datetime.datetime.strptime(str(analysis_date), '(%m, %d, %Y)').strftime('%m-%d')
                except ValueError:
                    window['-CAL-DATE-TEXT-'].update('-')
                else:
                    window['-CAL-DATE-TEXT-'].update(analysis_date)
                
            elif event == '-EXPLORE-PERF-RUN-':
                extract_arch_de = True in [values['-ARCH-WR-'], values['-ARCH-CP-']]
                try:
                    archetype_name
                except:
                    archetype_name = None
                    extract_arch_de = False #Avoiding a bug                
                try:
                    deck_folder
                except:
                    deck_folder = self.deck_folder
                try:
                    analysis_path
                except:
                    analysis_path = self.analysis_path
                try:
                    analysis_date
                except:
                    analysis_date = datetime.date.today().strftime('%m-%d')
                finally:
                    class_for = []                 
                    if extract_arch_de == True:
                        class_for = archetype_name                   
                    else:
                        for_key_list = self.generate_var_tag_list('DE')
                        class_for += [self.class_names_list[i] for i, n
                            in enumerate(for_key_list) if values[n] == True]

                    class_against = []                               
                    against_key_list = self.generate_var_tag_list('DE-VS')
                    class_against += [self.class_names_list[i] for i, n
                        in enumerate(against_key_list) if values[n] == True]

                    if (class_for in [[], 'All']) or ('All' in class_for):
                        class_for = None
                    if (class_against in [[], 'All']) or ('All' in class_against):
                        class_against = None

                    if values['-CLASS-WR-'] == True or values['-ARCH-WR-'] == True:   
                        explore = 'WR'
                    elif values['-CLASS-CP-'] == True or values['-ARCH-CP-'] == True:
                        explore = 'CP'

                    temp_data = self.explore_performance(explore, deck_folder,
                    analysis_path, analysis_date, extract_arch_de, class_for,
                    class_against, archetype_name)
                    print(temp_data)
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
        
#GA = GraphicalArchmage()        
#GA.analyze()        