from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from sklearn.decomposition import PCA
from colory.color import Color
from sys import argv
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import subprocess
import argparse
import json
import sys
import os

import Pascal_Labels
import Dominant_Color
import Decision_Rule


def create_mpeg_features(data_set, jar_name):
    # creating feature vector for dataset and storing in csv
    subprocess.call(['java', '-jar', jar_name, '-f', data_set])


def read_feature_csv(file_name):
    # Read data set feature vectors
    feature = pd.read_csv(file_name, header=None).sort_values(0)
    # feature = feature.sort_values(0)
    # Dropping 1st column from the data frame
    vector = feature.drop(columns=[0])
    return feature, vector


# Method to calculate dimensions based on the co-variance
def calculate_dimensions(feature, feature_name):
    pca_dims = PCA()
    pca_dims.fit(feature)
    cum_sum = np.cumsum(pca_dims.explained_variance_ratio_)
    dim = np.argmax(cum_sum >= 0.95) + 1
    # print('{} Dimension : {}'.format(feature_name, dim))
    return dim


# Perfome PCA on data features
def fit_pca(dim, data_feature, query_feature):
    pca = PCA(n_components=dim)
    data_feature = pca.fit_transform(data_feature)
    # print('Data Feature Shape : {}'.format(data_feature.shape))
    query_feature = pca.transform(query_feature)
    # print('Query Feature Shape : {}'.format(query_feature.shape))
    return data_feature, query_feature


def get_label(name):
    start = name.find('_') + len('_')
    end = name.find('.')
    label = name[start:end]
    return label


# Display result images
def display_result(data, label):
    img_array = []
    for i in data.index:
        arr = []
        img = Image.open('pascal2009/JPEGImages/'+data[0][i])
        arr.append(img)
        arr.append(label.get(data[0][i]))
        img_array.append(arr)

    # Top 10 Search Results
    print('TOP 10 SEARCH RESULT')
    plt.figure(figsize=(15, 15))
    for i in range(len(img_array)):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(img_array[i][0], cmap=plt.cm.binary)
        plt.xlabel(img_array[i][1])
    plt.show()


def cld_calculations(features, vector, query_vector):
    dim = calculate_dimensions(vector, 'CLD')
    data_feature_cld, query_feature_cld = fit_pca(dim, vector, query_vector)
    # euclidean distance between query image and complete dataset
    euc_dis_cld = pd.DataFrame(euclidean_distances(query_feature_cld, data_feature_cld).flatten(), columns=['cld_dis'])
    dataset = pd.concat([features, euc_dis_cld], axis=1)
    # sorting result in descending order
    # euc_dis_result = dataset_cld.sort_values(by='cld_dis', ascending=True)[[0, 'cld_dis']].head(20)
    return dataset


def scd_calculations(features, vector, query_vector):
    dim = calculate_dimensions(vector, 'SCD')
    data_feature_scd, query_feature_scd = fit_pca(dim, vector, query_vector)
    # euclidean distance between query image and complete dataset
    euc_dis_scd = pd.DataFrame(euclidean_distances(query_feature_scd, data_feature_scd).flatten(), columns=['scd_dis'])
    dataset = pd.concat([features, euc_dis_scd], axis=1)
    # Euclidean Distance sorting
    # euc_dis_result = dataset_scd.sort_values(by='scd_dis', ascending=True)[[0, 'scd_dis']].head(20)
    return dataset


def ehd_calculations(features, vector, query_vector):
    dim = calculate_dimensions(vector, 'EHD')
    data_feature_ehd, query_feature_ehd = fit_pca(dim, vector, query_vector)
    # manhattan distance between query image and complete dataset
    man_dis_ehd = pd.DataFrame(
        manhattan_distances(query_feature_ehd, data_feature_ehd, sum_over_features=True).flatten(), columns=['ehd_dis'])
    dataset = pd.concat([features, man_dis_ehd], axis=1)
    # Manhattan Distance sorting
    # man_dis_result = dataset_ehd.sort_values(by='ehd_dis', ascending=True)[[0, 'ehd_dis']].head(20)
    return dataset


def create_features_csv():
    feature_df = pd.DataFrame(pd.concat([cld_features, scd_features_vector, ehd_features_vector, dataset_cld['cld_dis'],
                                       dataset_scd['scd_dis'], dataset_ehd['ehd_dis'],
                                         colours.rename(columns={0: 'colour'})], axis=1))
    feature_df.to_csv('output_features_combined.csv', index=False, header=False)


def get_image_colour(feature):
    arr = []
    for index, row in feature.iterrows():
        print(row[0])
        arr.append(Dominant_Color.get_dominant_color(row[0]))
    return pd.DataFrame(arr)


def run(query):
    # dataset = argv[1]
    # query = argv[2]
    labels = Pascal_Labels.run()
    # colour = Dominant_Color.get_dominant_color(query)
    # print('Dominant Colour : {}'.format(colour))

    # Run featuresmpeg.jar to create features
    create_mpeg_features('pascal2009/JPEGImages', 'featuresmpeg.jar')
    # Read the features into pandas dataframe
    cld_features, cld_features_vector = read_feature_csv('CLDFeature.csv')
    scd_features, scd_features_vector = read_feature_csv('SCDFeature.csv')
    ehd_features, ehd_features_vector = read_feature_csv('EHDFeature.csv')
    query_cld = cld_features.loc[cld_features[0] == query]
    query_scd = scd_features.loc[scd_features[0] == query]
    query_ehd = ehd_features.loc[ehd_features[0] == query]
    # Dropping 1st column from the dataframe
    query_cld_vector = query_cld.drop(columns=[0])
    query_scd_vector = query_scd.drop(columns=[0])
    query_ehd_vector = query_ehd.drop(columns=[0])
    dataset_cld = cld_calculations(cld_features, cld_features_vector, query_cld_vector)
    dataset_scd = scd_calculations(scd_features, scd_features_vector, query_scd_vector)
    dataset_ehd = ehd_calculations(ehd_features, ehd_features_vector, query_ehd_vector)
    # print(cld_result)
    cld_sim = dataset_cld['cld_dis'].values
    scd_sim = dataset_scd['scd_dis'].values
    ehd_sim = dataset_ehd['ehd_dis'].values
    colour_df = get_image_colour(cld_features)
    colour_df.to_csv('image_colour.csv', header=None, index=None)
    colours = pd.read_csv('image_colour.csv', header=None)

    sim_score = ((2 * cld_sim) + (0.5 * scd_sim) + (1 * ehd_sim)) / 3
    sim_score_df = pd.concat([cld_features[0], pd.DataFrame(sim_score, columns=['simval']),
                              pd.DataFrame(cld_sim, columns=['simcld']),
                              pd.DataFrame(scd_sim, columns=['simscd']),
                              pd.DataFrame(ehd_sim, columns=['simehd']),
                              colours.rename(columns={0: 'colour'})], axis=1)
    # print(sim_score_df)
    # Top 20 images
    # sim_score_sorted = sim_score_df.sort_values(by='simval', ascending=True).head(20)
    # print(sim_score_sorted)
    #
    # result = Decision_Rule.run(sim_score_sorted, sim_score_df.loc[sim_score_df[0] == query])
    # print(result)
    #
    # display_result(sim_score_sorted, labels)
    # create_features_csv()

    # Write csv file with similarity scores, colour and texture information
    # sim_score_df.to_csv('output.csv', index=False, header=False)
    # print('DONE!!!')
    return sim_score_df


if __name__ == '__main__':
    query = '2009_000001.jpg'
    run(query)
