from skimage import io
#from skimage import data_dir
#import numpy as np


im1 = io.imread('/home/octavian/github/lojux/imgs-input/p-j.jpg')
print 'im1: ', im1
print io.plugins()

#ic = io.ImageCollection('/home/octavian/github/lojux/imgs-input/*')
#print 'ic: ', ic
#print('length: ', len(ic))
#print('ic[0]: ', ic[0])
#print('shape: ', ic[0].shape)
