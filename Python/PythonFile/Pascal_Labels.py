from os import listdir, getcwd
from os.path import join
import xml.etree.ElementTree as ET
import pandas as pd
import pickle
import csv
import os


def convert_annotation(image_id, dict, classes):
    in_file = open('pascal2009/Annotations/%s.xml' % image_id)
    tree = ET.parse(in_file)
    root = tree.getroot()
    labels = set()
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls in classes:
            labels.add(cls)
    dict[image_id+'.jpg'] = list(labels)
    return dict


def write_labels_dic(dic):
    # output = open('pascal_labels.csv', 'w')
    # writer = csv.writer(output)
    # for key, value in dic.items():
    #     writer.writerow([key, value])
    # output.close()

    with open('pascal_labels.csv', 'w') as f:
        for key in dic.keys():
            f.write("%s,%s\n"%(key, dic[key]))


def write_df(df):
    df.to_csv('labels.csv', header=None)


def set_label_value(dic, query_label):
    arr = []
    for key, value in dic.items():
        for val in value:
            if query_label == val:
                arr.append('1')
            else:
                arr.append('0')
    return arr


def run():
    sets = ['train', 'val']
    classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    labels_dict = {}

    wd = getcwd()

    for image_set in sets:
        if not os.path.exists('pascal2009/labels/'):
            os.makedirs('pascal2009/labels/')
        image_ids = open('pascal2009/ImageSets/Main/%s.txt' % image_set).read().strip().split()
        list_file = open('%s.txt' % image_set, 'w')
        for image_id in image_ids:
            list_file.write('%s/pascal2009/JPEGImages/%s.jpg\n' % (wd, image_id))
            labels_dict = convert_annotation(image_id, labels_dict, classes)
        list_file.close()
    labeldf = pd.DataFrame.from_dict(labels_dict, orient='index')
    write_df(labeldf)
    # write_labels_dic(labels_dict)
    # print(labels_dict)
    # return labels_dict


if __name__ == '__main__':
    run()
