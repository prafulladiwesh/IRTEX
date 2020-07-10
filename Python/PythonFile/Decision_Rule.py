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
        for v in value:
            if val.lower() == v.lower():
                return key
    # return val


def get_color(color):
    for col in colors:
        if color in col:
            return True
    return False


# attr1=imagecolor, attr2=foreground, attr3=background, attr4=texture, attr5=objects
def decision_rules(attr1, attr2, attr3, attr4, attr5):
    if 'airplane' in attr5.lower():
        if attr3.lower() == 'green':
            return 'grass'
        elif attr3.lower() == 'blue' or attr3.lower() == 'grey':
            return 'sky'
    if 'horse' in attr5.lower() or 'cow' in attr5.lower() or 'sheep' in attr5.lower() or 'dog' in attr5.lower():
        if attr3.lower() == 'green':
            return 'grass'
        elif attr3.lower() == 'blue' or attr3.lower() == 'grey' or attr3.lower() == 'white':
            return 'snow'
    if 'train' in attr5.lower():
        return 'terrain'
    if 'ship' in attr5.lower():
        return 'water'
    if 'person' in attr5.lower():
        if attr3.lower() == 'green':
            return 'grass'
        if 'horse' in attr5.lower():
            return 'grass'
        if attr3.lower() == 'purple':
            return 'indoor'
    if attr4 == 'water':
        tex = rules(attr1, attr3)
        return attr5 if tex is None else tex
    if attr4 == 'sky':
        tex = rules(attr1, attr3)
        return attr5 if tex is None else tex
    if attr4 == 'terrain':
        return 'Roads or Rail Tracks'
    return attr4


def rules(attr1, attr3):
    if get_color(attr1):
        key1 = get_key_from_value(attr1)
        key3 = get_key_from_value(attr3)
        if key1 != key3:
            return key3
        return key1


# def run():
#     attrs = read_csv('example.csv')
#     for ind in attrs.index:
#         tex = decision_rules(attrs[0][ind], attrs[1][ind], attrs[2][ind], attrs[3][ind], attrs[4][ind],
#                              attrs[5][ind])
#         attrs[4][ind] = tex
#         print(attrs)
#     return tex


def run(att1, att2, att3, att4, att5):
    return decision_rules(att1, att2, att3, att4, att5)


if __name__ == '__main__':
    run(att1, att2, att3, att4, att5)
