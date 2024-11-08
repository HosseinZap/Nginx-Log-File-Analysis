import pandas as pd
from IPython.display import display
import os

# finds the test.csv temporary file
current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)
csvfile = os.path.join(current_directory, "test.csv")


table = pd.read_csv(csvfile)    # creates a dataframe from the csv file
display(table)

print(table.isnull().sum())     # lists the number of NULL values in the table based on columns

# replaces NULL string literals in the IP column with pandas NAN value. in the following, NAN values are filled with 0.0.0.0 to indicate an invalid IP address
table['IP'] = table['IP'].replace("NULL", pd.NA)
table = table.fillna("0.0.0.0")

print(table.isnull().sum())     # lists the number of missing values again to demonstrate the changes in the data
display(table)    

table.to_csv(os.path.join(current_directory, "cleaned.csv"), index=False)   # stores the cleaned table in another csv file called cleaned.csv in the same directory