# Cherwell_Integration
Module used to interact with Cherwell SMT ( Service Managament Tool ) 

For the module to work follow below steps:

1) In the authenticate method, update username, password and API key.\
    user_name  = username
    password   = password
    api_key    = apikey

   
2) In the getCustomerInternalRecordId method, Update the value of Full name of the User ID that was used to create the ID.

      search_criteria = {
      "fieldId":  "93382178280a07634f62d74fc4bc587e3b3f479776",  #Full name field ID
      "operator": "eq",
      "value":    "" #Full name of the user ID
    }
    



    
