#--------------------------------------------------------
# Ticket Template Tool
# Created by Gregory Savage for Russell Industries Corp.
# Contact:
#    Email: gregory.savage@russellindustries.com
#--------------------------------------------------------   

# Ticket creation functions
# Requests is a third-party library
#   Use 'pip install requests' to install it
import requests
import json
from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)

# Loads config file and extracts API Key and Freshdesk Domain
config = open('config.json')
conf = json.load(config)
api_key = str(conf['apiKey'])
domain = str(conf['domain'])
password = "x"

# Takes ticket data from external function. Looping variable is optional, used in case of ticket batches
def make_ticket(ticket, noConfirm = False):
    
    headers = { 'Content-Type' : 'application/json' }

    r = requests.post("https://"+ domain +".freshdesk.com/api/v2/tickets", auth = (api_key, password), headers = headers, data = json.dumps(ticket))
    # Omits ticket data returns in the instance of batches
    if (noConfirm == True):
        if r.status_code == 201:
            print("Ticket created successfully")
        else:
            print("Failed to create ticket at Freshdesk, errors are displayed below,")
            response = json.loads(r.content)
            print(response["errors"])
            print("x-request-id : " + r.headers['x-request-id'])
            print("Status Code : " + str(r.status_code))
    # In cases of singular ticket creation, returns newly created ticket data in PrettyPrinted JSON format
    # If an error is generated here, the ticket was either formed incorrectly or Freshdesk encountered an error
    else:
        if r.status_code == 201:
          print("Ticket created successfully, the response is given below.")
          pp.pprint(r.json())
          print("Location Header : " + r.headers['Location'])
        else:
          print("Failed to create ticket, errors are displayed below,")
          response = json.loads(r.content)
          print(response["errors"])

          print("x-request-id : " + r.headers['x-request-id'])
          print("Status Code : " + str(r.status_code))
      
# Allows for viewing of ticket provided ticket number is known
def view_ticket(tnum):
    headers = { 'Content-Type' : 'application/json' }
    r = requests.get("https://"+ domain +".freshdesk.com/api/v2/tickets/"+ str(tnum), auth = (api_key, password), headers = headers)
    print(r.status_code)
    if r.status_code == 200:
      print("Ticket information:")
      pp.pprint(r.json())
    else:
      print("Failed to load ticket, errors are displayed below,")
      response = json.loads(r.content)
      print(response["errors"])

      print("x-request-id : " + r.headers['x-request-id'])
      print("Status Code : " + str(r.status_code))

# Produces list of active agents. Requires elevated permissions.
def view_agents():
    headers = { 'Content-Type' : 'application/json' }
    r = requests.get("https://"+ domain +".freshdesk.com/api/v2/agents", auth = (api_key, password), headers = headers)
    if r.status_code == 200:
        print("Agent List")
        response = json.loads(r.content)
        for i in range(1, len(response)):
            print("{:2}. Name: {}".format(i,response[i]["contact"]["name"]))
            print("    Title: {}".format(response[i]["contact"]["job_title"]))
            print("    Email: {}".format(response[i]["contact"]["email"]))
            print("    ID: {}".format(response[i]["id"]))
            print()
    else:
      print("Failed to load agents, errors are displayed below,")
      response = json.loads(r.content)
      print(response["errors"])

      print("x-request-id : " + r.headers['x-request-id'])
      print("Status Code : " + str(r.status_code))