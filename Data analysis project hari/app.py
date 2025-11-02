import pandas as pd
import numpy as np

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import pandas as pd
filename =("C:\\Users\veathavalli\\Downloads\\Paris-2024-Event-Programme.xlsx")
df = pd.read_excel(filename)
print(df.head ())