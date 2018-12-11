"""
Created on 07 December 2018
@author: Yonas Teodros Tefera
@brief : frame selector
"""
from processing import Reconstruction
import os
parent=Reconstruction('/media/yonas/DACACEA3CACE7B71/Yonas/Dataset/IIT_back/back_3_2','/media/yonas/DACACEA3CACE7B71/Yonas/Dataset/IIT_back/back_3_2/images')

print parent.datasets_path
print parent.output_path
print parent.getImage_path()
'''
Frame extraction

#I frame
#os.system("ffmpeg -i /media/yonas/DACACEA3CACE7B71/Yonas/Dataset/IIT_back/back_3/MVI_4755.MP4 -vf 'select=eq(pict_type\,I)' -vsync vfr /media/yonas/DACACEA3CACE7B71/Yonas/Dataset/IIT_back/back_3/extracted/frame-%04d.png")
#
'''
os.system("ffmpeg -i /media/yonas/DACACEA3CACE7B71/Yonas/Dataset/IIT_back/back_3/MVI_4755.MP4 -vf fps=30 -vsync vfr /media/yonas/DACACEA3CACE7B71/Yonas/Dataset/IIT_back/back_3/extracted/frame-%04d.png")


print "................................."
print "................................."
print "------>Feature Extraction<-------"
print "................................."
print "................................."
extract=parent.feature_extractor('')
print extract

print "................................."
print "................................."
print "------>Feature Matching<---------"
print "................................."
print "................................."
match=parent.exhaustive_matcher('')
print match

print "................................."
print "................................."
print "------> Mapping<-----------------"
print "................................."
print "................................."

mapper=parent.mapper('')
print mapper

print "................................."
print "................................."
print "------> Undistortion step<--------"
print "................................."
print "................................."

undistort=parent.Image_Undistorter(' --output_type COLMAP  --max_image_size 2000')
print undistort


print "................................."
print "................................."
print "-> Dense Sterio matching<--------"
print "................................."
print "................................."

sterio=parent.Dense_Stereo('  --workspace_format COLMAP  --PatchMatchStereo.geom_consistency true')
print sterio

print "................................."
print "................................."
print "--->Dense fusing Running<--------"
print "................................."
print "................................."

fuser=parent.Dense_Fuser('  --workspace_format COLMAP  --input_type geometric')
print fuser

print "Poisson Surface Reconstruction..."
print "................................."
print "................................."
print "->Poisson Surface Reconstruction<-"
print "................................."
print "................................."
Mesher=parent.Dense_Mesher('')
print Mesher
