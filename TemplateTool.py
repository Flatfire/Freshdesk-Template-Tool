#--------------------------------------------------------
# Ticket Template Tool
# Created by Gregory Savage for Russell Industries Corp.
# Contact:
#    Email: gregory.savage@russellindustries.com
#--------------------------------------------------------   

from ticket_func import view_ticket, view_agents
from template_func import set_template, create_template
import json
import sys, getopt


# Opens templates file, loads json data and closes file. Templates file should be placed at root.
t = open('templates.json')
tJ = json.load(t)
t.close()
tArr = tJ['templates']


def main(template = "", region = "", agentid = ""):
    
    # Skips menu interactions if template is forced
    if (len(template) > 0):
        print("Forcing {} ticket creation".format(template))
        i = 0
        while (i < len(tArr) and tArr[i]['quickref'] != template):
            i+=1
        if (i < len(tArr)):
            tempSel = tArr[i]
            # If region parameter is blank, create for all regions
            if (len(region)>0):
                region = region.upper()
                try:
                    create_template(tempSel, region, agentid, noConfirm = True)
                except error as e:
                    print("Invalid region passed as argument. Terminating.")
                    print(e)
            else:
                regions = tempSel['regions']
                for r in range(len(regions)):
                    create_template(tempSel, regions[r], agentid, noConfirm = True)
    
    # If no options are specified, menu is launched                
    else:      
        menu()

def menu():
    # Menu selections. May relocate to JSON file.
    # To add new features, simply add the function to the list, along with a description in the same format as existing menu options
    menu_options = [[set_template, "Recurring ticket templates"], [view, "View an existing ticket"],[view_agents,"View list of available agents"]]
    # Will return to main menu after task unless told to quit
    while True:
        print("Available functions: ")
        for i in range(len(menu_options)):
            print("{}. {}".format(i+1, menu_options[i][1]))
        print()
        try:
            sel = input("Enter your selection ('x' to quit):  ")
            if (sel == 'x'):
                break
            sel = int(sel)
            menu_options[sel-1][0]()
        except Exception as e:
            print("Error occurred during operation, error is presented below:")
            print(e)    
            
# View ticket prompt. Allows user to view ticket based on ticket number.
def view():
    tnum = input("Enter a ticket number: ")
    view_ticket(tnum)

# Executes main function. Scans for commmand line arguments before launch.   
if __name__ == "__main__":
    template, region, agentid = "","",""
    # Omit filename as argument
    argArr = sys.argv[1:]
    # Parse arguments and values
    opts, args = getopt.getopt(argArr, "t:r:a:", ["template =", "region =", "agentid ="])
    for opt, arg in opts: 
        if opt in ['-t', '--template']: 
            template = arg 
        elif opt in ['-r', '--region']: 
            region = arg 
        elif opt in ['-a', '--agent']:
            agentid = arg
    main(template, region, agentid)