from datetime import datetime

def log_with_time(message):
    current_time = datetime.now().strftime("%H:%M")
    print(f"[{current_time}] {message}")


def error_with_time(message):
    log_with_time(f"(╥‸╥) {message}")


def log_items_with_time(message):
    log_with_time(f"♡♡♡ {message} ♡♡♡")


def log_path_with_time(message):
    log_with_time(f"{message} ᐟ.⊹.˚୧")


def log_header_with_time(message):
    log_with_time(f"˖⁺‧₊˚♡˚ {message} ˚♡˚₊‧⁺˖")


def input_with_time(message):
    current_time = datetime.now().strftime("%H:%M")
    log_with_time(f"Enter {message} 𖦹 ⋆｡°✩")
    result = input(f"[{current_time}] ===> ").strip()
    return result