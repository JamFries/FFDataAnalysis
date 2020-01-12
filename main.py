import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import DataAnalyzer as d

ff_data = d.DataAnalyzer('2019-2.csv') #Creates an object that analyzes the given csv file

######################################################################################################

# How did Targets + Rushing TDs correlate to fantasy points per game for Running Backs in 2019?
ff_data.plotUsagePerGame('RB')
ff_data.plotUsagePerGame('WR')


# How does efficiency correlate to fantasy football performance?
ff_data.plotEfficiency('RB')
ff_data.plotEfficiency('WR')

# How does rushing yards per attempt correlate with fantasy football points?

