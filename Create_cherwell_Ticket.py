########################

#Author : Venugopal P
#Python version : 3.6.8
#Requirements : requests,json,os.
#Purpose : To create Incidents/Requests in cherwell tool.

########################

import requests
import json
import os

class Cherwell:

  def __init__(self, url):
    self.server    = url
    self.api_url   = "https://{}/CherwellAPI" . format(self.server)
    self.headers   = {"Content-Type": "application/json"}
    self.token     = ""
    self.auth_mode = "Internal"
    self.boid = "6dd53665c0c24cab86870a21cf6434ae"
    self.session = requests.session()
    self.teamName = "your team name goes here"
    self.teamId = "944d7ef175ef37d9be87284182808fa24ca78f5312"
  ## End __init__

  def authenticate(self):
    '''
    Authentication part
    '''
    user_name  = username
    password   = password
    api_key    = apikey
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
  

  def Get_BusinessObjectSummary(self):
    uri = "https://{}/CherwellAPI/api/V1/getbusinessobjectsummary/busobid/{}".format(self.server,self.boid)
    response = self.session.request(method='get',url=uri,headers=self.headers)
    return response
  
  def GetBusinessObjectTemplate(self):
    uri = "https://{}/CherwellAPI/api/V1/getbusinessobjecttemplate".format(self.server)
    data = {"busObId": self.boid,
            "includeAll" : "true"
           }
    response = self.session.request(method = "post",url=uri, json= data,headers=self.headers)
    return response.json() 
  

  def getUser(self):
    technicianloginid   = userid / username
    technicianlogintype = "Internal"

    uri = "https://{}/CherwellAPI/api/v3/getuserbyloginid?loginid={}&loginidtype={}" . format(self.server, technicianloginid, technicianlogintype)
    response = self.session.request(method = "get",url=uri, headers=self.headers)
    print(response.json()["shortDisplayName"])
    return response.json()
 
  def setFieldValue(self,Template,FieldName,Value):
    
    fields = Template["fields"]
    field = {}

    for f in fields:
      if f["name"] == FieldName:
        field = f


    field["value"] = Value
    field["dirty"] = True

    return field

  def getCustomerInternalSchema(self):
    uri = "https://{}/CherwellAPI/api/V1/getbusinessobjectschema/busobid/{}" . format(self.server, self.boid)
    response = self.session.request(method = "get",url=uri, headers=self.headers)
    obj = response.json()

    return obj


  def getCustomerInternalRecordId(self):
    customer_internal_schema = self.getCustomerInternalSchema()

    search_field = {}
    field_definitions = customer_internal_schema["fieldDefinitions"]
    for fd in field_definitions:
      if fd["displayName"] == "FullName":
        search_field = fd

    search_criteria = {
      "fieldId":  "93382178280a07634f62d74fc4bc587e3b3f479776",  #Full name field ID
      "operator": "eq",
      "value":    "" #Full name of the user ID
    }

    request_body = {
      "busObId":          self.boid,
      #"includeAllFields": True,
      "filters":          search_criteria
    }

    uri = "https://{}/CherwellAPI/api/V1/getsearchresults" . format(self.server)
    response = self.session.request(method="post",url=uri, headers=self.headers, data=json.dumps(request_body))
    obj = response.json()
    obj_rec_id = obj["businessObjects"][0]["busObRecId"]
    return obj_rec_id
  

  def Create_incident(self,Summary,Description,Priority,Team,TicketType):
    uri = "https://{}/CherwellAPI/api/V1/savebusinessobject".format(self.server)
    incident_template = self.GetBusinessObjectTemplate()

    self.setFieldValue(incident_template, "CustomerRecID", self.getCustomerInternalRecordId())
    self.setFieldValue(incident_template, "CustomerDisplayName", "User, Internal")
    self.setFieldValue(incident_template, "IncidentType", TicketType)
    self.setFieldValue(incident_template, "Summary", Summary)
    self.setFieldValue(incident_template, "Description", Description)
    self.setFieldValue(incident_template, "Priority", Priority)
    self.setFieldValue(incident_template, "Service", "Information Technology")
    self.setFieldValue(incident_template, "Category", "Server")
    self.setFieldValue(incident_template, "Subcategory", "Submit a Request")
    self.setFieldValue(incident_template, "Source", "Event")
    self.setFieldValue(incident_template, "OwnedByTeam", Team)
 
    request_body = {
      "busObId": self.boid,
      "fields":  incident_template["fields"]
    }


    response = self.session.request(method='post',url=uri,json=request_body,headers=self.headers)
    return response

C = Cherwell('') #cherwell server name (FQDN goes here
C.authenticate()
print("####################################")
print("Welcome to Cherwell Integration")
print("####################################")
Summary = str(input('Enter the Summary : '))
Description = str(input('Enter a Brief Description : '))
TicketType = str(input('Enter "Request" or "Incident" : '))
Priority = int(input('Enter the Priority of the %s'%TicketType + ' : '))
Team = str(input('Enter the team name : '))
if TicketType in ["Request","Incident"] and 2 < Priority < 6 :
  resp = C.Create_incident(Summary,Description,Priority,Team,TicketType)
  print(resp.json()['busObPublicId'] + " has been raised!!!")
else:
  print('Either Priority or the TicketType is not correctly entered')
