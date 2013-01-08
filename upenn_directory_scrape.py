import mechanize
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re

#This scraper uses Penn Directory to scrape the public addresses of individuals by their email addresses
def scrape_addresses():

	#Go to the Directory page and login with info
	driver = webdriver.Firefox()
	driver.get('https://medley.isc-seo.upenn.edu/directory/jsp/fast.do?fastStart=pennView')
	login = driver.find_element_by_name('login')
	password = driver.find_element_by_name('password')
	login.send_keys('')
	password.send_keys('')
	driver.find_element_by_name('loginform').submit()

	#Open the list of emails to use
	email_list = open('/Users/nitiniyer/Py_Projects/ugr16_work/clean_output_edited.txt', 'r')

	while 1:

		#Enter a given email from file and submit the form
		email = email_list.readline()
		if not email: break
		str_email = email.replace('\n', '')
		email_value = driver.find_element_by_xpath('//tr[5]/td[2]/input')
		email_value.send_keys(str_email)
		driver.find_element_by_xpath('//span').submit()
		out = open('/Users/nitiniyer/Py_Projects/ugr16_work/name_address_output.txt', 'a')


		#This code is only used after the below code is run with this commented out and some edits. This is done because in its
		#current state, the directory to be scraped from is imperfect so an initial run through must be done to find bad email.
		if str_email in no_address_list:
			WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//a[@class='linkTextBoldNoUnderline']/span"))
			raw_name = driver.find_element_by_xpath("//a[@class='linkTextBoldNoUnderline']/span")
			name =  str(raw_name.text)
			name += ', '+str_email+', \n'
			out.write(name)
			out.close()
			driver.find_element_by_xpath("//a[@class='submitButton']/span").click()
			driver.find_element_by_xpath('//tr[5]/td[2]/input').clear()



		#This code navigates to where the address is located and then saves address to an output file along with the person's name
		if str_email not in no_address_list:
			WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//a[@class='linkTextBold']/span"))
			raw_name = driver.find_element_by_xpath("//a[@class='linkTextBold']/span")
			name =  str(raw_name.text)
			name += ', '+str_email+', '
			out.write(name)
			driver.find_element_by_xpath("//a[@class='linkTextBold']/span").click()
			for handle in driver.window_handles:
				driver.switch_to_window(handle)
			WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath('//html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[10]/td[3]'))
			results = driver.find_element_by_xpath('//html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[10]/td[3]')
			address = str(results.text)
			if address.startswith('PHILADELPHIA'):
				results = driver.find_element_by_xpath('//html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[8]/td[3]')
				address = str(results.text)
			address += '\n'
			out = open('/name_address_output.txt', 'a') #Insert path to script here
			out.write(address)
			out.close()
			driver.find_element_by_xpath("//a[@class='submitButton']/span").click()
			for handle in driver.window_handles:
				driver.switch_to_window(handle)
			driver.find_element_by_xpath("//a[@class='submitButton']/span").click()
			driver.find_element_by_xpath('//tr[5]/td[2]/input').clear()

#This method takes two lists and filters one down to contain only the information of individuals that are on the rush_list
def filter_names():

	#Get the file ready to be filtered
	rush_list = open('', 'r') #Insert path to csv file here
	rush_csv = csv.reader(rush_list)

	for rush in rush_csv:
		rush_name = (str(rush[0]) + str(rush[1])).lower()
		address_list = open('', 'r') #Insert path to csv file here
		address_csv = csv.reader(address_list)
		count = 0
		for address in address_csv:
			first_raw = address[1].split()
			first = str(first_raw[0])
			address_check = (str(address[0]) + ' ' + first).lower()
			if rush_name == address_check:
				count += 1
				arr = [str(address[0]).lower(), first.lower(), str(address[2]), str(address[3])]
				building = arr[3].split(' ', 4)[-1]
				out = open('rush_addresses.txt', 'a') #Insert path to script here
				entry = "%s %s,%s,%s, %s" % (arr[1], arr[0], arr[2], arr[3], building)
				entry += '\n'
				out.write(entry)
				out.close()
		#This is included for those names that are three words or longer, more functionality will be added to handle this
		if (count == 0):
			out = open('rush_addresses.txt', 'a') #Insert path to script here
			entry_raw = rush_name.split()
			entry = entry_raw[1] + ' ' + entry_raw[0] + '\n'
			out.write(entry)
			out.close()


if __name__=='__main__':
	scrape_addresses()