def change_text_color(color):
    if type(color) == type("string"):    
        if color.title() == "Red":
            color = 31
        elif color.title() == "Green":
            color = 32
        elif color.title() == "Yellow":
            color = 33
        elif color.title() == "Blue":
            color = 34
        elif color.title() == "Default":
            color = 37
    color_string = "\033[0;" + str(color) + ";50m"
    print(color_string, end="")

def print_in_color(text, color, ending="\n"):
    change_text_color(color)
    print(text, end=ending)
    change_text_color(37)