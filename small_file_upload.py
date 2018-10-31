import json
import hashlib
import requests
from mark_done import mark_done

class SmallFileUpload:
    def __init__(self, data):
        self.file_name = data['file_name']
        self.local_file = data['local_file']
        self.local_dir = data['local_dir']
        self.remote_file = data['remote_file']
        self.content_type = data['content_type']
        self.api_url = data['api_url']
        self.bucket_id = data['bucket_id']
        self.account_authorization_token = data['account_authorization_token']

    def get_upload_url(self):
        data = json.dumps({ 'bucketId' : self.bucket_id })
        headers = { 'Authorization': self.account_authorization_token }

        response = requests.post('%s/b2api/v2/b2_get_upload_url' % self.api_url, data=data, headers=headers)
        responseJson = response.json()

        self.upload_url = responseJson['uploadUrl']
        self.upload_authorization_token = responseJson['authorizationToken']

    def upload_file(self):
        file_data = open(self.local_file).read()
        sha1_of_file_data = hashlib.sha1(file_data).hexdigest()

        headers = {
            'Authorization' : self.upload_authorization_token,
            'X-Bz-File-Name' : self.remote_file,
            'Content-Type' : self.content_type,
            'X-Bz-Content-Sha1' : sha1_of_file_data
        }

        response = requests.post(self.upload_url, data=file_data, headers=headers)

        if response.status_code == 200:
            mark_done(self.local_dir, self.file_name)
        else:
            print response.json()
    
    def upload_small_file(self):
        self.get_upload_url()
        self.upload_file()