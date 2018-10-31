import base64
import json
import os
import mimetypes
import requests
from large_file_upload import LargeFileUpload
from small_file_upload import SmallFileUpload
from creds import KEY_ID, KEY, BUCKET_ID

def upload_file(file_name, local_dir, remote_dir):
	local_file = os.path.join(local_dir, file_name)
	remote_file = '{0}/{1}'.format(remote_dir, file_name)

	mimetype = mimetypes.guess_type(local_file)[0]
	content_type = mimetype if mimetype else 'application/octet-stream'

	id = KEY_ID
	key = KEY
	bucket_id = BUCKET_ID

	local_file_size = os.stat(local_file).st_size
	chunk_size = 52428800

	# authorize account
	id_and_key = '{0}:{1}'.format(id, key)
	basic_auth_string = 'Basic ' + base64.b64encode(id_and_key)
	headers = { 'Authorization': basic_auth_string }

	response = requests.get(
		'https://api.backblazeb2.com/b2api/v2/b2_authorize_account', 
		headers=headers
	)
	responseJson = response.json()

	data = {
		'file_name': file_name,
		'local_file': local_file,
		'local_dir': local_dir,
		'local_file_size': local_file_size,
		'chunk_size': chunk_size,
		'remote_file': remote_file,
		'content_type': content_type,
		'api_url': responseJson['apiUrl'],
		'bucket_id': bucket_id,
		'account_authorization_token': responseJson['authorizationToken']
	}

	# upload large file
	if local_file_size > chunk_size:
		upload = LargeFileUpload(data)
		upload.upload_large_file()
	# upload small file
	else:
		upload = SmallFileUpload(data)
		upload.upload_small_file()