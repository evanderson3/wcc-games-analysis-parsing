# --------------------
# This script takes in a file path for a specific WCC match, 
# and produces a DataFrame for the entire event. 
# --------------------

# loading packages
import chess.pgn
import pandas as pd
from parse_game import get_game_df

# for testing
import datetime

# given a path to a pgn file, returns a DF representation of the event
def make_file_df(path):

   # opening file
   file = open(path, encoding='cp1252')

   # for storing games
   game_df_list = []

   # establishing a naming convention.
   match_name = path.replace('WCC_Matches/', '').replace('.pgn', '')
   game_id_num = 1

   # iterating over games in file
   finished = False
   while not finished:

      # parsing using a pgn reader
      game = chess.pgn.read_game(file)

      # detecting end of file
      if game == None:
         finished = True
      else:
         # using custom function to format pgn data into DataFrame
         game_id = match_name + '_game' + str(game_id_num)

         start_time = datetime.datetime.now()
         game_df = get_game_df(game, game_id)
         finish_time = datetime.datetime.now()

         print(game_id)
         print('...', finish_time - start_time)
         print()

         # adding to our list, incrementing game_id
         if not game_df.empty:
            game_df_list.append(game_df)
            game_id_num += 1

   # closing file
   file.close()
   
   # combining games into a master DF
   file_df = pd.concat(game_df_list)
   file_df.reset_index(drop=True, inplace=True)
   file_df.to_csv("matches/" + match_name + ".csv")

   return file_df