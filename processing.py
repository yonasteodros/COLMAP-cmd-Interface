#!/usr/bin/python
"""
Created on 07 December 2018
@author: Yonas Teodros Tefera
@brief : frame selector
"""
import errno
import os
import subprocess
import shutil
import sys
import shlex
class Reconstruction(object):
	def __init__(self,datasets_path,output_path):
		self.colmap_binary_path = '/usr/local/bin/colmap'
 		self.datasets_path = datasets_path
  		self.output_path = output_path
  		self.database_path = datasets_path + '/' +'rest.db'
  		self.image_path=datasets_path + '/' + 'images'
		self.input_path = datasets_path + '/' + 'sparse'+ '/' + '0'
		self.workspace_path = datasets_path + '/' +'dense'
  	def Call(self,command):
		print "calling function"
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	 	while True:
			output = proc.stdout.readline()
			print output.strip()
			if output == '' and proc.poll() is not None:
				break
	        if output:
	            print output.strip()
		rc = proc.poll()
  		return rc
	def MakeDirsExistOk(self,directory_path):
		try:
			os.makedirs(directory_path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	def feature_extractor(self,options):
		options=' --database_path ' + self.database_path + ' --image_path ' + self.image_path + options
		call =  (os.path.join('/usr/local/bin/colmap feature_extractor') + options)
		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	 	stdout, stderr = proc.communicate()
		print stdout
		if proc.returncode != 0:
			print('Call failed with error code ' + str(proc.returncode) + stderr)
			sys.exit(1)
		else:
			return stdout
	def exhaustive_matcher(self,options):
		options=' --database_path ' + self.database_path + options
		call =  (os.path.join('/usr/local/bin/colmap exhaustive_matcher') + options)
		 
		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	 	stdout, stderr = proc.communicate()
		if proc.returncode != 0:
			print('Call failed with error code ' + str(proc.returncode) + stderr)
			sys.exit(1)
		else:
			return stdout
	def mapper(self,options):
		# Loop over all directories in datasets_path.
		for dir_name in os.listdir(self.datasets_path):
			dir_path = os.path.join(self.datasets_path, dir_name)
			if not os.path.isdir(dir_path):
				continue
    		# Skip if output already present.
			sparse = os.path.join(self.datasets_path,'sparse')
			dense =  os.path.join(self.datasets_path,'dense')
			output_file_path = os.path.join(self.output_path, dir_name + '.ply')
			timing_file_path = os.path.join(self.output_path, dir_name + '.txt')
			if os.path.isfile(output_file_path) and os.path.isfile(timing_file_path):
				print('Skipping since output already present: ' + dir_name)
 				continue
		
		self.MakeDirsExistOk(sparse)
		options =' --database_path ' + self.database_path + ' --image_path ' + self.image_path + ' --output_path ' + sparse + options 
		call =  (os.path.join('/usr/local/bin/colmap mapper') + options)
		 
		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	 	stdout, stderr = proc.communicate()
		if proc.returncode != 0:
			print('Call failed with error code ' + str(proc.returncode) + stderr)
			sys.exit(1)
		else:
			return stdout

	def Image_Undistorter(self,options):
		dense =  os.path.join(self.datasets_path,'dense')
		self.MakeDirsExistOk(dense)
		options=' --image_path ' + self.image_path + ' --input_path ' + self.input_path + ' --output_path ' + dense +  options 
 		call =  (os.path.join('/usr/local/bin/colmap image_undistorter') + options)
		
		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = proc.communicate()
		if proc.returncode != 0:
			print('Call failed with error code ' + str(proc.returncode) + stderr)
			sys.exit(1)
		else:
			return stdout
	def Dense_Stereo(self,options):
		options=' --workspace_path ' + self.workspace_path + options
		call =  (os.path.join('/usr/local/bin/colmap patch_match_stereo ') + options)
		
		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	 	stdout, stderr = proc.communicate()
		if proc.returncode != 0:
			print('Call failed with error code ' + str(proc.returncode) + stderr)
			sys.exit(1)
		else:
			return stdout
	def Dense_Fuser(self,options):
		dense =  os.path.join(self.datasets_path,'dense')
		self.MakeDirsExistOk(dense)
		output_file_fused=os.path.join(dense + '/' + 'fused.ply')
		output_file_meshed=os.path.join(dense + '/' + 'meshed.ply')
		options=' --workspace_path ' + self.workspace_path + options + ' --output_path ' + output_file_fused
		call =  (os.path.join('/usr/local/bin/colmap stereo_fusion') + options)
		
		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	 	stdout, stderr = proc.communicate()
		if proc.returncode != 0:
			print('Call failed with error code ' + str(proc.returncode) + stderr)
			sys.exit(1)
		else:
			return stdout
	def Dense_Mesher(self,options):
		output_file_fused=os.path.join(dense + '/' + 'fused.ply')
		output_file_meshed=os.path.join(dense + '/' + 'meshed.ply')
		options=' --input_path ' + output_file_fused + ' --output_path ' + output_file_meshed + options
		call =  (os.path.join('/usr/local/bin/colmap poisson_mesher') + options)
		
		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	 	stdout, stderr = proc.communicate()
		if proc.returncode != 0:
			print('Call failed with error code ' + str(proc.returncode) + stderr)
			sys.exit(1)
		else:
			return stdout

	def setDatasets_path(self,datasets_path):
		self.datasets_path = datasets_path
  		self.output_path = output_path
  	def setOutput_path(self,output_path):
		self.datasets_path = datasets_path
  		self.output_path = output_path
  	def getDatasets_path(self):
  		return self.datasets_path
  	def getOutput_path(self):
  		return self.output_path
  	def setImage_path(self,image_path):
  		self.image_path=image_path
  	def getImage_path(self):
  		return self.image_path
