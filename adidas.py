import time
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from keyboard import press

# Globals for testing
target_shoe = 'https://www.adidas.com/us/cloudfoam-pure-shoes/EG3820.html'

delay = 7
size = '6.5'

login = {
	"user": 'ncarchio@gmail.com',
	"pass":'Gracie0418'
}

creditcard = {
	'name_on_card': 'joeshmo',
	'number': '02131231232', 
	'expr_date': '01/01/2023',
	'cvv': '123'
}

class Adidas_Bot:
	# instantiates bot
	def __init__(self, website):
	    # Using Firefox to access web
	    self.browser = webdriver.Firefox(executable_path=r'/Users/nicolascarchio/Desktop/python_projs/adidas/geckodriver')
	    self.browser.get(website)
	    self.browser.implicitly_wait(7)
	
	# searches for a given criteria
	def search(self, search_request, shoe_type): 
		# Find search bar and Send the search request
		home_search = self.browser.find_element_by_name('q')
		home_search.click()
		home_search.send_keys(search_request)
		home_search.send_keys(Keys.RETURN)

		# if there is a popup, close it
		try: 
			popup = self.browser.find_element_by_class_name("gl-modal__close")
			popup.click()
			print("found popup, exited out of it")
		except: 
			print("did not find popup, continued to website")

		# loop through and find the correct shoe
		selected_shoes = self.browser.find_elements_by_xpath("//a[@class='gl-product-card__media-link']")
		while (len(selected_shoes) <= 0): 
			selected_shoes = self.browser.find_elements_by_xpath("//a[@class='gl-product-card__media-link']")
		print('size of selected shoes: ' + str(len(selected_shoes)))
		for i in selected_shoes:
			title = i.find_element_by_xpath("//img[@title='" + shoe_type + "']")
			if title is not None:
				print(i.get_attribute('title'))
				action = ActionChains(self.browser)
				action.move_to_element(title)
				action.click()
				action.perform()
				print('\n' + '\n' + 'found it!' + '\n' + '\n')
				break
	
	# add the selected shoe to the cart
	def search_and_add_to_cart(self, search_request, shoe_type): 
		# first search for the item we want to add to the cart
		self.search(search_request, shoe_type)
		
		# now after the search successfully completes, get the size of the shoe
		#size = input("what size shoe would you like?" + '\n' + '\t')

		# then, get list of shoe sizes and find the selected shoe size
		shoe_container = self.browser.find_element_by_xpath("//div[@class='sizes___2IneS']")
		print(shoe_container.get_attribute('class'))
		shoe_size = shoe_container.find_element_by_xpath("//button[.='" + size + "']")
		print(shoe_size)
		shoe_size.click()
		print ('selected the size!')

		# now, add to the bag
		add_to_bag = self.browser.find_element_by_xpath("//button[@class='gl-cta gl-cta--primary gl-cta--full-width']")
		add_to_bag.click()

	# checkout the cart
	def checkout(self): 
		print('in checkout')
		# first, exit the popup if one exists
		try: 
			popup = self.browser.find_element_by_class_name("gl-modal__close")
			popup.click()
			print("found 2nd popup, exited out of it")
		except: 
			print("did not find popup, continued to website")

		# bring us onto the cart page and click checkout
		checkout_icon = self.browser.find_element_by_xpath("//a[@title='Checkout']")
		checkout_icon.click() 
		checkout_button = self.browser.find_element_by_xpath("//button[@data-auto-id='glass-checkout-button-bottom']")
		checkout_button.click()

		# log into account -> username
		login_user = self.browser.find_element_by_id('login-email')
		login_user.click()
		login_user.send_keys(login.get("user"))
		login_user.send_keys(Keys.RETURN)
		# password
		login_pass = self.browser.find_element_by_id('login-password')
		login_pass.click()
		login_pass.send_keys(login.get("pass"))
		login_pass.send_keys(Keys.RETURN)


		# review and play
		try: 
			rev_and_pay = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.XPATH, "//button[@data-auto-id='review-and-pay-button']")))
			rev_and_pay.click()
			# action = ActionChains(self.browser)
			# action.move_to_element(rev_and_pay)
			# action.click()
			# action.perform()
			print("rev_and_pay button worked")
		except TimeoutException: 
			print("page took tooooo long to load")
			return

		# review and pay				
		# rev_and_pay = self.browser.find_element_by_xpath("//button[@data-auto-id='review-and-pay-button']")
		# rev_and_pay.click()

		#<button type="button" class="gl-cta gl-cta--primary" data-auto-id="review-and-pay-button" aria-label="Review and Pay"><span class="gl-cta__content">Review and Pay</span><svg class="gl-icon gl-cta__icon"><use xlink:href="#arrow-right-long"></use></svg></button>

		# handle bank info
		# card number
		card_number = self.browser.find_element_by_name('card.number')
		card_number.click()
		card_number.send_keys(creditcard.get('number'))

		# name on card 
		card_name = self.browser.find_element_by_name('card.holder')
		card_name.click()
		card_name.send_keys(creditcard.get('name_on_card'))

		# expiry date		
		card_exp_date = self.browser.find_element_by_xpath("//input[@data-auto-id='expiry-date-field']")
		card_exp_date.click()
		card_exp_date.send_keys(creditcard.get('expr_date'))

		# cvv		
		card_cvv = self.browser.find_element_by_name('card.cvv')
		card_cvv.click()
		card_cvv.send_keys(creditcard.get('cvv'))

		# **** haven't implemented a BUY feature yet, becasue I do not want to spend money yet
			#<button type="submit" class="gl-cta gl-cta--primary gl-cta--full-width order-button___oa2MV gl-vspace-bpall-medium" data-auto-id="place-order-button"><span class="gl-cta__content">Place Order</span><svg class="gl-icon gl-cta__icon"><use xlink:href="#arrow-right-long"></use></svg></button>


	# if the user's credentials are not valid, create an account for them
	def create_account(): 
		pass

	# main to test the bot
	def main(): 
		bot = Adidas_Bot('https://www.adidas.com/us')
		bot.search_and_add_to_cart("women's running shoes", "Cloudfoam Pure Shoes")
		bot.checkout()

		# quit the browzer
		time.sleep(10)
		#bot.browser.quit()


if __name__=="__main__": 
    Adidas_Bot.main() 

