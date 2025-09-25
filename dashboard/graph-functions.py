"""File containing the functions needed to create the figures 
required for the LMNH dashboard."""

import datetime

import pandas as pd
import altair as alt
import numpy as np


dft = pd.DataFrame({'A': ['spam', 'eggs', 'spam', 'eggs'] * 6,
                   'B': ['alpha', 'beta', 'gamma'] * 8,
                    'C': [np.random.choice(pd.date_range(datetime.datetime(2013, 1, 1), datetime.datetime(2013, 1, 3))) for i in range(24)],
                    'D': np.random.randn(24),
                   'E' : np.random.random_integers(0, 4,24)})

## List of figures needed:
