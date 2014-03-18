import dropbox
import json
import os
APP_KEY = 'o3n6u096tbfspas'
APP_SECRET = '9um8m6mlzfiyx6o'
ACCESS_TOKEN = 'INSTERT ACCESS_TOKEN'


def getAccess_token():
	app_key = APP_KEY
	app_secret = APP_SECRET

	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

	# Have the user sign in and authorize this token
	authorize_url = flow.start()
	print '1. Go to: ' + authorize_url
	print '2. Click "Allow" (you might have to log in first)'
	print '3. Copy the authorization code.'
	code = raw_input("Enter the authorization code here: ").strip()

	# This will fail if the user enters an invalid authorization code
	access_token, user_id = flow.finish(code)

	client = dropbox.client.DropboxClient(access_token)
	print 'linked account: ', client.account_info()
	print 'access token: ' , access_token
	#TODO - automate grabbing the token

def authenticate(access_token):
	client = dropbox.client.DropboxClient(access_token)
	return client


def getMetaData(client, path, type = 'dictionary'):
	folder_metadata = client.metadata(path, list=True, file_limit=25000, hash=None, rev=None, include_deleted=True)
	if type == 'dictionary':
		return folder_metadata
	else:
		return json.dumps(folder_metadata)

#really need to change from tuples to dict
def explore(client, path):
	fileDict = {}
	metaData = getMetaData(client, path)
	for content in metaData["contents"]:
		name,ext = os.path.splitext(content["path"])
		newPath = content["path"]
		if content["is_dir"] == False:
			# print "Exploring File:\t\t\t" , newPath
			if "is_deleted" in content.keys():
				# should really use dictionary instead of tuple
				fileDict[newPath] = (content["bytes"], 'file', "deleted", ext)
			else:
				fileDict[newPath] = (content["bytes"], 'file', "not-deleted", ext)
		else:
			# print "Exploring Folder:\t\t", newPath 
			if "is_deleted" in content.keys():
				fileDict[newPath] = (content["bytes"], 'folder', "deleted")
			else:
				fileDict[newPath] = (content["bytes"], 'folder', "not-deleted")
			rDict = explore(client, newPath)
			fileDict.update(rDict)
	return fileDict

#should improve naming scheme to accurately depict what's in dict
def removeFoldersFromDict(fileDict):
	copyDict = fileDict.copy()
	for key in fileDict:
		if fileDict[key][1] == 'folder':
			del copyDict[key]
	return copyDict

def countFiles(fileDict):
	fileCount = 0
	dfileCount = 0
	folderCount = 0
	dfolderCount = 0
	for content in fileDict:
		if fileDict[content][1] == 'file':
			fileCount += 1
			if fileDict[content][2] == "deleted":
				dfileCount += 1
		else:
			folderCount += 1
			if fileDict[content][2] == "deleted":
				dfolderCount += 1
	return fileCount, dfileCount, folderCount, dfolderCount


def sortBySize(fileDict):
	sizeList = []
	for key in fileDict.keys():
		if fileDict[key][1] == 'file' and fileDict[key][2] != 'deleted':
			sizeList.append((fileDict[key][0], key))
	sizeList.sort()
	return sizeList

def findByExt(fileDict, ext):
	extList = []
	for key in fileDict.keys():
		if fileDict[key][3] == ext:
			extList.append(key);
	return extList

client = authenticate(ACCESS_TOKEN)
fileDict = explore(client, '/')
# print getMetaData(client, '/', type = 'json')
fileCount, dfileCount, folderCount, dfolderCount = countFiles(fileDict)
print "Total number of files is: " , fileCount
print "Total number of deleted files is: ", dfileCount
print "Total number of folders is: " , folderCount
print "Total number of deleted folders is: ", dfolderCount
print "Total number of non-deleted files is: ", fileCount - dfileCount
print "Total number of non-deleted folders is: ", folderCount - dfolderCount

fileDict = removeFoldersFromDict(fileDict)
sizeList = sortBySize(fileDict)
print "Smallest File is: " , sizeList[0][1], "at " , sizeList[0][0] , " bytes"
print "Largest File is: " , sizeList[-1][1], "at " , sizeList[-1][0] , " bytes"


print "These are the .txt files " , findByExt(fileDict, '.txt')
print "These are the .pdf files " , findByExt(fileDict, '.pdf')
