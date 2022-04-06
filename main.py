# --------------------
# This script iterates over all of the files in a specific directory,
# calling a custom function (see parse_file.py) on each file, and combines
# the returned DFs into a master DF containing information from all WCC game.
# --------------------

# loading packages
import pandas as pd
import os

# for testing
import datetime

# loading custom modules
from parse_file import make_file_df

# our main scripting function
def main():

   # listing all of our files
   directory_name = 'WCC_Matches'
   pgn_files = os.listdir(directory_name)

   # here we'll store the DataFrames from each event
   file_df_list = []

   # iterating over files, creating a DataFrame of games each time
   file_paths = [directory_name + '/' + x for x in pgn_files]
   for path in file_paths: 
      
      file_df = make_file_df(path)
      file_df_list.append(file_df)

   # combining the event DataFrames
   all_games_df = pd.concat(file_df_list)
   all_games_df.reset_index(drop=True, inplace=True)
   all_games_df.to_csv("all_games.csv")

start_time = datetime.datetime.now()
main()
finish_time = datetime.datetime.now()

print("Total run time: " + str(finish_time - start_time))