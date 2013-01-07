#PYTHON SCRIPT:pdf2bookreader

#!usr/bin/python

####################################

def MakeFile(file_name):

	"""
		MakeFile(file_name): makes a file.
	"""
	temp_path =homepath+'/'+ file_name   
	file = open(temp_path, 'w')
	file.write('')
	file.close()
####################################
def Makedir(dir_name):
    """
    Makedir(dir_name):makes a directory.
    """
    try:
    	temp_path =homepath+'/'+dir_name
    	#if os.path.exists(temp_path)==False:
    	os.mkdir(temp_path)
    	#else:
    		#print 'using the already existing '+dir_name
    except OSError:
   		pass		
####################################
def get_dirname(sourcepdf):

	"""
		get_dirname(sourcepdf): extract the name of input pdf file.
	"""
	try:
		if os.path.exists(sourcepdf)==False:
			print sourcepdf +' : No such file exists'
			print 'specify the correct path'
			sys.exit()
			
		else:
			pathelements=sourcepdf.split('/')
			no_elements=len(pathelements)
			getfilename=pathelements[no_elements-1]
			name=getfilename.split('.')
			if len(name) !=2:
				print "gave the extension of file"
				sys.exit()	

			if name[1] != 'pdf' :
				print 'Invalid file type, enter the name of the file in pdf format'
				sys.exit()
			else:
				dirname=name[0]
			
	except OSError:
		pass	
		
	return dirname
####################################
def convert_pdf(sourcepdf,destn_path):

	"""
		convert_pdf(sourcepdf,destn_path): run the command to convert pdf file to images
	"""

	command='convert'+' '+sourcepdf+' '+destn_path+'000.jpg'
	os.system(command)
	
####################################
def rename_files(destn_path):

	"""
		rename_files(destn_path): rename the image files created.
	"""
	try:
		filenames=os.listdir(destn_path)
 
		for filename in filenames:
			name=filename.split('.')
			num=name[0].split('-')
			if int(num[1])<10:
				newfilename='000'+num[1]+'.jpg'

			elif (int(num[1])>10 and int(num[1])<100):
				newfilename='00'+num[1]+'.jpg'
			else:
				newfilename='0'+num[1]+'.jpg'
			
			os.rename(destn_path+filename, destn_path+newfilename)
			if os.path.exists(destn_path+filename)==True:
				os.remove(destn_path+filename)
		newfilenames=os.listdir(destn_path)
		newfilenames.sort()
		no_leaves=len(newfilenames)
		
	except OSError:
		pass
    	
	#print 'the image files after renamed:'    
	#print newfilenames

	return no_leaves
####################################
def copy_data(sourcefile,destinfile,vars):
	"""
		copy_data(sourcefile,destinfile,vars): copies data from source file to destination and make the string substitutions
	"""
	template=open(sourcefile,'r')
	create=open(destinfile,'w')
	content=template.read() 
	if vars != None:
		content=content%vars
	create.write(content)
	template.close()
	create.close()


####################################
def create_images(dirname,sourcepdf):

	"""
		create_images(dirname,sourcepdf): create the image folder 
	"""
	Makedir(dirname+'/images')
	destn_path=dirname+'/images/'
	filenames=os.listdir(destn_path)
	for filename in filenames:
		if os.path.exists(destn_path+filename)==True:
			os.remove(destn_path+filename)

	convert_pdf(sourcepdf,destn_path)
	no_leaves=rename_files(destn_path)
	
	return no_leaves
			
####################################
def create_index(dirname):

	"""
		create_index(dirname): create the index file
	"""
	MakeFile(dirname+'/index.html')
	vars=None
	copy_data('index.html',dirname+'/index.html',vars)

####################################
def create_bookreaderJS(dirname,no_leaves):

	"""
		create_bookreaderJS(dirname,no_leaves): create the bookreader.js file
	"""
	MakeFile(dirname+'/bookreader.js')
	vars={'width': 800 , 'height': 1200 ,'leaf_imageurl' : '\'images/\'','no_leaves' : no_leaves}
	copy_data('bookreader.js',dirname+'/bookreader.js',vars)

####################################
def create_BookReaderCSS(subdir):

	"""
		create_BookReaderCSS(subdir): create the BookReader.css file
	"""
	MakeFile(subdir+'/BookReader.css')
	vars=None
	copy_data('bookreader/BookReader.css',subdir+'/BookReader.css',vars)
	
####################################
def create_BookReaderJS(subdir):

	"""
		create_BookReaderJS(subdir): create the BookReader.js file
	"""
	MakeFile(subdir+'/BookReader.js')
	vars=None
	copy_data('bookreader/BookReader.js',subdir+'/BookReader.js',vars)
	
####################################
def copy_file(filename,source,destn):

	"""
		 copy_file(filename,source,destn): copy files from source to destination
	"""
	try:
		shutil.copy(source+filename,destn)       
	except OSError:
		pass

####################################
def create_Images(subdir):

	"""
		 create_Images(subdir): create images subdirectory
	"""
	Makedir(subdir+'/images')
	#copying files
	destn=subdir+'/images'
	source='bookreader/images/'
	try:
		filenames=os.listdir(source)
		for filename in filenames:
			copy_file(filename,source,destn)		    
	except OSError:
		pass
			

####################################
def main(sourcepdf):

	"""
		 main(sourcepdf): main method
	"""
 	dirname=get_dirname(sourcepdf)
	#create folder 
	print 'creating ' + dirname
	Makedir(dirname)
	#create images folder
	print 'creating images folder'
	no_leaves=create_images(dirname,sourcepdf)
	#create index.html 
	print 'creating index.html file'
	create_index(dirname)
	#create bookreader.js file 
	print 'creating bookreader.js file'
	create_bookreaderJS(dirname,no_leaves)
	#create BookReader directory
	subdir=dirname+'/BookReader'
	print 'creating BookReader directory'
	Makedir(subdir)
	#create /BookReader/BookReader.css
	print 'creating /BookReader/BookReader.css'
	create_BookReaderCSS(subdir)
	#create /BookReader/BookReader.js
	print 'creating /BookReader/BookReader.js'
	create_BookReaderJS(subdir)
	#create the images'  folder /BookReader/images
	print 'creating images\' folder /BookReader/images\''
	create_Images(subdir)


####################################
 
if __name__ == "__main__":
  	import sys
	import os
	import shutil
	import string

	if len(sys.argv) != 2:
		print "Usage : python pdf2bookreader.py  <path> <name_of_pdf_file.pdf>"
		sys.exit()
		
	homepath=os.getcwd()

	main(sys.argv[1])

####################################




