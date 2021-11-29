# Cherwell_Integration
Module used to interact with Cherwell SMT ( Service Managament Tool ) 

For the module to work follow below steps:

1) In the authenticate method, update username, password and API key.\
    user_name  = "username"
    password   = "password"
    api_key    = "apikey"

   
2) In the getCustomerInternalRecordId method, Update the value of Full name of the User ID that was used to create the ID(You can get it from your cherwell admin.

      search_criteria = {
      "fieldId":  "93382178280a07634f62d74fc4bc587e3b3f479776",  #FullName's field ID
      "operator": "eq",
      "value":    "" #Full name of the user ID
    }
    

3) execute the module as follows.

(venu) (base) [root@server Cherwell_Integration]# python Create_cherwell_Ticket.py
Enter cherwell FQDN : cherwell.example.com
####################################
Welcome to Cherwell UNIX Integration
####################################
Enter the Summary : Testing
Enter a Brief Description : Testing
Enter "Request" or "Incident" : Incident
Enter the Priority of the Incident : 5
Enter the team name : Unix
2029597 has been raised!!!
(venu) (base) [root@server Cherwell_Integration]#

Incident 2029597 has been raised in the above case to Unix team with priority 5.


    
