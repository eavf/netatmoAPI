import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _kluce import login_atmo, pass_atmo

from sql_store import *

def vyber_fav(brows, cas):
    time.sleep(cas)
    # menu = brows.find_element(By.XPATH, '//p[text()="favorites"]')
    menu = brows.find_element(By.XPATH, '//*[contains(concat(" ", normalize-space(@class), " "), " favorites ")]')
    menu.click()

    time.sleep(cas)
    # menu = brows.find_element(By.XPATH, '//a[text()="More details"]')
    menu = brows.find_element(By.XPATH, '//a[contains(concat(" ", normalize-space(@class), " "), " w-link ")]')
    menu.click()

def vyber_fav1(brows, cas, no=1):
    try:
        time.sleep(cas)
        # menu = brows.find_element(By.XPATH, '//p[text()="favorites"]')
        menu = brows.find_element(By.XPATH, '//*[@id="ng-app"]/div[1]/weathermap/div/navbar/div/div[1]/div')
        menu.click()
    except NoSuchElementException:
        print('Failed finding Favorites')
        return None
    """
    //*[@id="ng-app"]/div[1]/weathermap/div/navbar/div/div[1]/div
    /html/body/div[1]/weathermap/div/navbar/div/div[1]/div
    """
    try:
        time.sleep(cas)
        # menu = brows.find_element(By.XPATH, '//p[text()="favorites"]')
        menu = brows.find_element(By.XPATH, f'//*[@id="popup-fav"]/div/fav-panel/div/div/div[1]/div[{no}]/div[2]/a')
        menu.click()
    except NoSuchElementException:
        print('Failed finding link to detailed information')
        return None
    """
    //*[@id="popup-fav"]/div/fav-panel/div/div/div[1]/div[1]/div[2]/a
    //*[@id="popup-fav"]/div/fav-panel/div/div/div[1]/div[2]/div[2]/a
    //*[@id="popup-fav"]/div/fav-panel/div/div/div[1]/div[3]/div[2]/a
    """

def nacitaj_udaje(brows, cas, pos = 1):
    time.sleep(cas)
    # temperature
    st = brows.find_element(By.CSS_SELECTOR, 'div.temperature>p')
    des = brows.find_element(By.CSS_SELECTOR, 'div.temperature>p + p')
    jed = brows.find_element(By.CSS_SELECTOR, 'div.temperature>p + p>span')
    final_temp = str(float(st.text + des.text[:2:1]))
    print("Teplota je: ", final_temp, " desatiny su : ", des.text[:2:1], " a jednotky sú : ", jed.text)

    # humidity
    hu = brows.find_element(By.CSS_SELECTOR, 'div.humidity>p')
    hujed = brows.find_element(By.CSS_SELECTOR, 'div.humidity>p>span')
    i = len(hu.text)
    final_hum = str(float(hu.text[:(i - 2)]))
    print("Vlhkosť = ", final_hum, " ", hujed.text)

    # Presure
    pr = brows.find_element(By.CSS_SELECTOR, 'div.pressure>p')
    prjed = brows.find_element(By.CSS_SELECTOR, 'div.pressure>p>span')
    j = len(pr.text)
    final_pr = str(float(pr.text[:(j - 5)]))
    print("Tlak = ", final_pr, " ", prjed.text)

    # Rainfall
    try:
        # hrs
        rfh = brows.find_element(By.CSS_SELECTOR, 'div.rain-1hour>div')
        rfjedh = brows.find_element(By.CSS_SELECTOR, 'div.rain-1hour>div>span')

        f = len(rfh.text)
        final_rh = str(float(rfh.text[:(f-2)]))
        rfjedhf = rfjedh.text

        # day
        rfd = brows.find_element(By.CSS_SELECTOR, 'div.rain-today>div')
        rfjedd = brows.find_element(By.CSS_SELECTOR, 'div.rain-today>div>span')

        f = len(rfh.text)
        final_rd = str(float(rfd.text[:(f-2)]))
        rfjeddf = rfjedd.text

        print("rain hour = ", final_rh, " ", rfjedhf)
        print("rain day = ", final_rd, " ", rfjeddf)
    except NoSuchElementException:
        print('Failed finding link to rainfall')
        final_rh = final_rd = rfjedhf = rfjeddf = ""

    # Wind
    try:
        # direction
        wd = brows.find_element(By.CSS_SELECTOR, 'div.wind-icon>p.w-text')
        final_wd = str(wd.text)

        # vitesse
        wv = brows.find_element(By.CSS_SELECTOR, 'div.wind-speed>div')
        wvjed = brows.find_element(By.CSS_SELECTOR, 'div.wind-speed>div>span')
        f = len(wv.text)
        final_wv = str(float(wv.text[:(f-4)]))
        wvjedf = wvjed.text

        # rafale
        wr = brows.find_element(By.CSS_SELECTOR, 'div.wind-gust>div')
        wrjed = brows.find_element(By.CSS_SELECTOR, 'div.wind-gust>div>span')
        f = len(wr.text)
        final_wr = str(float(wr.text[:(f-4)]))
        wrjedf = wrjed.text

        print("Wind direction = ", final_wd)
        print("Wind vitesse = ", final_wv, " ", wvjedf)
        print("Wind rafale = ", final_wr, " ", wrjedf)
    except NoSuchElementException:
        print('Failed finding link to wind')
        final_wd = final_wv = final_wr = wvjedf = wrjedf = ""

    # look at ti here
    # https://saucelabs.com/resources/articles/selenium-tips-css-selectors
    """
    div.temperature>p
    div.temperature>p + p
    div.temperature>p + p>span
    """

    return {
        'temp': final_temp,
        'temp_unit': jed.text,
        'humidity': final_hum,
        'hum_unit': hujed.text,
        'pressure': final_pr,
        'press_unit': prjed.text,
        'rain_hrs': final_rh,
        'rain_hrs_unit': rfjedhf,
        'rain_day': final_rd,
        'rain_day_unit': rfjeddf,
        'wind_dir': final_wd,
        'wind_vitesse': final_wv,
        'wind_vitesse_unit': wvjedf,
        'wind_rafale': final_wr,
        'wind_rafale_unit': wrjedf
    }


