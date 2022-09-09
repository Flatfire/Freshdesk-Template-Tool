#--------------------------------------------------------
# Ticket Template Tool
# Created by Gregory Savage for Russell Industries Corp.
# Contact:
#    Email: gregory.savage@russellindustries.com
#--------------------------------------------------------   

## This script requires "requests": http://docs.python-requests.org/
## To install: pip install requests

from ticket_func import make_ticket
import json

# Opens config for AgentID number and domain data
config = open('config.json')
conf = json.load(config)
config.close()
cAgentID = None

# Checks for agentID
try:
    cAgentID = int(conf['agentID'])
except:
    pass

# Opens JSON that stores template data and contacts for each region then closes file
tTemplates = open('templates.json')
tempData = json.load(tTemplates)
tTemplates.close()

# Email Addresses From JSON
contacts = tempData['contacts']
# Template List
templateArray = tempData['templates']

# Template Selection Function
# Returns template from templates (tempSel)
def temp_select(templateArray):
    print("Templates: ")
    for i in range(len(templateArray)):
        print("{}. {}".format(i+1, templateArray[i]['title']))
    print()
    i = -1
    while (i == -1):
        try:
            # Input for template selection
            i = int(input("Enter a selection number:"))
            # Selects correct region name        
            tempSel = templateArray[i-1]
        except:
            print("Invalid template")
            i = -1
            
    return tempSel

# Selects Region from tempRegions (array of region strings)
# Returns region selection (string)
def region_select(tempRegions):
    regSel = ""
    n = 1
    print("Regions: ")
    for i in range(len(tempRegions)):
        print("{}. {}".format(i+1, tempRegions[i]))
        n+=1
    print("{}. All".format(n))
    print()
    while True:
        try:
            # Input for Region
            i = int(input("Enter a selection number:"))
            if (i == len(tempRegions)+1):
                regSel = "ALL"
            else:
                # Checks validity of region
                regSel = tempRegions[i-1]
            break
        except:
            print("Invalid region")
    
    return regSel

# Compiles template based on template and region selections
def set_template():
    noConfirm = False
    tempSel = temp_select(templateArray)
    regions = tempSel['regions']
    regSel = region_select(regions)
    if (regSel == "ALL"):
        confirm = input("Would you like to create {} tickets for all regions? (Y/N)".format(tempSel['title']))
        if (confirm.upper() == "Y" or confirm.upper() == "YES"):
            noConfirm = True
            for r in range(len(regions)-1):
                create_template(tempSel, regions[r], noConfirm)
        else:
            print("Cancelling ticket creation")
    else:
        create_template(tempSel, regSel)

# Private function for simplification of looping
def create_template(tempSel, regSel, agentID = "", noConfirm = False):
    # Checks for agentID override. If none, default to config.
    if (len(agentID)==0):
        agentID = cAgentID
    else:
        agentID = int(agentID)
        
    # Check for corresponding region contact
    try:
        regMail = contacts[regSel]
    except:
        print("Region contact does not exist. Aborting")
        
    tempDesc = tempSel['description']
    title = tempSel['title']
    # Request confirmation to avoid ticket spam
    # For the love of god please move the regions, templates and contacts into a json file so you can stop making weird hacks like this
    if (noConfirm == False):
        confirm = input("Would you like to create a {} ticket for {} region with contact {}? (Y/N)".format(title ,regSel, regMail))
    else:
        confirm = "Y"
        
    if (confirm.upper() == "Y" or confirm.upper() == "YES"):
        print("Creating {} ticket for {} region with contact {}".format(title ,regSel, regMail))
        # Ticket creation template. Refer to Freshdesk API for additional fields that can be added or modified
        ticket = {
            'subject' : '{} - {}'.format(regSel, title),
            'description' : '{}'.format(tempDesc),
            'email' : '{}'.format(regMail),
            'priority' : 1,
            'status' : 2,
            'source' : 2,
            'responder_id' : agentID
        }
        make_ticket(ticket, noConfirm)
    else:
        print("Cancelling ticket creation")
