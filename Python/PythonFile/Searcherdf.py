# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 12:40:09 2020

@author: steve
"""



import pandas as pd
import os
import numpy as np
import json
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.linear_model import LinearRegression
import math
#from MPEG_Features import run
from segment import MPEG_Features
class Searcherdf:
    def __init__(self, indexPath):
        # store our index path
        self.indexPath = indexPath
    def search(self, queryImage, limit = 20):
        results = {}
        
        y_train = [0,0,0,0,0,0,0,0,0,0,0,0]
                        
        """############################################## Local Feature Descriptors F1  #####################"""
        
        feature_1 = MPEG_Features.run(os.path.basename(queryImage))
        f1_simcld = feature_1['simcld']
        simcld_F1 = pd.DataFrame(f1_simcld.div(f1_simcld.max()).values, columns=['simcld_F1'])
        f1_simscd = feature_1['simscd']
        simscd_F1 = pd.DataFrame(f1_simscd.div(f1_simscd.max()).values, columns=['simscd_F1'])
        f1_simehd = feature_1['simehd']
        simehd_F1 = pd.DataFrame(f1_simehd.div(f1_simehd.max()).values, columns=['simehd_F1'])

        f1_sim = feature_1['simval']
        sim_F1 = pd.DataFrame(f1_sim.div(f1_sim.max()).values, columns=['simval_F1'])
        #print(sim_F1)
        """############################################## Local Feature Descriptors F1 #####################"""
        
        
        """############################################## Foreground and Background F2 -SEGMENTATION #####################"""
        ######################################## Begin put indexed file to df #############################
        data_features_F2 = pd.read_csv('index_pascal_2009_2k.csv', header=None)
        data_attributes_F2 = data_features_F2.iloc[:,-5:]
        data_features_F2 = data_features_F2.iloc[:,0:data_features_F2.shape[1]-5]
        data_feature_vector_F2 = data_features_F2.drop(columns=[0])   
        ####################################### End put indexed file to df ##############################
        
        ######################################## put query feature to df #############################
        #query_feature_vector = pd.DataFrame(queryFeatures)
        #query_feature_vector = query_feature_vector.transpose() 
        query_feature_F2 = data_features_F2.loc[data_features_F2[0] == os.path.basename(queryImage)]
        query_feature_vector_F2 = query_feature_F2.drop(columns=[0])
        ########################################end put query feature to df #############################
        ######################################## begin caluclate distance #############################
        dtexturefg = euclidean_distances(data_feature_vector_F2.iloc[:,0:102],query_feature_vector_F2.iloc[:,0:102])
        dshapefg =   euclidean_distances(data_feature_vector_F2.iloc[:,102:127],query_feature_vector_F2.iloc[:,102:127])
        dcolorfg =   euclidean_distances(data_feature_vector_F2.iloc[:,127:207],query_feature_vector_F2.iloc[:,127:207])
        dcolorbg =   euclidean_distances(data_feature_vector_F2.iloc[:,207:287],query_feature_vector_F2.iloc[:,207:287])
        dtexturebg = euclidean_distances(data_feature_vector_F2.iloc[:,287:],query_feature_vector_F2.iloc[:,287:])
        ######################################## end caluclate distance #############################
        ######################################## Begin z-score Normalization #############################
        #ztexturefg = stats.zscore(dtexturefg)
        #zshapefg = stats.zscore(dshapefg)
        #zcolorfg = stats.zscore(dcolorfg)
        #zcolorbg = stats.zscore(dcolorbg)
        #ztexturebg = stats.zscore(dtexturebg)
        distval_F2 = 3*dtexturefg + 2*dshapefg + 2*dcolorfg + .5*dcolorbg + 2*dtexturebg
        maxval_F2 = distval_F2.max()
        data_attributes_F2['dtexturefg'] = 3*dtexturefg/maxval_F2
        data_attributes_F2['dcolorfg'] = 2*dcolorfg/maxval_F2
        data_attributes_F2['dcolorbg'] = .5*dcolorbg/maxval_F2
        data_attributes_F2['dtexturebg'] = 2*dtexturebg/maxval_F2
        sim_F2 =  pd.DataFrame(distval_F2, columns=['simval_F2']).div(maxval_F2)
        ######################################## End z-score Normalization #############################       
        """############################################## Foreground and Background F2 -SEGMENTATION #####################"""
        
        
        """############################################## HLD F3 #####################"""
        ######################################## Begin put indexed file to df #############################
        data_features_F3 = pd.read_csv('index_vgg_pascal2009_2k.csv', header=None)
        data_attributes_F3 = data_features_F3.iloc[:,-2:]
        data_features_F3 = data_features_F3.iloc[:,0:512]
        data_feature_vector_F3 = data_features_F3.drop(columns=[0])
        ####################################### End put indexed file to df ##############################
        
        ######################################## put query feature to df #############################
        query_feature_F3 = data_features_F3.loc[data_features_F3[0] == os.path.basename(queryImage)]
        query_feature_vector_F3 = query_feature_F3.drop(columns=[0])
        ########################################end put query feature to df #############################
        dist_F3 = euclidean_distances(data_feature_vector_F3, query_feature_vector_F3)        
        maxval = dist_F3.max()
        sim_F3 =  pd.DataFrame(dist_F3, columns=['simval_F3']).div(maxval)        
        """############################################## HLD F3 #####################"""     
                    
        #######################################################################################################
        labels = pd.read_csv('labels.csv', header=None)        
        labels = labels.iloc[:,-5:].fillna(0)
        #print(labels)
           
        #####################################################  cmombine FV ##############################################################
       
        #simvalue = reg.coef_[0]*sim_F1.values + reg.coef_[1]*sim_F2.values +  reg.coef_[2]*sim_F3.values + reg.intercept_
        simvalue = .5*sim_F1.values + sim_F2.values + 2*sim_F3.values
        #simvalue = sim_F2.values + 2*sim_F3.values
        sim_F1F2F3 = pd.DataFrame(simvalue, columns=['simval'])
        dataset_result = pd.concat([data_features_F2[0], sim_F1F2F3,sim_F1,sim_F2,sim_F3,simcld_F1,simscd_F1,simehd_F1,feature_1.iloc[:,-1:],data_attributes_F2,data_attributes_F3,labels], axis=1)
        #dataset_result = pd.concat([data_features_F2[0], sim_F1F2F3,sim_F2,sim_F3,data_attributes_F2,data_attributes_F3], axis=1)
        sort_result_F4 = dataset_result.sort_values(by='simval', ascending=True).head(12)   
        #####################################################  cmombine FV ################
        ##############################################
               
        
        ##################################################3 Linear Regression for global explanation ###################################        
        queryLabel = sort_result_F4.loc[sort_result_F4[0] == os.path.basename(queryImage)]
        queryLabel = queryLabel.iloc[0,-5:].values
        
        for l in queryLabel:
            if l != 0:           
                i=0
                for index, row in sort_result_F4.iterrows():                    
                    if l == row[1] or l == row[2] or l == row[3] or l == row[4] or l == row[5]:
                        y_train[i] += 1                       
                    i+=1        
                                       
        sort_result_F4 = pd.concat([sort_result_F4.reset_index(),pd.DataFrame(y_train, columns=['y_train']).astype(bool).astype(int)],axis=1)        
        x_train = sort_result_F4.iloc[:,2:5]          
        clf = LinearRegression()
        # train
        clf = clf.fit(x_train, sort_result_F4['y_train'])
        # predict                
        ##################################################3 Linear Regression for global explanation ###################################
                  
        # converting result to json format
        json_array = []
        for i in sort_result_F4.index:
            results[os.path.basename(sort_result_F4[0][i])] = os.path.basename(str(sort_result_F4['simval'][i]))        
            x = {
                    "name": os.path.basename(sort_result_F4[0][i]),
                    "score1": str(sort_result_F4['simval_F1'][i]),
                    "score2": str(sort_result_F4['simval_F2'][i]),
                    "score3": str(sort_result_F4['simval_F3'][i]),
                    "weights":str(clf.coef_[0])+","+str(clf.coef_[1])+","+str(clf.coef_[2]),
                    "cld":str(sort_result_F4['simcld_F1'][i]),
                    "scd":str(sort_result_F4['simscd_F1'][i]),
                    "ehd":str(sort_result_F4['simehd_F1'][i]),
                    "imagecolor": str(sort_result_F4['colour'][i]),
                    "fgtexture" :str(sort_result_F4['dtexturefg'][i]),
                    "fgcolor":  str(sort_result_F4['dcolorfg'][i]),
                    "bgcolor":  str(sort_result_F4['dcolorbg'][i]),
                    "bgtexture": str(sort_result_F4['dtexturebg'][i]),
                    "foregroundcolor":str(sort_result_F4[390][i]),
                    "backgroundcolor":str(sort_result_F4[391][i]),
                    "foregroundhue":str(sort_result_F4[392][i]),
                    "backgroundhue":str(sort_result_F4[393][i]),
                    "texture":str(sort_result_F4[394][i]),
                    "object":str(sort_result_F4[513][i]),
                    "objectcount":str(sort_result_F4[514][i])
                    }

            json_array.append(x)
            # convert into JSON:
            json_data = json.dumps(json_array)
        print(json_data)
        return results
            
    def chi2_distance(self, histA, histB, eps = 1e-10):
        # compute the chi-squared distance        
        d = pd.DataFrame((.5*(histA.values-histB.values) **2)/(histA.values+histB.values), columns=histB.columns)
        d = d.sum(axis=1)
        return d
