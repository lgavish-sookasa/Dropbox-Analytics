import dropbox
import json
import os

class User:
	def __init__(self, access_token):
		client = dropbox.client.DropboxClient(access_token)
		self.client = client
		self.fileList = []
		self.deletedFileList = []
		self.folderList = []
		self.deletedFolderList = []

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

	def getMetaData(self, path, type = 'dictionary'):
		folder_metadata = self.getClient().metadata(path, list=True, file_limit=25000, hash=None, rev=None, include_deleted=True)
		if type == 'dictionary':
			return folder_metadata
		else:
			return json.dumps(folder_metadata)
	
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
				print "appending file!"
				contentObj = File(content)
				self.fileList.append(contentObj)
			elif self.contentType(content) == "Deleted File":
				contentObj = DeletedFile(content)
				self.deletedFileList.append(contentObj)
			else:
				print "Error"

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
		name,ext = os.path.splitext(self.getContent["path"])
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