def get_meteo():
    # Look here for searching with selenium
    # https://selenium-python.readthedocs.io/locating-elements.html#locating-elements
    cas = time.time()
    options = Options()
    options.headless = False
    try:
        browser = webdriver.Firefox(options=options)
    except Exception as e:
        print('Failed opening Firefox webdriver : ' + str(e))
        return None

    url = 'https://auth.netatmo.com/fr-fr/access/login?message=__NOT_LOGGED&next_url=https%3A%2F%2Fweathermap.netatmo.com%2F'
    browser.get(url)
    timeout = 80
    timeeout1 = 2

    # print ("Headless Firefox Initialized")
    time.sleep(timeeout1)
    name = 'email'
    search_el = browser.find_element(By.CSS_SELECTOR, '[name="email"]')
    # print(search_el)
    search_el.send_keys(f"{login_atmo}")

    search_el = browser.find_element(By.CSS_SELECTOR, '[name="password"]')
    # print(search_el)
    search_el.send_keys(f"{pass_atmo}")

    submit_btn = browser.find_element(By.CSS_SELECTOR, "button[id='submit-btn']")
    # print("Submit button coord.:  ---- ", submit_btn.get_attribute('name'))
    time.sleep(timeeout1)
    submit_btn.click()

    # Načítaniee stánky
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'close-slider'))
        WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return None

    close_div = browser.find_element(By.CLASS_NAME, "close-slider")
    time.sleep(timeeout1)
    close_div.click()

    for x in range(5):
        vyber_fav1(browser, timeeout1, x+1)
        budmerice1 = nacitaj_udaje(browser, timeeout1, x+1)
        mesto = "Budmerice"
        if (x+1) == 1:
            wsnm = "Kaplnka"
        elif (x+1) == 2:
            wsnm = "J. Holceka 472"
        elif (x+1) == 3:
            wsnm = "Pod Kastielom"
        elif (x+1) == 4:
            wsnm = "Farma pri potoku"
        elif (x+1) == 5:
            wsnm = "Tichá vinica"
        elif (x+1) == 6:
            mesto = "Bahon"
            wsnm = "Kaplnka"

        budmerice2 = {
            'town': f"{mesto}",
            'wheather_station': f"NetAtmo WS {x+1}: {wsnm}",
            'ws_id': str(x + 1)
        }
        budmerice = budmerice2 | budmerice1
        print (budmerice)
        volaj(budmerice)

    cas = int(round(time.time() - cas))
    print("Program trval: ", cas, " s")

    time.sleep(timeeout1)
    # print ("Headless Firefox Closing")
    browser.quit()

    return None
