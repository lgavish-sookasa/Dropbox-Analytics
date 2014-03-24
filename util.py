import dropbox
import json
import os

class User:
	def __init__(self, access_token, path):
		client = dropbox.client.DropboxClient(access_token)
		self.client = client
		self.fileList = []
		self.deletedFileList = []
		self.folderList = []
		self.deletedFolderList = []
		self.explore('/')

	def getClient(self):
		return self.client

	def getFileList(self):
		return self.fileList

	def deletedFileList(self):
		return self.deletedFileList

	def folderList(self):
		return self.folderList

	def deletedFolderList(self):
		return self.deletedFolderList
	'''
		Returns a dictionary or JSon of the metadata of a file or folder at path
	'''
	def getMetaData(self, path, type = 'dictionary'):
		folder_metadata = self.getClient().metadata(path, list=True, file_limit=25000, hash=None, rev=None, include_deleted=True)
		if type == 'dictionary':
			return folder_metadata
		else:
			return json.dumps(folder_metadata)
	
	'''
		Returns a string indicating type of content
	'''
	def contentType(self, content):
		if content["is_dir"] == True:
			if "is_deleted" in content.keys():
				return "Deleted Folder"
			else:
				return "Folder"
		else:
			if "is_deleted" in content.keys():
				return "Deleted File"
			else:
				return "File"

	'''
		Populates four lists(deletedFileList, deletedFolderList, fileList, folderList) with respective objects using naive Depth-first search
	'''			
	def explore(self, path):
		metaData = self.getMetaData(path)
		for content in metaData["contents"]:
			if self.contentType(content) == "Deleted Folder":
				contentObj = DeletedFolder(content)
				self.deletedFolderList.append(contentObj)
				self.explore(contentObj.getPath())
			elif self.contentType(content) == "Folder":
				contentObj = Folder(content)
				self.folderList.append(contentObj)
				self.explore(contentObj.getPath())
			elif self.contentType(content) == "File":
				contentObj = File(content)
				self.fileList.append(contentObj)
			elif self.contentType(content) == "Deleted File":
				contentObj = DeletedFile(content)
				self.deletedFileList.append(contentObj)
			else:
				print "Error"

	'''
		Returns a sorted list of tuples(size, File object)
	'''
	def sortFileListBySize(self):
		sizeList = []
		for f in self.fileList:
			sizeList.append((f.getSize(), f))
			sizeList.sort()
		return sizeList

	def getLargestFile(self):
		return self.sortFileListBySize()[-1][1]

	def getSmallestFile(self):
		return self.sortFileListBySize()[0][1]

	'''
		Returns a list of File or deletedFile objects with extention ext
	'''
	def findExt(self, ext, deleted = True):
		extList = []
		if deleted == True:
			for f in self.deletedFileList:
				if f.getExt() == ext:
					extList.append(f)
		else:
			for f in self.fileList:
				if f.getExt() == ext:
					extList.append(f)
		return extList

	def extCount(self, ext, deleted = True):
		return len(self.findExt(ext, deleted))

	def fileCount(self):
		return len(self.fileList)

	def deletedFileCount(self):
		return len(self.deletedFileList)

	def folderCount(self):
		return len(self.folderList)

	def deletedFolderCount(self):
		return len(self.deletedFolderList)

	def simpleAnalytics(self):
		print "Total number of files(deleted and non-deleted) is:\t\t " , self.fileCount() + self.deletedFileCount()
		print "Total number of non-deleted files is:\t\t\t\t ", self.fileCount()
		print "Total number of deleted files is:\t\t\t\t ", self.deletedFileCount()

		print "Total number of folders(deleted and non-deleted) is:\t\t " , self.folderCount() + self.deletedFolderCount()
		print "Total number of non-deleted folders is:\t\t\t\t ", self.folderCount()
		print "Total number of deleted folders is:\t\t\t\t ", self.deletedFolderCount()

		print "Total number of files with extention .pdf is:\t\t\t ", self.extCount('.pdf', True) +  self.extCount('.pdf', False)
		print "Total number of files with extention .txt is:\t\t\t ", self.extCount('.txt', True) +  self.extCount('.txt', False)
		print "Total number of files(deleted) with extention .txt is:\t\t ", self.extCount('.txt', True)
		print "Total number of files(non-deleted) with extention .txt is:\t ", self.extCount('.txt', False)
		
		smallestFile = self.getSmallestFile()
		largestFile = self.getLargestFile()
		print "Smallest File is:\t ", smallestFile.getPath(), " at size ", smallestFile.getSize(), " Bytes"
		print "Largest File is:\t ", largestFile.getPath(), " at size ", largestFile.getSize(), " Bytes"




class Content:
	def __init__(self, content):
		self.content = content

	def getContent(self):
		return self.content

	def getSize(self):
		return self.content["bytes"]

	def isDeleted(self):
		if "is_deleted" in self.getContent().keys():
			self.isDeleted = True
		else:
			self.isDeleted = False

	def getPath(self):
		return self.content["path"]
		
class File(Content):
	def getExt(self):
		name,ext = os.path.splitext(self.getContent()["path"])
		return ext
	def isDeleted(self):
		return False


class Folder(Content):
	def isDeleted(self):
		return False

class DeletedFile(File):
	def isDeleted(self):
		return True

class DeletedFolder(Folder):	
	def isDeleted(self):
		return True	
