import re

pattern = re.compile("[0-9BbRr]+")
if pattern.fullmatch("5487R21rBB") : print("yeah")
else : print("ney")