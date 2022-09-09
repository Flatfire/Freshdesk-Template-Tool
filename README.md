## Ticket Template Tool V1

This an easily configurable tool for creating FreshDesk tickets for designated regions
based on predefined templates. It uses the FreshDesk API to provide Agents with an easy
way to create tickets based on user definable templates either through a brief menu
system or by command line arguments. It is also capable of viewing raw JSON ticket data
when provided a ticket number.

The only required external python library is 'requests'. It can be installed with
	
	pip install requests

from the command line.

For information about the Freshdesk API go to https://developers.freshdesk.com/api/

## Getting Started:
	
	Configuration:
		
		The primary configuration is done from the 'config.json' at the root of the folder.
		This file stores the API key, agent ID for the agent tickets are to be assigned
		to and the freshdesk support domain.
		
		The API key can be found from your user profile page within Freshdesk. Each Agent
		has a unique API key. Permissions may vary depending on the API key used, as
		tickets will be created by the Agent it's associated with.
		
		The agent ID can be found in the user profile URL: 
		https://yourdomain.freshdesk.com/a/profiles/[agentID]/
		This ID is used to assign an agent to tickets. If you do not wish to assign an agent
		to a ticket, leave this blank.
		
		The domain is used to determine the correct support desk for which the tickets are
		meant to be created for. This value is the FreshDesk subdomain used by your support
		desk: http://domain.freshdesk.com/
		
	Templates:
		
		Templates are loaded from the 'templates.json' file at the root of the execution
		folder. Templates are selected either from the command line menu or through arguments
		on program start.
		
		Templates consist of 4 primary components: A quick reference name, a subject title,
		applicable region/company and a ticket description. The region/company determines 
		the contact that will be attributed to the ticket. Additional templates can be added
		following this format in the 'templates.json' file.
		
		Regional/Company contacts are contained in the contacts field, each email contact is
		represented by their corresponding region. This is of the format "Company" : "Email"
		
## Creating Tickets:

	By Argument:
		
		Tickets can be created without user intervention by means of command line arguments.
		Tickets created this way will have confirmation prompts suppressed. 
		
		Argument values with spaces should be enclosed in quotes.
		
		The arguments are as follows:
			
			TemplateTool [-t|--ticket] [quickref] [-r|--region] [region] [-a] [agentid]
			
			-t or --ticket	|    Used to choose a template at start. If no template is chosen,
					     Or the selected template is not found the program menu will
					     be launched instead. 
							
					     Example: TemplateTool -t maintenance
			
			-r or --region	|    Used to designate a region for the ticket. If a template is
					     not specified the parameter will be ignored. The region 
					     passed must be a valid region for the selected template.
								
					     Example: TemplateTool -t maintenance -r testregion
			
			-a or --agentid |    Used to designate the associated agent for ticket assignment.
					     If none specified, ticket will default to agentID in config
					     file. AgentIDs can be acquired from Freshdesk user profiles.
						
					     Example: TemplateTool -t maintenance -a 45832418663
		
	By Menu:
		
		Tickets can also be created through a template selection menu that is launched if no
		arguments are passed at start, or if a template is specified incorrectly. If the
		ticket number is known, tickets can also be viewed from this menu. 
		
		The menu allows users to select a template, the intended region, or all applicable 
		regions for that template. For individual tickets, the completed ticket data will be 
		returned. For batches, this step is skipped and a creation confirmation is returned
		in its place.

		In cases where Agent IDs are unknown or you would like to look up the list of available
		agents for assignment, the tool also allows you to list available agents along with their
		email and ID number quickly, without visiting their profile. To use this feature, the
		API key in the 'config.json' file must have elevated privileges in Freshdesk.
		
		The menu also provides action confirmation to ensure data presents correctly before
		creating the ticket.
		
		
		
		
		
