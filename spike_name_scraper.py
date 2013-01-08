import mechanize
import re
from bs4 import BeautifulSoup

#Scrape the names of a class year from a spike page
def scrape_names():
	mech = mechanize.Browser()
	mech.set_handle_robots(False)
	mech.set_handle_refresh(False)
	mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	#Find and insert the id of the class year you want to scrape at the end of the url
	spike_page = mech.open('https://spike.wharton.upenn.edu/Community/groups/?id=63654')
	mech.select_form(nr=1)
	
	#Insert provided login information
	mech.form['username'] = ''
	mech.form['password'] = ''
	mech.submit()

	#Make a soup object from the group page
	ugr_group_page = mech.response().read()
	soup = BeautifulSoup(ugr_group_page)


	links = soup.find_all('a')
	for raw_link in links:
		possible_link = str(raw_link['href'])
		if possible_link.startswith("../member/?"):
			raw_name = str(raw_link.contents[0])
			split_name = raw_name.split()
			if len(split_name) == 2:
				entry = "%s, %s" % (split_name[1], split_name[0])
				entry += '\n'

				#Insert path to where script is located
				out = open('/name_output.txt', 'a')
				out.write(entry)
				out.close()

if __name__=='__main__':
	scrape_names()
