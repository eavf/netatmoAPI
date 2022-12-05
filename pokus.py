from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")  # comment it or remove it to run with window

#driver = webdriver.Firefox(firefox_options=options)  # DeprecationWarning: firefox_options
driver = webdriver.Firefox(options=options)

driver.get('http://books.toscrape.com/')

# find some elements
elements = driver.find_elements_by_xpath('//div[@class="side_categories"]//ul//ul//a')

# display elements
for item in elements:
    print('category:', item.text)

driver.close()