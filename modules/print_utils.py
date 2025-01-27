from modules.log_utils import get_divider_with_time, get_log_header_with_time, get_log_with_time

def print_info():
    menu_options = [
        # {"id": "0", "header": "Info", "description": "Display information about the script and its functionalities."},
        # {"id": "1", "header": "Print menu", "description": "Display the available menu options."},
        {"id": "1", "header": "Info", "description": "Display information about the script and its functionalities."},
        {"id": "2", "header": "New directory path", "description": "Change the current directory path.",
         "input": "'directory path'"},
        {"id": "3", "header": "Auto", "description": "Automatically performs the following actions: Rename, Move, Convert, Compress, and Remove.",
         "input": "'files name'", "from": "'directory path'", "to": "'directory path'"},
        {"id": "4", "header": "Rename", "description": "Renames all files in the directory that contain a volume number. Extracts numbers from the name and adds them in the format 'v***'.",
         "input": "'files name'", "from": "'directory path'", "to": "'directory path'",
         "example": "'something (something) 1 something' ==> 'files name v001'"},
        {"id": "5", "header": "Move files", "description": "Moves all cbz and cbr files to the 'archives' folder and all pdf files to the 'pdf' folder.",
         "from": "'directory path'", "to": "'archives' and 'pdf' subfolders"},
        {"id": "6", "header": "Convert files", "description": "Clone and converts all cbz and cbr files to pdf files.",
         "from": "'archives' subfolder", "to": "'pdf' subfolder"},
        {"id": "7", "header": "Compress files", "description": "Clone and compress files from the 'pdf' folder into the 'compressed' folder.",
         "from": "'pdf' subfolder", "to": "'compressed' subfolder"},
        {"id": "8", "header": "Remove subfolders", "description": "Moves files from the 'compressed' folder to its parent directory and deletes subfolders: 'archives', 'pdf', 'compressed'.",
         "from": "'compressed' subfolder", "to": "'directory path'"},
        {"id": "9", "header": "Combine pdf files", "description": "Combines all pdf files in the directory into a single pdf file.",
         "from": "'directory path'", "to": "'directory path'"},
        {"id": "10", "header": "Combine subfolders images", "description": "Combines all image files in the subfolders into a single pdf file.",
         "from": "'directory path' subfolders", "to": "'pdf' subfolder"}
    ]

    print(get_log_header_with_time("Info"))

    for option in menu_options:
        print(get_log_with_time(f"   {option['id']}. {option['header']}"))
        print(get_log_with_time(option['description']))
        
        if 'input' in option:
            print(get_log_with_time(f"Input:  {option['input']}"))
        
        if 'from' in option:
            print(get_log_with_time(f"From:   {option['from']}"))
        
        if 'to' in option:
            print(get_log_with_time(f"To:     {option['to']}"))
        
        if 'example' in option:
            print(get_log_with_time(f"Example: {option['example']}"))

        print(get_divider_with_time())
        print()

def print_menu():
    menu_options = [
        # {"id": "0", "label": "Info"},
        # {"id": "1", "label": "Print menu"},
        {"id": "1", "label": "Info"},
        {"id": "2", "label": "New directory path"},
        {"id": "3", "label": "Auto"},
        {"id": "4", "label": "Rename"},
        {"id": "5", "label": "Move to subfolders"},
        {"id": "6", "label": "Convert"},
        {"id": "7", "label": "Compress"},
        {"id": "8", "label": "Remove subfolders"},
        {"id": "9", "label": "Combine pdf files"},
        {"id": "10", "label": "Combine subfolders images"}
    ]
    
    print(get_log_header_with_time("Choose an action"))
    
    for option in menu_options:
        print(get_log_with_time(f"    {option['id']}. {option['label']}"))
    
    print(get_divider_with_time())
    print()