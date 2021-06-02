import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


class DataAnalyzer:

    #calculations assume half-ppr, will later implement options of standard, half-ppr, full ppr
    def __init__(self, csvDataset):
        self.data = pd.read_csv(csvDataset) #import the csv file into pandas dataframe

        # drop unneccesary columns from the dataset
        self.data.drop(['Rk', '2PM', '2PP', 'FantPt', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 'Fmb', 'GS'],axis=1, inplace=True)

        # fix name formatting
        self.data['Player'] = self.data['Player'].apply(lambda x: x.split('*')[0]).apply(lambda x: x.split('\\')[0])

        # rename columns
        self.data.rename({
            'TD': 'PassingTD',
            'TD.1': 'RushingTD',
            'TD.2': 'ReceivingTD',
            'TD.3': 'TotalTD',
            'Yds': 'PassingYDs',
            'Yds.1': 'RushingYDs',
            'Yds.2': 'ReceivingYDs',
            'Att': 'PassingAtt',
            'Att.1': 'RushingAtt'
        }, axis=1, inplace=True)

        # separate dataframes based off position
        self.data_rb = self.data[self.data['FantPos'] == 'RB']
        self.data_qb = self.data[self.data['FantPos'] == 'QB']
        self.data_wr = self.data[self.data['FantPos'] == 'WR']
        self.data_te = self.data[self.data['FantPos'] == 'TE']

        #calculate fantasy points for each position
        self.data_rb['FantasyPoints'] = self.data_rb['RushingYDs'] * 0.1 + self.data_rb['RushingTD'] * 6 + self.data_rb['Rec'] * 0.5 + self.data_rb['ReceivingYDs'] * 0.1 + self.data_rb['ReceivingTD'] * 6 - self.data_rb['FL'] * 2
        self.data_qb['FantasyPoints'] = self.data_qb['PassingTD'] * 4 + self.data_qb['RushingYDs'] * 0.1 + self.data_qb['RushingTD'] * 6 + self.data_qb['Rec'] * 0.5 + self.data_qb['ReceivingYDs'] * 0.1 + self.data_qb['ReceivingTD'] * 6 - self.data_qb['FL'] * 2 - self.data_qb['Int'] * 2
        self.data_wr['FantasyPoints'] = self.data_wr['RushingYDs'] * 0.1 + self.data_wr['RushingTD'] * 6 + self.data_wr['Rec'] * 0.5 + self.data_wr['ReceivingYDs'] * 0.1 + self.data_wr['ReceivingTD'] * 6 - self.data_wr['FL'] * 2
        self.data_te['FantasyPoints'] = self.data_te['RushingYDs'] * 0.1 + self.data_te['RushingTD'] * 6 + self.data_te['Rec'] * 0.5 + self.data_te['ReceivingYDs'] * 0.1 + self.data_te['ReceivingTD'] * 6 - self.data_te['FL'] * 2
        #add extra columns of data for each position
        self.initializeColumns(self.data_rb)
        self.initializeColumns(self.data_qb)
        self.initializeColumns(self.data_wr)
        self.initializeColumns(self.data_te)

        # Add a catchrate column to positions of players that can catch balls
        self.data_wr['CatchRate'] = self.data_wr['Rec'] / self.data_wr['Tgt']
        self.data_te['CatchRate'] = self.data_te['Rec'] / self.data_te['Tgt']
        self.data_rb['CatchRate'] = self.data_rb['Rec'] / self.data_rb['Tgt']


    #Method that adds extra columns to its dataset that can be used for later calculations
    def initializeColumns(self, positionDataset):
        #fantasy points per game (an average)
        positionDataset['FantasyPoints/GM'] = positionDataset['FantasyPoints'] / positionDataset['G']
        positionDataset['FantasyPoints/GM'] = positionDataset['FantasyPoints/GM'].apply(lambda x: round(x, 2))




    #Method that plots the usage per game by the fantasy points per game of the given position
    def plotUsagePerGame(self, position):
        x, y = (0, 0) #initalize x and y variables for plotting
        if position == 'RB':
            # Create new column for usage per game. Usage is define as # of targets + carries
            self.data_rb['Usage/GM'] = (self.data_rb['RushingAtt'] + self.data_rb['Tgt']) / self.data_rb['G']
            # round each row value to two decimal places
            self.data_rb['Usage/GM'] = self.data_rb['Usage/GM'].apply(lambda x: round(x, 2))

            x = self.data_rb['Usage/GM']
            y = self.data_rb['FantasyPoints/GM']

        elif position == 'QB':
            pass
        elif position == 'WR':
            # Create new column for usage per game. Usage is defined as the # of targets
            self.data_wr['Usage/GM'] = (self.data_wr['Tgt']) / self.data_wr['G']
            # round each row value to two decimal places
            self.data_wr['Usage/GM'] = self.data_wr['Usage/GM'].apply(lambda x: round(x, 2))

            x = self.data_wr['Usage/GM']
            y = self.data_wr['FantasyPoints/GM']
        elif position == 'TE':
            # Create new column for usage per game. Usage is define as # of targets
            self.data_te['Usage/GM'] = (self.data_te['Tgt']) / self.data_te['G']
            # round each row value to two decimal places
            self.data_te['Usage/GM'] = self.data_te['Usage/GM'].apply(lambda x: round(x, 2))

            x = self.data_te['Usage/GM']
            y = self.data_te['FantasyPoints/GM']
        else:
            print('Incorrect position entered')
            return #because we dont want to plot an empty graph
        sns.set_style('whitegrid')
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 10)
        plot = sns.regplot(x, y, scatter=True)
        plt.show()

    #method that plots the efficiency (TD/Usage) by Fantasy Points per game
    def plotEfficiency(self, position, cutoff=20):
        x, y = (0, 0)
        if position == 'RB':
            self.data_rb['TD/Usage'] = (self.data_rb['RushingTD'] + self.data_rb['ReceivingTD']) / (self.data_rb['RushingAtt'] + self.data_rb['Tgt'])
            sampleSize = self.data_rb[self.data_rb['RushingAtt'] > cutoff] #adjust the size of the data based on the user's input

            x = sampleSize['TD/Usage']
            y = sampleSize['FantasyPoints/GM']
        elif position == 'QB':
            pass
        elif position == 'WR':
            self.data_wr['TD/Usage'] = (self.data_wr['RushingTD'] + self.data_wr['ReceivingTD']) / (self.data_wr['RushingAtt'] + self.data_wr['Tgt'])
            sampleSize = self.data_wr[self.data_wr['Tgt'] > cutoff]  # adjust the size of the data based on the user's input

            x = sampleSize['TD/Usage']
            y = sampleSize['FantasyPoints/GM']
        elif position == 'TE':
            self.data_te['TD/Usage'] = (self.data_te['RushingTD'] + self.data_te['ReceivingTD']) / (
                        self.data_te['RushingAtt'] + self.data_te['Tgt'])
            sampleSize = self.data_te[self.data_te['Tgt'] > cutoff]  # adjust the size of the data based on the user's input

            x = sampleSize['TD/Usage']
            y = sampleSize['FantasyPoints/GM']
        else:
            print('Incorrect position entered')
            return
        sns.set_style('whitegrid')
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 10)
        plot = sns.regplot(x, y, scatter=True)
        plt.show()

    # method that plots Y/A by fantasy football points per game. defaults to runningback if position parameter is not filled
    def plotRushYardsPerAttempt(self, position='RB', minAttempts=5):
        x, y = (0, 0)
        if position == 'RB':
            sampleSize = self.data_rb[self.data_rb['RushingAtt'] > minAttempts] #narrows the size by cutting those who ran the ball less than 'minAttempts' times throughout the season
            x = sampleSize['Y/A']
            y = sampleSize['FantasyPoints/GM']
        elif position == 'QB':
            pass
        elif position == 'WR':
            sampleSize = self.data_wr[self.data_wr['RushingAtt'] > minAttempts]  # narrows the size by cutting those who ran the ball less than 'minAttempts' times throughout the season
            x = sampleSize['Y/A']
            y = sampleSize['FantasyPoints/GM']
        elif position == 'TE':
            sampleSize = self.data_te[self.data_te['RushingAtt'] > minAttempts]  # narrows the size by cutting those who ran the ball less than 'minAttempts' times throughout the season
            x = sampleSize['Y/A']
            y = sampleSize['FantasyPoints/GM']
        else:
            print("Incorrect position entered")
            return
        sns.set_style('whitegrid')
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 10)
        plot = sns.regplot(x, y, scatter=True)
        plt.show()

    # method that plots rushes per game by fantasy football points
    def plotRushAttemptsPerGame(self, position='RB'):
        self.data_rb['RushAttempts/GM'] = self.data_rb['RushingAtt'] / self.data_rb['G']
        x = self.data_rb['RushAttempts/GM']
        y = self.data_rb['FantasyPoints/GM']

        sns.set_style('whitegrid')
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 10)
        plot = sns.regplot(x, y, scatter=True)
        plt.show()

    # generalized plotting method
    def plot(self, position, statOne, statTwo):
        pass