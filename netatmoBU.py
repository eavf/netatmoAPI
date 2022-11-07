import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _kluce import login_atmo, pass_atmo


def get_meteo()
    # Look here for searching with selenium
    # https://selenium-python.readthedocs.io/locating-elements.html#locating-elements
    cas = time.time()
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    url = 'https://auth.netatmo.com/fr-fr/access/login?message=__NOT_LOGGED&next_url=https%3A%2F%2Fweathermap.netatmo.com%2F'
    browser.get(url)
    timeout = 80
    timeeout1 = 2

    #print ("Headless Firefox Initialized")
    time.sleep(timeeout1)
    name = 'email'
    search_el = browser.find_element(By.CSS_SELECTOR, '[name="email"]')
    #print(search_el)
    search_el.send_keys(f"{login_atmo}")

    search_el = browser.find_element(By.CSS_SELECTOR, '[name="password"]')
    #print(search_el)
    search_el.send_keys(f"{pass_atmo}")

    submit_btn = browser.find_element(By.CSS_SELECTOR, "button[id='submit-btn']")
    #print("Submit button coord.:  ---- ", submit_btn.get_attribute('name'))
    time.sleep(timeeout1)
    submit_btn.click()

    # Načítaniee stánky
    try:
        element_present = EC.presence_of_element_located((By.ID, 'close-slider'))
        WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out waiting for page to load")
        return None

    close_div = browser.find_element(By.CLASS_NAME, "close-slider")
    time.sleep(timeeout1)
    close_div.click()

    time.sleep(timeeout1)
    menu = browser.find_element(By.XPATH, '//p[text()="Favorites"]')
    menu.click()

    time.sleep(timeeout1)
    menu = browser.find_element(By.XPATH, '//a[text()="More details"]')
    menu.click()

    st = browser.find_element(By.CSS_SELECTOR, 'div.temperature>p')
    des = browser.find_element(By.CSS_SELECTOR, 'div.temperature>p + p')
    jed = browser.find_element(By.CSS_SELECTOR, 'div.temperature>p + p>span')
    final_temp = st.text + des.text
    #print ("Teplota je: ", final_temp, " ", jed.text)

    # humidity
    hu = browser.find_element(By.CSS_SELECTOR, 'div.humidity>p')
    hujed = browser.find_element(By.CSS_SELECTOR, 'div.humidity>p>span')
    #print ("Vlhkosť = ", hu.text, " ", hujed.text)

    # Presure
    pr = browser.find_element(By.CSS_SELECTOR, 'div.pressure>p')
    prjed = browser.find_element(By.CSS_SELECTOR, 'div.pressure>p>span')
    #print ("Tlak = ", pr.text, " ", prjed.text)

    # look at ti here
    # https://saucelabs.com/resources/articles/selenium-tips-css-selectors
    """
    div.temperature>p
    div.temperature>p + p
    div.temperature>p + p>span
    """
    #print ("Headless Firefox Closing")
    browser.quit()
    cas = int(round(time.time() - cas))
    #print("Program trval: ", cas, " s")
    budmerice = {
        'town': "Budmerice",
        'wheather_station': "NetAtmo Weather station",
        'temp': int(final_temp),
        'temp_unit': jed.text,
        'humidity': int(hu.text),
        'hum_unit': hujed.text,
        'pressure': int(pr.text),
        'press_unit': prjed.text
    }
    return budmerice

