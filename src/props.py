class bcolors:
    """ colors codes for colored writeouts to terminal
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def count_lines_endings(text):
    """function for counting line endings - number of lines

    Args:
        text (str): text to be processed

    Returns:
        int: number of lines ending
    """

    new_line_counter = 0
    for c in text:
        if c == "\n":
            new_line_counter += 1

    return new_line_counter