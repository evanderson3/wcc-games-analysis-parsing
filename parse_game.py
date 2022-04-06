import pandas as pd
import chess.pgn
from stockfish import Stockfish

import datetime

# cleans the date into a parsable format
def get_clean_date(date):
   clean_date = date.replace('.', '-')
   return clean_date
      
# cleans the eval object into a readable string
def get_clean_eval(eval_object):

   # unpacking object
   eval_type = eval_object['type']
   eval_val = eval_object['value'] / 100

   # creating string to build up
   eval_string = ""

   # adding direction of eval
   if eval_val < 0:
      eval_string += "-"

   if eval_type == "Mate":
      eval_string += "M"

   # adding value to string
   eval_string += str(abs(eval_val))

   return eval_string

# returns a clean eval string, given the current board
def get_eval(board, stockfish):

   # fen representation of curr position
   curr_fen = board.fen()

   # setting stockfish position and analyzing
   stockfish.set_fen_position(curr_fen)
   evaluation = get_clean_eval(stockfish.get_evaluation())

   return evaluation

# returns a list of moves and corresponding evals
def analyze_game(game):

   # creating board that we can analyze on
   new_board = chess.Board()

   # initializing our Stockfish engine
   stockfish = Stockfish(parameters={'Threads': 4})
   engine_depth = 15
   stockfish.set_depth(engine_depth)

   # initializing our lists for storing moves and evals
   moves_list = []
   eval_list = []

   # iterating over game moves
   mainline = list(game.mainline_moves())

   # iterating over moves
   for m in range(0, len(mainline)):

      try: 
         # getting algabraic notation of current move
         move_san = new_board.san(mainline[m])

         # making move, analyzing position
         new_board.push(mainline[m])
         pos_eval = get_eval(new_board, stockfish)

         # appending items to respective lists
         moves_list.append(move_san)
         eval_list.append(pos_eval)

      except AssertionError:
         print('invalid move')
         return [], []

   return moves_list, eval_list

# returns a df representation of the game
def get_game_df(game, game_id): 

   # parsing pgn into a game object
   # game = chess.pgn.read_game(pgn_file)
   game_info = game.headers

   # analyzing game
   moves, evals = analyze_game(game)

   # adding color info
   colors = []
   for m in range(len(moves)):
      if m%2 == 0:
         colors.append('white')
      elif m%2 != 0:
         colors.append('black')

   # creating DataFrame
   game_df = pd.DataFrame({
      'game_id': game_id,
      'move_color': colors,
      'move': moves,
      'evaluation': evals,
      'event': game_info['Event'],
      'site': game_info['Site'],
      'date': get_clean_date(game_info['Date']),
      'round': game_info['Round'],
      'white': game_info['White'],
      'white_elo': game_info['WhiteElo'],
      'black': game_info['Black'],
      'black_elo': game_info['BlackElo'],
      'result': game_info['Result'],
      'eco': game_info['ECO']
   })

   # merging with ECO opening names
   eco_codes = pd.read_csv("eco_openings.csv")
   game_df = game_df.merge(eco_codes, on='eco', how='left')

   # writing full df to csv
   game_df.to_csv('games/' + game_id + '.csv')

   # we can be doing the opposite of this screener earlier on
   if len(game_df.index) > 0:
      # subsetting a single row for placing in master df
      game_info_df = game_df.drop(['move_color', 'move', 'evaluation'], axis=1)
      game_info_df = game_info_df.iloc[[0]]

      return game_info_df

   return game_df
