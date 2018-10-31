import os
import json
import hashlib
import requests
from mark_done import mark_done

class LargeFileUpload:
    def __init__(self, data):
        self.file_name = data['file_name']
        self.local_file = data['local_file']
        self.local_dir = data['local_dir']
        self.local_file_size = data['local_file_size']
        self.remote_file = data['remote_file']
        self.content_type = data['content_type']
        self.chunk_size = data['chunk_size']
        self.api_url = data['api_url']
        self.bucket_id = data['bucket_id']
        self.account_authorization_token = data['account_authorization_token']

    def start_large_file_upload(self):
        data = json.dumps({ 'fileName': self.remote_file, 'contentType': self.content_type, 'bucketId': self.bucket_id })
        headers = { 'Authorization': self.account_authorization_token }

        response = requests.post('%s/b2api/v2/b2_start_large_file' % self.api_url, data=data, headers=headers)
        responseJson = response.json()

        self.file_id = responseJson['fileId']

    def get_upload_part_url(self):
        data = json.dumps({ 'fileId' : self.file_id })
        headers = { 'Authorization' : self.account_authorization_token }

        response = requests.post('%s/b2api/v2/b2_get_upload_part_url' % self.api_url, data=data, headers=headers)
        responseJson = response.json()

        self.upload_authorization_token = responseJson['authorizationToken']
        self.upload_url = responseJson['uploadUrl']

    def upload_chunk(self):
        size_of_part = self.chunk_size
        total_bytes_sent = 0
        part_no = 1
        part_sha1_array = []
        divider = '=========================='

        print divider

        while (total_bytes_sent < self.local_file_size):
            if ((self.local_file_size - total_bytes_sent) < self.chunk_size):
                size_of_part = self.local_file_size - total_bytes_sent
            filed = open(self.local_file)
            filed.seek(total_bytes_sent)
            file_data = filed.read(size_of_part)
            filed.close()
            sha1_digester = hashlib.new('SHA1')
            sha1_digester.update(file_data)
            sha1_str = sha1_digester.hexdigest()
            part_sha1_array.append(sha1_str) 

            headers = {
                'Authorization': self.upload_authorization_token,
                'X-Bz-Part-Number': str(part_no), 
                'Content-Length':  str(size_of_part), 
                'X-Bz-Content-Sha1': sha1_str
            }

            requests.post(self.upload_url, data=file_data, headers=headers)

            total_bytes_sent = total_bytes_sent + size_of_part
            part_no += 1

            percentage = round((total_bytes_sent / float(self.local_file_size)) * 100, 1)

            print '{0} of {1} bytes sent'.format(total_bytes_sent, self.local_file_size) 
            print '{0}{1} complete'.format(percentage, '%')
            print divider
        
        self.part_sha1_array = part_sha1_array

    def finish_large_file_upload(self):
        data = json.dumps({ 'fileId' : self.file_id, 'partSha1Array': self.part_sha1_array})
        headers = { 'Authorization': self.account_authorization_token }

        response = requests.post('%s/b2api/v2/b2_finish_large_file' % self.api_url, data=data, headers=headers)

        if response.status_code == 200:
            mark_done(self.local_dir, self.file_name)
        else:
            print response.json()

    def upload_large_file(self):
        self.start_large_file_upload()
        self.get_upload_part_url()
        self.upload_chunk()
        self.finish_large_file_upload()



