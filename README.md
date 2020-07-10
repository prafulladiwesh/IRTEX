# Project Introduction

This project is about building an image retrieval system which includes Global and Local Textual as well as visual explanations about the selected image with query image. It helps user to understand the reason for the retrieval of certains images.
  This is a Scientific Team Project with a team size of 4.
  
### Motivation:
The main idea behind an image retrieval is to understand the notion of similarity. It is difficult to define the similarity. So it is interesting to see how a retrieval system decide on similarity. And is it possible to explain the working of retrieval system to an user.

### System Design:

![Architecture](https://github.com/prafulladiwesh/IRTEX/blob/master/Images/IRArchitecture.png)


### Goal of the Project:

### Datasets used for this project:

### Implementation Steps:

### Results:



# Individual Contribution:

This branch contains files for extracting low level features based on MPEG-7 color, shape and texture descriptors.
Repository has 2 parts :
  1. Java application : MPEGFeatureExtraction
  2. Python Notebook for Image Search


## 1. Java application : MPEGFeatureExtraction
The MPEG-7 Descriptors used for feature extraction are :
  1. Color Descriptor:
      1. Scalable Color Descriptor: It is a color histogram in the HSV color space. It has a scalable binary representation                                       over a large granularity range. The scalability is achieved in terms for bit representation and bin numbers.
      2. Color Layout Descriptor: It represents a very compact spatial layout of color image. An 8x8 thumbnail of the image is                                   generated which is encoded and quantized.
      3. Edge Histogram Descriptor: It represents spatial distribution of total five edges – four directional and one non-                                         directional edges. Each edge is consisting of local histograms which can be aggregated as global histogram.
  2. Shape Descriptor:
      1. Region-Based Shape Descriptor: The descriptor expresses the region-based shape of an object. Multiple objects with                                           discontinuous regions can be described by this descriptor. It gives a compact and efficient way of describing properties of multiple disjoint regions simultaneously.
      
 
### To run this java application below are the steps to follow :

  ### Feature Extraction runnable JAR name : featuresmpeg.jar
  #### The mpegfeatures.jar can be found at Java/MPEGFeatureExtractor/mpegfeatures.jar in this repository
  ### To Extract complete dataset features :
    Command : java -jar mpegfeatures.jar -f cifar10/cifar10/train
       • -f : token to indicate dataset feature generation
       • cifar10/cifar10/train : name of the directory
    Output file name : CLDFeature.csv, SCDFeature.csv, EHDFeature.csv
    Output file location : same as runnable jar location
    
## 2. Python Notebook and files
The searching and manipulation of features and images in this project are done using python programming.
There are many python notebooks for different types of implementation.
We have used 2 different datasets for the image search implementation. They are 
  1. CIFAR-10 dataset : Implemented in CifarMpegIndividualFeatures.ipynb notebook.
                        Implemented Individual Descriptor Feature Extraction and applying Linear Regression to get the contribution of each descriptor in the final retrieval. The experiment is done in CifarMpegIndividualFeatures.ipynb notebook. It can be found at Python/Notebook/CifarMpegIndividualFeatures.ipynb
                        #### This notebook can be found at Python/Notebook/CifarMpegIndividualFeatures.ipynb
  2. PASCAL dataset : Implemented in PascalPython.ipynb notebook.
                      #### This notebook can be found at Python/Notebook/PascalPython.ipynb
  
  These notebooks contains call to mpegfeatures.jar for feature extraction and when using these python notebooks there is no     need to run the mpegfeatures.jar file seperately for feature extraction.

Apart from notebooks there are also Python runnable files which can be run from command prompt. For this keep the mpegfeatures.jar and AnotherPython.py runnable python files in the same directory.

The MPEG_Features.py file contain all the implemention and is the master file for this feature. All the other implementation files are called and accessed using this master file. The descriptions and workings of all the files are below:
1. MPEG_Features.py - Main file which has reading dataset and similarity calculations for query image.
2. Decision_Rule.py - Decision rules for better global and textual explanations(Under work).
3. Dominant_Color.py - To get the dominant color information of the image.
4. Pascal_Labels.py - To get the multiple lables for pascal dataset.

The command for running these python files are :
  #### To Extract complete dataset features :
    Command : python3 AnotherPython.py -f cifar10/cifar10/train
       • -f : token to indicate dataset feature generation
       • cifar10/cifar10/train : name of the directory
    Output file name : CLDFeature.csv, SCDFeature.csv, EHDFeature.csv
    Output file location : same as runnable jar location
  
  ##### Note that the name of runnable python file is AnotherPython.py (name will be changed in some time) which will do all the work. The file can be located at Python/PythonFile/AnotherPython.py in this repository.
  
  Some of the sample query and results are displayed below:
  
  Query Image :
   
  ![Query Image](https://github.com/stevemanavalan/IRTEX/blob/mpeg7_features/Images/query_image.png)
  
  Results :
  ![Result Image](https://github.com/stevemanavalan/IRTEX/blob/mpeg7_features/Images/result_images.png)
  
