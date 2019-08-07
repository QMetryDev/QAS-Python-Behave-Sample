from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By


def get_find_by(locator):
    value = ''
    if locator.startswith('xpath='):
        by = By.XPATH
        value = locator.split('xpath=', 1)[1]
    elif locator.startswith('//'):
        by = By.XPATH
        value = locator
    elif locator.startswith('id='):
        by = By.ID
        value = locator.split('id=', 1)[1]
    elif locator.startswith('name='):
        by = By.NAME
        value = locator.split('name=', 1)[1]
    elif locator.startswith('class='):
        by = By.XPATH
        value = "//*[@class='" + locator.split('class=', 1)[1] + "']"
    elif locator.startswith('text='):
        by = By.XPATH
        value = "//*[@text='" + locator.split('text=', 1)[1] + "']"
    elif locator.startswith('css='):
        by = By.CSS_SELECTOR
        value = locator.split('text=', 1)[1]
    elif locator.startswith('content-desc='):
        by = By.XPATH
        value = '//*[@*="' + locator.split('content-desc=', 1)[1] + '"]'
    elif "=" in locator:
        by = str(locator).split("=")[0]
        value = str(locator).split("=")[1]
    else:
        by = By.ID
        value = str(locator)
    return by, value
