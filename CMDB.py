########################

#Author : Venugopal P
#Python version : 3.6.8
#Requirements : requests,json,os.
#Purpose : To pull asset details from CMDB

########################

import requests
import json
import pandas as pd
import os
import sys

class Cherwell:

  def __init__(self, url):
    self.server    = url
    self.api_url   = "https://{}/CherwellAPI" . format(self.server)
    self.headers   = {"Content-Type": "application/json"}
    self.token     = ""
    self.auth_mode = "Internal"
    self.boid = "93dada9f640056ce1dc67b4d4bb801f69104894dc8" #config server BOID
    self.session = requests.session()

  def authenticate(self):
    '''
    Authentication part
    '''
    user = <base64 encoded username>
    passwd = <utf-16 encoded passwd>
    apiKey = <hex encoded apikey>
    user_name  = user.decode('base64')
    password   = passwd.decode('utf-16')
    api_key    = apiKey.decode('hex')
    grant_type = "password"

    uri = "{}/token?auth_mode={}&api_key={}" . format(self.api_url, self.auth_mode, api_key)
    requestBody = {
                    "accept":     "application/json",
                    "grant_type": grant_type,
                    "client_id":  api_key,
                    "username":   user_name,
                    "password":   password
                  }

    response = requests.post(uri, headers=self.headers, data=requestBody)

    response_decoded = response.json()
    token = response_decoded["access_token"]
    self.token = token
    self.headers["Authorization"] = "Bearer {}" . format(self.token)
    return token

  def getCmdb(self):
    uri = "https://{}/CherwellAPI/api/V1/getsearchresults".format(self.server)
    request_body = {
    "busObId": self.boid,
    "pageSize" : 5000,
    "fields" : ["93db94f556e932fd3239504767babd1bfb6c013bb6","9379053db492ece14816704ef5a9e3e567e217511b","93790597a2bebf214063ac4f8096aa5e3ead9b3da5","938b7febc3ddfd3cd2402549638f14ca223c437e40","945cf0c46f228bb630e06d4863bf338a375838ae0d"],
    "filters" : [
        {
      "fieldId": "9343f8800b9723457d7de946c8bf85a77532ab9e0d",
      "operator": "Equals",
      "value": "Unix"
    }
    ],
    }
    response = self.session.request(method='post',url=uri,json=request_body,headers=self.headers)
    return response.json()


if __name__ == '__main__':
  C = Cherwell('')
  C.authenticate()
  s = C.getCmdb()['businessObjects']
  os.system('touch CMDB_all.txt')
  with open('CMDB_all.txt','wb') as f:
    for i in range(len(s)):
      server_name = str(s[i]['fields'][0]['value'])
      server_status = str(s[i]['fields'][1]['value'])
      server_OS = str(s[i]['fields'][2]['value'])
#      server_MW = str(s[i]['fields'][3]['value'])
#      server_App = str(s[i]['fields'][4]['value'])
      data = ','.join([server_name,server_status,server_OS])
      f.write(data + '\n')

