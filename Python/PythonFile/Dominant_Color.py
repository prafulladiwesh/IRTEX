from __future__ import print_function
from PIL import Image
import binascii
import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import webcolors

# Used GitHub color implementation -  https://github.com/apoorvaeternity/colory
from colory.color import Color


def get_dominant_color(image):
    NUM_CLUSTERS = 5

    # print('reading image')
    im = Image.open('pascal2009/JPEGImages/'+image)
    im = im.resize((150, 150))  # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    # print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    # print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
    counts, bins = np.histogram(vecs, len(codes))  # count occurrences

    index_max = np.argmax(counts)  # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    # print('most frequent is %s (#%s)' % (peak, colour))
    # print('Most frequent color is %s' % ('#' + colour))
    colour = Color('#' + colour, 'xkcd')
    return colour.name


if __name__ == '__main__':
    get_dominant_color(image)

