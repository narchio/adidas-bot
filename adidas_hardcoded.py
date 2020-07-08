import time
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from keyboard import press

# Globals for testing
target_shoe = 'https://www.adidas.com/us/cloudfoam-pure-shoes/EG3820.html'

class Adidas_Bot:
	# instantiates bot
	def __init__(self, website):
	    # Using Firefox to access web
	    self.browser = webdriver.Firefox(executable_path=r'/Users/nicolascarchio/Desktop/python_projs/adidas/geckodriver')
	    self.browser.get(website)
	
	# searches for a given criteria
	def search(self, body): 
		# Find search bar and Send the search request
		home_search = self.browser.find_element_by_name('q')
		home_search.click()
		home_search.send_keys(body)
		home_search.send_keys(Keys.RETURN)
		time.sleep(1)

		# if there is a popup, close it
		try: 
			popup = self.browser.find_element_by_class_name("gl-modal__close")
			popup.click()
			print("found popup, exited out of it")
			time.sleep(1)
		except: 
			print("did not find popup, continued to website")

		# loop through and find the correct shoe
		selected_shoes = self.browser.find_elements_by_xpath("//a[@class='gl-product-card__media-link']")
		for i in selected_shoes:
			if i.get_attribute('href') == target_shoe: 
				action = ActionChains(self.browser)
				action.move_to_element(i)
				action.click()
				action.perform()
				print('\n' + '\n' + 'found it!' + '\n' + '\n')
				break
		time.sleep(5)
	
	# add the selected shoe to the cart
	def add_to_cart(self, size): 
		# get list of shoe sizes and find the selected shoe size
		shoe_container = self.browser.find_element_by_xpath("//div[@class='sizes___2IneS']")
		print(shoe_container.get_attribute('class'))
		shoe_size = shoe_container.find_element_by_xpath("//button[.='" + size + "']")
		print(shoe_size)
		shoe_size.click()
		print ('selected the size!')
		time.sleep(3)

		# now, add to the bag
		add_to_bag = self.browser.find_element_by_xpath("//button[@class='gl-cta gl-cta--primary gl-cta--full-width']")
		add_to_bag.click()

	# checkout the cart
	def checkout(self): 
		pass

	# main to test the bot
	def main(): 
		bot = Adidas_Bot('https://www.adidas.com/us')
		#bot = Adidas_Bot('https://www.adidas.com/us/cloudfoam-pure-shoes/EG3820.html')
		bot.search("women's running shoes")
		bot.add_to_cart(input("what size shoe would you like?" + '\n' + '\t'))
		#bot.add_to_cart('size')
		# quit the browzer
		time.sleep(10)
		bot.browser.quit()


if __name__=="__main__": 
    Adidas_Bot.main() 

