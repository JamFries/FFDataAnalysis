import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

import pandas
import plotly.express as px

import layouts
import DataAnalyzer as d

# Helper function that takes a csv dataset from pro-football-reference and cleans it up as usable data
def cleanDataset(csvFile):
    retVal = pd.read_csv(csvFile)

    # Remove any unnecessary columns
    retVal.drop(['Rk', '2PM', '2PP', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 'Fmb', 'GS'],axis=1, inplace=True)

    # Fix the player name column data
    retVal['Player'] = retVal['Player'].apply(lambda x: x.split('*')[0]).apply(lambda x: x.split('\\')[0])

    # Rename Columns for more useful analysis
    retVal.rename({
        'TD': 'PassingTD',
        'TD.1': 'RushingTD',
        'TD.2': 'ReceivingTD',
        'TD.3': 'TotalTD',
        'Yds': 'PassingYDs',
        'Yds.1': 'RushingYDs',
        'Yds.2': 'ReceivingYDs',
        'Att': 'PassingAtt',
        'Att.1': 'RushingAtt',
        'FantPt': 'FantasyPointsSTD',
    }, axis=1, inplace=True)

    # Add additional columns to dataset in order to identify more useful trends and patterns

    # Add columns for fantasy points (Half PPR & PPR)
    retVal['FantasyPointsHalfPPR'] = 0
    retVal['FantasyPointsPPR'] = 0
    # Calculate fantasy points based on the player's position
    for index, row_series in retVal.iterrows():
        if (retVal.at[index, 'FantPos'] == 'QB'):
            retVal.at[index, 'FantasyPointsHalfPPR'] = row_series['PassingTD'] * 4 + row_series['RushingYDs'] * 0.1 + row_series['RushingTD'] * 6 + row_series['Rec'] * 0.5 + row_series['ReceivingYDs'] * 0.1 + row_series['ReceivingTD'] * 6 - row_series['FL'] * 2 - row_series['Int'] * 2
            retVal.at[index, 'FantasyPointsPPR'] = row_series['PassingTD'] * 4 + row_series['RushingYDs'] * 0.1 + row_series['RushingTD'] * 6 + row_series['Rec'] * 1.0 + row_series['ReceivingYDs'] * 0.1 + row_series['ReceivingTD'] * 6 - row_series['FL'] * 2 - row_series['Int'] * 2
        elif (retVal.at[index, 'FantPos'] == 'RB'):
            retVal.at[index, 'FantasyPointsHalfPPR'] = row_series['RushingYDs'] * 0.1 + row_series['RushingTD'] * 6 + row_series['Rec'] * 0.5 + row_series['ReceivingYDs'] * 0.1 + row_series['ReceivingTD'] * 6 - row_series['FL'] * 2
            retVal.at[index, 'FantasyPointsPPR'] = row_series['RushingYDs'] * 0.1 + row_series['RushingTD'] * 6 + row_series['Rec'] * 1 + row_series['ReceivingYDs'] * 0.1 + row_series['ReceivingTD'] * 6 - row_series['FL'] * 2
        elif (retVal.at[index, 'FantPos'] == 'WR'):
            retVal.at[index, 'FantasyPointsHalfPPR'] = row_series['RushingYDs'] * 0.1 + row_series['RushingTD'] * 6 + row_series['Rec'] * 0.5 + row_series['ReceivingYDs'] * 0.1 + row_series['ReceivingTD'] * 6 - row_series['FL'] * 2
            retVal.at[index, 'FantasyPointsPPR'] = row_series['RushingYDs'] * 0.1 + row_series['RushingTD'] * 6 + row_series['Rec'] * 1 + row_series['ReceivingYDs'] * 0.1 + row_series['ReceivingTD'] * 6 - row_series['FL'] * 2
        elif (retVal.at[index, 'FantPos'] == 'TE'):
            retVal.at[index, 'FantasyPointsHalfPPR'] = row_series['RushingYDs'] * 0.1 + row_series['RushingTD'] * 6 + row_series['Rec'] * 0.5 + row_series['ReceivingYDs'] * 0.1 + row_series['ReceivingTD'] * 6 - row_series['FL'] * 2
            retVal.at[index, 'FantasyPointsPPR'] = row_series['RushingYDs'] * 0.1 + row_series['RushingTD'] * 6 + row_series['Rec'] * 1 + row_series['ReceivingYDs'] * 0.1 + row_series['ReceivingTD'] * 6 - row_series['FL'] * 2

    # Add column for Fantasy Points per Game
    retVal['FantasyPoints/GM'] = retVal['FantasyPointsHalfPPR'] / retVal['G']
    retVal['FantasyPoints/GM'] = retVal['FantasyPoints/GM'].apply(lambda x: round(x, 2))

    return retVal

df_2019 = cleanDataset("FF_data_2019.csv")


app = dash.Dash()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False), # represents the URl bar, doesnt render anything
    html.Div(id='page-content'), # content will be rendered in the html Div element
])

index_page = layouts.index_page()
test_page = layouts.test()
ff_2019 = layouts.ff_data()
ff_2020 = layouts.ff_data()



@app.callback(
    Output(component_id='page-content', component_property='children'),
    [Input(component_id='url', component_property='pathname')]
)
def display_page(pathname):
    if (pathname == '/ff-2019'):
        return ff_2019
    elif (pathname == '/ff-2020'):
        return ff_2020
    elif (pathname == '/test'):
        return test_page
    else:
        return index_page

# Connect the plotly graph with the dash components





if __name__ == '__main__':
    app.run_server(debug=True)

# ff_data_2019 = d.DataAnalyzer('FF_data_2019.csv') #Creates an object that analyzes the given csv file
######################################################################################################

# How did Targets + Rushing TDs correlate to fantasy points per game for Running Backs in 2019?
#ff_data.plotUsagePerGame('RB')
#ff_data.plotUsagePerGame('WR')


# How does efficiency correlate to fantasy football performance?
#ff_data.plotEfficiency('RB')
#ff_data.plotEfficiency('WR')

# How does rushing yards per attempt correlate with fantasy football points?
#ff_data.plotRushYardsPerAttempt('RB', 20) #at least 20 rushes in the season
######################################################################################################
# ff_data_2019.plotUsagePerGame('WR')
#
# # The plot shows that WR's with 8+ targets per game average 12+ ff points per game
# # Print a list of all WRs that averaged 8+ targets per game
# bestTargets = ff_data_2019.data_wr[ff_data_2019.data_wr['Usage/GM'] > 8]
# print('_______________________________________________________________')
# print(bestTargets)
#
# print('_______________________________________________________________')
# # Determine the highest targeted receiver's catch rates
# bestCatchRate = bestTargets[bestTargets['CatchRate'] > 0.75] #WR catches 75% of his targets
# print(bestCatchRate)
# #From this we can see that the only receiver to get 8+ targets a game and has a catch rate >75% is Michael Thomas
#
#
# print('_______________________________________________________________')
# # ff_data_2019.plotRushAttemptsPerGame()
#
# # The plots shows that RB's with 15+ rushes per game average 13+ ff points per game
# # Print a list of all RBs that averaged 15+ rushes per game
# bestRushAtt = ff_data_2019.data_rb[ff_data_2019.data_rb['RushAttempts/GM'] > 15] #get list of RBs who had >15 rushes per game
# print(bestRushAtt)