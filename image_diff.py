# import the necessary packages
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import gaussian_filter1d
from skimage.measure import compare_ssim
from Score import Score
import os
import argparse
import imutils
import cv2
import numpy as np
import subprocess

# Get the number in the file name to sort the files
def getImageNumber(string):
	if "image" in string: 
		string = string.lstrip("image")
		string = string.rstrip(".jpg")
		resp = int(string)
		return resp

# Get frames from video
os.chdir('/Users/ShanePereira/Movies/Test')
subprocess.call(['ffmpeg', '-i', 'testvideo.mov', 'image%d.jpg'])

# Get a list of images
imageNames = os.listdir("/Users/ShanePereira/Movies/Test")
imageNames = [x for x in imageNames if "image" in x]
# Sort the list on the numbers returned by the function
imageNames = sorted(imageNames, key=getImageNumber)

# Init list
images = []

# For name in the list imageNames add the path
for n in range(len(imageNames)):
	path = "/Users/ShanePereira/Movies/Test/{}".format(imageNames[n])
	images.append(cv2.imread(path))

# init list
gray = []

# For every image in list image convert it to grey image
for n in range(len(images)):
	gray.append(cv2.cvtColor(images[n], cv2.COLOR_BGR2GRAY))

# init some results
highest = 0
lowest = 1
results = []

# For every in list grey
# if n is not last in list
# get the SSIM of the two images
# append the SSIM using a Score object 
for n in range(len(gray)):
	if(n < len(gray)-1):
		(score, diff) = compare_ssim(gray[n], gray[n+1], full=True)
		diff = (diff * 255).astype("uint8")
		print("SSIM: {}".format(score))

		imageName1 = 'image{}.jpg'.format(n)
		imageName2 = 'image{}.jpg'.format(n+1)
		results.append(Score(score,imageName1,imageName2))

		if score > highest:
			highest = score
		if score < lowest:
			lowest = score

lowest = "lowest: {}".format(lowest)
highest = "highest: {}".format(highest)

print(lowest)
print(highest)

# If a result in the list is > 0.99 it means there is barely/no difference between images
# these images are removed
for i in range(len(results)):
	if(results[i].score > 0.99):
		os.chdir('/Users/ShanePereira/Movies/Test')
		os.remove(results[i].img2)

# Get a new list of images (removed images are gone)
imageNames = os.listdir("/Users/ShanePereira/Movies/Test/")
imageNames = [x for x in imageNames if "image" in x]
# Sort the list on the numbers returned by the function
imageNames = sorted(imageNames, key=getImageNumber)
path = "/Users/ShanePereira/Movies/Test/"

# Rename all the images
for n in range(len(imageNames)):
	src = path + imageNames[n]
	dst = path + "image" + str(n) + ".jpg"
	os.rename(src, dst)

# Turn the images into a video again
os.chdir('/Users/ShanePereira/Movies/Test')
subprocess.call(['ffmpeg', '-f', 'image2', '-i', 'image%d.jpg', 'output.mpg'])

# Create a plot, make it smooth using a gaussian filter
# resultsSmooth = gaussian_filter1d(results, sigma = 10) 
# plt.plot(range(0, len(results)), resultsSmooth)
# plt.show()



