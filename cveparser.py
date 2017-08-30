#!/usr/bin/env python2.7

import sys
import csv
import time
import shodan
import pickle
import os.path
import pycurl
import json

from blessings import Terminal

t = Terminal()
c = pycurl.Curl()

edb = False
logging = False

# Print logo
print t.cyan("""
oo.ooooo.  oooo    ooo oo.ooooo.   .oooo.   oooo d8b  .oooo.o  .ooooo.   oooo d8b 
 888' `88b  `88.  .8'   888' `88b `P  )88b  `888""8P d88(  "8 d88' `88b `888""8P 
 888   888   `88..8'    888   888  .oP"888   888     `"Y88b.  888ooo888  888 
 888   888    `888'     888   888 d8(  888   888     o.  )88b 888    .o  888 
 888bod8P'     .8'      888bod8P' `Y888""8o d888b    8""888P' `Y8bod8P' d888b 
 888       .o..P'       888                                             
o888o      `Y8P'       o888o            				
					Common Vulnerabilities and Exploits
 										""")

# We'll just go ahead and steal ExploitDB's hard work for this part (<3)
def s_sploit():
	
	print "\n[" + t.green("+") + "]Please provide a search query. Multiple terms are allowed in this module."
	query = raw_input("\n<" + t.cyan("SEARCHSPLOIT") + ">$ " )
	
	try:
		result = os.system("searchsploit -j " + query)
	except Exception as e:
		print "\n[" + t.red("!") + "]Critical. An error was raised while attempting to retrieve data."
		print e		
	
	if logging == True:
		with open('searchsploit.log', 'ab') as outfile:
			outfile.write(result)
			outfile.close()

# Function to install and configure ExploitDB's Searchsploit utility
def exploit_DB():
	global edb
	
	print "\n[" + t.green("+") + "]To get additional comprehensive search results, installing ExploitDB's" 
	print "[" + t.green("+") + "]'Searchsploit' utility is recommended. Functionality from which will be"
	print "[" + t.green("+") + "]integrated into PyParser-CVE."	
	
	print "\n[" + t.magenta("?") + "]Would you like PyParser to install this utility?"
	get_edb = raw_input("[Y]es/[N]o: ")
		
	if get_edb == 'y':
		print "\n[" + t.green("+") + "]Invoking git...\n"
		time.sleep(1)
		try:
			os.system("git clone https://github.com/offensive-security/exploit-database.git")
			os.system("cd exploit-database && abspath=$(pwd) && sudo ln -sf $abspath/searchsploit /usr/local/bin/searchsploit")
			os.system("chmod +x searchsploit")
		
		except Exception as e:
			print "\n[" + t.red("!") + "]Critical. An error was raised with the following message."
			print e
		
			sys.exit(0)
		
		print "\n[" + t.green("+") + "]Completed"
		edb = True
	
	elif get_edb == 'n':
		print "\n[" + t.green("+") + "]Not installing."
		edb = False
	else:
		print "\n[" + t.red("!") + "]Unhandled option"

# Shodan CVE look up
def shodan_q():
	global logging
	
	print "\n[" + t.green("+") + "]Please provide a search query. I.e 'cisco' will return all known vulns for that item" 
	
	query = raw_input("\n<" + t.cyan("SHODAN") + ">$ " )
	
	try:
		api = shodan.Shodan(SHODAN_API_KEY)
		results = api.exploits.search(query, 5, 'author, platform, port, type')
	except Exception as e:
		print "\n[" + t.red("!") + "]Critical. An error was raised with the following error message"
		print e
	
	format = json.dumps(results, indent = 2)	
	print format
	
	if logging == True:
		with open('shodan_cve.log', 'ab') as outfile:
			outfile.write(format)
			outfile.close()
			
		print "\n[" + t.green("+") + "]Results have been saved to 'shodan_cve.log' in the current directory."


def cve_mitre():
	global logging
	
	if not os.path.isfile('cve_mitre.csv'):
		print "\n[" + t.green("+") + "]Fetching CVE Mitre data. This may take a while..."
		try:
			c.setopt(c.URL, "http://cve.mitre.org/data/downloads/allitems.csv")
			with open('cve_mitre.csv', 'wb') as outfile:
				c.setopt(c.WRITEFUNCTION, outfile.write)
				c.perform()
				c.close()
		except Exception as e:
			print "\n[" + t.red("!") + "]Critical. An error was raised while attempting to retrieve data"
			print e
		
		
		print "\n[" + t.green("+") + "]Complete"
		
	print "\n[" + t.green("+") + "]Please provide a search query."
	query = raw_input("\n<" + t.cyan("MITRE") + ">$ " )
	
	with open('cve_mitre.csv', 'rb') as infile:
		csv_reader = csv.DictReader(infile)
		rows = [row for row in csv_reader]
		for row in rows:
			for col_name in row:
				if query in row[col_name]:
					result = json.dumps(row)
					print result
					
				
				if logging == True:
					with open('cve_mitre.log', 'ab') as outfile:
						outfile.write(result)
						outfile.close

def main():
	try:
		while True:
			print "\n[" + t.green("+") + "]Welcome to PyParser-CVE. Please select an action"
			print """

1. Query Shodan				4. Logging	
2. Query CVE Mitre			5. Quit
3. Invoke Searchsploit					"""
		
			action = raw_input("\n<" + t.cyan("PYPARSER") + ">$ ")
		
			if action == '1':
				shodan_q()
			elif action == '2':
				cve_mitre()
			elif action == '3':
			
				if edb == False:
					print "\n[" + t.red("!") + "]Warning! Searchsploit was not installed."
					print "[" + t.green("?") + "]Would you like PyParser to automatically resolve this issue?\n"

					get_edb = raw_input("[Y]es/[N]o: ")
					if get_edb == 'y':
						exploit_DB()
					elif get_edb == 'n':
						print "\n[" + t.green("+") + "]Not resolving."
					else:
						print "\n[" + t.red("!") + "]Unhandled option"
				else:
					s_sploit()
				
			elif action == '4':
				print "\n[" + t.magenta("?") + "]Enable logging?"
				query = raw_input("[Y]es/[N]o: ")
			
				if query == 'y':
					logging = True
				elif query == 'n':
					logging = False
				else:
					print "\n[" + t.red("!") + "]Unhandled option"
				
			elif action == '5':
				break
			else:
				print "\n[" + t.red("!") + "]Unhandled option"
			
	except KeyboardInterrupt:
		print "\n[" + t.red("!") + "]Critical. User aborted."

if __name__ == '__main__':
	# Check to see if we have Shodan API key saved
	if not os.path.isfile('api.p'):
		print "\n[" + t.green("+") + "]Welcome to PyParser-CVE. Please provide your Shodan API Key"

		SHODAN_API_KEY = raw_input("API key: ")
		pickle.dump(SHODAN_API_KEY, open( "api.p", "wb" ))
		
		print "\n[" + t.green("+") + "]Your API key has been saved to 'Shodan_API.p' in the current directory.\n"
	
		# Once we have the API key properly stored/loaded check for ExploitDB directory
		# if we can't find it we will assume Searchsploit has not been installed and prompt to resolve
		if not os.path.isdir('exploit-database'):
			exploit_DB()
	else:
		SHODAN_API_KEY = pickle.load(open( "api.p", "rb" ))
		path = os.path.abspath("api.p")

		print "\n[" + t.green("+") + "]Your Shodan API key was sucesfully loaded from " + path
		if not os.path.isdir('exploit-database'):
			exploit_DB()
	
	main()
