import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import DataAnalyzer as d

ff_data_2019 = d.DataAnalyzer('FF_data_2019.csv') #Creates an object that analyzes the given csv file



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
ff_data_2019.plotUsagePerGame('WR')

# The plot shows that WR's with 8+ targets per game average 12+ ff points per game
# Print a list of all WRs that averaged 8+ targets per game
bestTargets = ff_data_2019.data_wr[ff_data_2019.data_wr['Usage/GM'] > 8]
print('_______________________________________________________________')
print(bestTargets)

print('_______________________________________________________________')
# Determine the highest targeted receiver's catch rates
bestCatchRate = bestTargets[bestTargets['CatchRate'] > 0.75] #WR catches 75% of his targets
print(bestCatchRate)
#From this we can see that the only receiver to get 8+ targets a game and has a catch rate >75% is Michael Thomas


print('_______________________________________________________________')
# ff_data_2019.plotRushAttemptsPerGame()

# The plots shows that RB's with 15+ rushes per game average 13+ ff points per game
# Print a list of all RBs that averaged 15+ rushes per game
bestRushAtt = ff_data_2019.data_rb[ff_data_2019.data_rb['RushAttempts/GM'] > 15] #get list of RBs who had >15 rushes per game
print(bestRushAtt)