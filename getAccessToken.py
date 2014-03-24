import dropbox

APP_KEY = 'o3n6u096tbfspas'
APP_SECRET = '9um8m6mlzfiyx6o'


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

getAccess_token()