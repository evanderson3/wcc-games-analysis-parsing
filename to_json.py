import pandas as pd
import os

# getting a list of our games
game_file_list = os.listdir('games')

# iterating over games
for game_file in game_file_list:

   if game_file != '.DS_Store':

      # games DataFrame
      game_df = pd.read_csv("games/" + game_file, index_col=0)
      game_id = game_file.replace(".csv", '') # useful

      # subsetting and writing to json
      game_df = game_df[['game_id', 'event', 'round', 'date', 'white', 'black', 'move_color', 'move', 'evaluation']]
      game_df.reset_index(drop=True, inplace=True)
      game_df['ply_number'] = game_df.index
      game_df.to_json('json/' + game_id + '.json', orient="records")

# getting a list of our matches
match_file_list = os.listdir('matches')

# iterating over games
for match_file in match_file_list:

   match_id = match_file.replace(".csv", "")

   match_df = pd.read_csv("matches/" + match_file, index_col=0)
   match_df.drop(columns=['white_elo', 'black_elo'], inplace=True)

   match_df.to_json('json/' + match_id + '.json', orient="records")