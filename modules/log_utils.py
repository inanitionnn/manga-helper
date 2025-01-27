import os
from datetime import datetime

def get_log_with_time(message):
    current_time = datetime.now().strftime("%H:%M")
    return f"[{current_time}] {message}"

def get_divider_with_time():
   return get_log_with_time("~~~~~~~~~~~(◕‿◕)~~~~~~~~~~~")

def get_error_with_time(message):
  return  get_log_with_time(f"(╥‸╥) {message}")


def get_log_items_with_time(message):
   return get_log_with_time(f"♡♡♡ {message} ♡♡♡")


def get_log_path_with_time(message):
 return   get_log_with_time(f"{message} ε(´｡•᎑•`)っ ➤")


def get_log_header_with_time(message):
   return get_log_with_time(f"˖⁺‧₊˚♡˚ {message} ˚♡˚₊‧⁺˖\n")


def input_with_time(message):
    current_time = datetime.now().strftime("%H:%M")
    print()
    print(get_log_with_time(f"Please, enter {message} 𖦹 ⋆｡°✩"))
    result = input(f"[{current_time}] ===> ").strip()
    return result

def clear_terminal(directory_path):
   os.system('cls||clear')
   print(get_log_with_time(f"···· {directory_path} ····\n"))
   