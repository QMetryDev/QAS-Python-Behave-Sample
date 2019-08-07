from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException


class WaitForAjax(object):
    def __init__(self, snippet):
        self.snippet = snippet

    def __call__(self, driver):
        try:
            value = driver.execute_script(self.snippet)
            return bool(value)
        except StaleElementReferenceException:
            return False


class WaitForVisible(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            value = _find_element(driver, self.locator).is_displayed()
            return value
        except StaleElementReferenceException:
            return False


class WaitForNotVisible(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            value = _find_element(driver, self.locator).is_displayed()
            return not value
        except StaleElementReferenceException:
            return False


class WaitForDisabled(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            value = _find_element(driver, self.locator).is_enabled()
            return not value
        except StaleElementReferenceException:
            return False


class WaitForEnabled(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            value = _find_element(driver, self.locator).is_enabled()
            return value
        except StaleElementReferenceException:
            return False


class WaitForPresent(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            elements = _find_elements(driver, self.locator)
            if elements is not None and len(elements) > 0:
                return True
            else:
                return False
        except NoSuchElementException as e:
            return False


class WaitForNotPresent(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            elements = _find_elements(driver, self.locator)
            if elements is None:
                return True
            else:
                return False
        except NoSuchElementException as e:
            return True


class WaitForText(object):
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = _find_element(driver, self.locator).text
            return self.text == element_text, element_text
        except StaleElementReferenceException:
            return False


class WaitForContainingText(object):
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = _find_element(driver, self.locator).text
            return self.text in element_text, element_text
        except StaleElementReferenceException:
            return False, ''


class WaitForNotText(object):
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = _find_element(driver, self.locator).text
            return self.text != element_text, element_text
        except StaleElementReferenceException:
            return False


class WaitForNotContainingText(object):
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = _find_element(driver, self.locator).text
            return self.text not in element_text, element_text
        except StaleElementReferenceException:
            return False


class WaitForValue(object):
    def __init__(self, locator, value_):
        self.locator = locator
        self.value = value_

    def __call__(self, driver):
        try:
            element_value = _find_element(driver, self.locator).get_attribute("value")
            return self.value == element_value, element_value
        except StaleElementReferenceException:
            return False


class WaitForNotValue(object):
    def __init__(self, locator, value_):
        self.locator = locator
        self.value = value_

    def __call__(self, driver):
        try:
            element_value = _find_element(driver, self.locator).get_attribute("value")
            return self.value != element_value, element_value
        except StaleElementReferenceException:
            return False


class WaitForSelected(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, ignored):
        return self.element.is_selected()


class WaitForNotSelected(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, ignored):
        return not self.element.is_selected()


class WaitForAttribute(object):
    def __init__(self, locator, attr_, value_):
        self.attr = attr_
        self.locator = locator
        self.value = value_

    def __call__(self, driver):
        try:
            element_value = _find_element(driver, self.locator).get_attribute(self.attr)
            return self.value == element_value, element_value
        except StaleElementReferenceException:
            return False


class WaitForNotAttribute(object):
    def __init__(self, locator, attr_, value_):
        self.attr = attr_
        self.locator = locator
        self.value = value_

    def __call__(self, driver):
        try:
            element_value = _find_element(driver, self.locator).get_attribute(self.attr)
            return self.value != element_value, element_value
        except StaleElementReferenceException:
            return False


class WaitForCssClass(object):
    def __init__(self, locator, class_name_):
        self.locator = locator
        self.class_name = class_name_

    def __call__(self, driver):
        try:
            element_class = _find_element(driver, self.locator).get_attribute("class")
            return self.class_name == element_class, element_class
        except StaleElementReferenceException:
            return False


class WaitForNotCssClass(object):
    def __init__(self, locator, class_name_):
        self.locator = locator
        self.class_name = class_name_

    def __call__(self, driver):
        try:
            element_class = _find_element(driver, self.locator).get_attribute("class")
            return self.class_name != element_class, element_class
        except StaleElementReferenceException:
            return False


class WaitForCssStyle(object):
    def __init__(self, locator, style_name_, value_):
        self.locator = locator
        self.style_name = style_name_
        self.value = value_

    def __call__(self, driver):
        try:
            style_value = _find_element(driver, self.locator).value_of_css_property(self.value)
            return self.style_name == style_value, style_value
        except StaleElementReferenceException:
            return False


class WaitForNotCssStyle(object):
    def __init__(self, locator, style_name_, value_):
        self.locator = locator
        self.style_name = style_name_
        self.value = value_

    def __call__(self, driver):
        try:
            style_value = _find_element(driver, self.locator).get_attribute(self.value)
            return self.style_name != style_value, style_value
        except StaleElementReferenceException:
            return False


def _find_element(driver, by):
    try:
        return driver.find_element(*by)
    except NoSuchElementException as e:
        raise e
    except WebDriverException as e:
        raise e


def _find_elements(driver, by):
    try:
        return driver.find_elements(*by)
    except WebDriverException as e:
        raise e
