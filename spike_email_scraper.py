import mechanize
import re
from bs4 import BeautifulSoup

#This method scrapes the emails from the web page
def scrape_raw_emails():
	mech = mechanize.Browser()
	mech.set_handle_robots(False)
	mech.set_handle_refresh(False)
	mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	#Find and insert the id of the class year you want to scrape at the end of the url
	spike_page = mech.open('https://spike.wharton.upenn.edu/Community/groups/?id=') 
	mech.select_form(nr=1)

	#Insert provided login information 
	mech.form['username'] = ''
	mech.form['password'] = ''
	mech.submit()

	ugr_group_page = mech.response().read()
	soup = BeautifulSoup(ugr_group_page)

	email_links = soup.find_all('a', href=True)
	for link in email_links:
		entry = str(link['href'])
		entry += '\n'

		#Insert the path to where this script is located
		out = open('/output.txt', 'a') #Path goes here
		out.write(entry)
		out.close()

	
#This method cleans up the scraped links so that they are usable
def clean_emails():
	raw_emails = open('/Users/nitiniyer/Py_Projects/ugr15_scrape/email_output.txt', 'r')
	for email in raw_emails:
		email_str = str(email)
		if email_str.startswith("mailto"):
			clean_email = email_str.replace("mailto:", "")
			clean_email += '\n'
			out = open('/clean_output.txt', 'a') #Insert path to script here
			out.write(clean_email)
			out.close()


if __name__=='__main__':
	get_to_page()
	clean_emails()


