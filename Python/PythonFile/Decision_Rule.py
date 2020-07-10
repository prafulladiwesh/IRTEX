import pandas as pd
import numpy as np


colors = ['Dull Brown', 'Dark Maroon', 'Puce', 'Off Blue', 'Camouflage Green', 'Light Brown', 'Light Blue Grey',
        'Very Light Pink', 'Light Grey', 'Dusk', 'Sepia', 'Tomato', 'Sienna', 'Slate Grey', 'Cobalt', 'Beige',
        'Olive Drab', 'Dark Olive', 'Dust', 'Chocolate', 'Milk Chocolate', 'Military Green', 'Slate', 'Charcoal',
        'Dark Brown', 'Pine Green', 'Very Dark Green', 'Almost Black', 'Chestnut', 'Dusty Orange', 'Mossy Green',
        'Sand Brown', 'Dirty Green', 'Grey', 'Very Dark Brown', 'Dark Blue Grey', 'Camo', 'Cool Blue', 'Cinnamon',
        'Dark Khaki', 'Faded Blue', 'Mud Brown', 'Camel', 'Light Peach', 'Blue/Grey', 'Sandstone', 'Bluey Grey',
        'Brown Grey', 'Battleship Grey', 'Purpley Grey', 'Plum', 'Dirt', 'Pale', 'Muddy Green', 'Pale Rose',
        'Windows Blue', 'Navy Green', 'Swamp', 'Dark', 'Reddish Brown', 'Brownish Purple', 'Purple Brown', 'Black',
        'Very Light Brown', 'Khaki Green', 'Stormy Blue', 'Dark Grey', 'Pale Olive', 'Charcoal Grey', 'Pinkish Tan',
        'Gunmetal', 'Russet', 'Pinkish Grey', 'Grey Brown', 'Putty', 'Dirt Brown', 'Powder Blue', 'Greyish',
        'Dusty Blue', 'Cadet Blue', 'Sandy', 'Greyish Pink', 'Army Green', 'Khaki', 'Bluegrey', 'Tan Green',
        'Camo Green','Brownish Pink', 'Grey Purple', 'Greyblue', 'Marine', 'Cloudy Blue', 'Cool Grey',
        'Light Grey Blue', 'Dark Taupe', 'Pale Brown', 'Earth', 'Pale Grey', 'Blue Grey', 'Asparagus',
        'Dark Sky Blue', 'Silver', 'Brownish Grey', 'Indian Red', 'Bluish Grey', 'Drab', 'Sky Blue', 'Midnight',
        'Mushroom', 'Medium Grey', 'Bland', 'Grey/Blue', 'Taupe', 'Reddish Grey', 'Clay', 'Green Grey',
        'Steel Grey', 'Brown', 'Dark Mauve', 'Slate Green', 'Greyish Brown', 'Steel', 'Pine', 'Turtle Green',
        'Sand', 'Dark Grey Blue', 'Dark Tan', 'Coffee', 'Moss', 'Purplish Brown', 'Ugly Blue', 'Cement', 'Ice',
        'Dark Sage', 'Warm Grey', 'Purplish Grey', 'Mocha', 'Cocoa', 'Stone', 'Medium Blue', 'Dark Orange']
texture = ['water', 'terrain', 'grass', 'sky', 'indoor']
dic = {'sky': ['blue', 'grey', 'pink', 'cement', 'orange', 'yellow', 'cyan'],
       'water': ['blue', 'grey', 'cement', 'cyan'],
       'grass': ['green', 'olive', 'camouflage'],
       'terrain': ['grey', 'brown', 'clay', 'khaki', 'orange', 'camo', 'beige', 'camouflage', 'cement'],
       'indoor': ['red']}
fore_back = ['brown', 'red', 'yellow', 'white', 'cyan', 'green', 'purple', 'grey', 'orange', 'blue']


def read_csv(file_name):
    return pd.read_csv(file_name, header=None)


def get_key_from_value(val):
    for key, value in dic.items():
        if val == value:
            return key
    return val


def get_color(color):
    for col in colors:
        if color in col:
            return col


# attr1=imagecolor, attr2=, attr3=, attr4=foreground, attr5=background, attr6=texture
def decision_rules(image_id, attr1, attr2, attr3, attr4, attr5, attr6):
    print(image_id, attr1, attr2, attr3, attr4, attr5, attr6)
    if attr6 == 'water':
        color = get_color(attr1)
        key = get_key_from_value(color)
        if key == attr6:
            return key
    if attr6 == 'sky':
        color = get_color(attr1)
        key = get_key_from_value(color)
        if key == attr6:
            return key
    return arr


def run():
    attrs = read_csv('attributes.csv')
    print(attrs)
    print(set(attrs[6]))
    print(set(attrs[1]))
    print(set(attrs[4]))
    print(set(attrs[5]))
    arr = []
    for ind in attrs.index:
        small = decision_rules(attrs[0][ind], attrs[1][ind], attrs[2][ind], attrs[3][ind], attrs[4][ind],
                               attrs[5][ind], attrs[6][ind])
        arr.append(small)
    return arr


if __name__ == '__main__':
    run()
