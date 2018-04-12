import time
from selenium import webdriver

ADS_LIST = ["""//*[@id="vn1s0p2c0"]""", """//*[@id="vn1s0p3c0"]""", """//*[@id="vn1s0p4c0"]""", """//*[@id="vn1s3p1c0"]""", """//*[@id="vn1s3p2c0"]""", """//*[@id="vn1s3p3c0"]"""]


def headlessGoogleAds(url, xpath, lifetime, headless=True):

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1200x600')
    if headless:
        options.add_argument('headless')

    browser = webdriver.Chrome(chrome_options = options)
    browser.get(url)

    time.sleep(lifetime)

    adsText=[]
    for i in ADS_LIST:
        adsText.append(browser.find_element_by_xpath(i).text.strip())

    #search_input = browser.find_element_by_xpath(xpath)
    #print search_input.text.strip()

    browser.close()
    return adsText

if __name__ == "__main__":
    url = "https://www.google.com/search?q=all+car+insurance+quotes&oq=all+car+insurance+quotes&aqs=chrome..69i57j0l2.681j0j7&sourceid=chrome&ie=UTF-8"

    xpath = '//*[@id="tads"]/ol/li'

    ads=headlessGoogleAds(url, xpath, 1, headless=False)
    for i in ads:
        print i




