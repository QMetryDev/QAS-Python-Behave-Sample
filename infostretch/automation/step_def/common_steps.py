from behave import *
from selenium.webdriver import ActionChains
from infostretch.automation.core.configurations_manager import ConfigurationsManager
from infostretch.automation.ui.webdriver.base_test_page import BaseTestPage

from infostretch.automation.ui.webdriver.base_driver import BaseDriver
from infostretch.automation.ui.webdriver.paf_web_element import PAFWebElement
from infostretch.automation.core.resources_manager import ResourcesManager
from infostretch.automation.keys.application_properties import ApplicationProperties
from infostretch.automation.util.locator_util import LocatorUtil
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
#import ConfigParser
import time
#config.read('ConfigFile.properties')
import json

use_step_matcher('re')
def process(text):
        if (text.startswith('${')):
                leng = len(text)
                text=  text[2:leng-1]
                text = str(ConfigurationsManager().get_str_for_key(text))
        return text

def remove_doller_key(text):
        leng = len(text)
        text=text[2:leng-1]
        return text

@step(u'COMMENT: "(.*)"')
def comment(context, value):
    print(process(value))

@step(u'change locale to: "(.*)"')
def comment(context, value):
    ResourcesManager.defaultLanguage=value
    ResourcesManager().set_up()

@step('store "(?P<val>\S+)" into "(?P<var>.*)"')
def store_into(context, val, var):
    ConfigurationsManager().set_object_for_key(var, process(val))

@step('sendKeys "(.*)" into "(.*)"')
def step_keys(context, text, loc):
    PAFWebElement(loc).send_keys(process(text))

@step('select "(.*)" in "(.*)"')
def select(context, text, loc):
    PAFWebElement(loc).send_keys(process(text))

@step('assert "(.*)" is present')
def assert_is_present(context, loc):
    PAFWebElement(loc).assert_present()

@step('assert link with text "(.*)" is present')
def assert_link_with_test_is_present(context, link_text):
#     PAFWebElement('linkText=' + process(link_text)).assert_present()
    BaseDriver().get_driver().find_element_by_link_text(process(link_text)).assert_present()

@step('assert link with partial text "(.*)" is present')
def assert_link_with_partial_text(context, link_text):
#     PAFWebElement('partialLinkText=' + process(link_text)).assert_present()
    BaseDriver().get_driver().find_element_by_partial_link_text(process(link_text)).assert_present()

@step('verify "(?P<loc>\S+)" is present')
def verify_is_present(context, loc):
    PAFWebElement(loc).verify_present()

@step('verify link with text "(.*)" is present')
def verify_link_with_text_is_present(context, link_text):
#      PAFWebElement('linkText=' + process(link_text)).verify_present()
     BaseDriver().get_driver().find_element_by_link_text(process(link_text)).verify_present()

@step('verify link with partial text "(.*)" is present')
def verify_link_with_partial_text_is_present(context, link_text):
#     PAFWebElement('partialLinkText=' + process(link_text)).verify_present()
    BaseDriver().get_driver().find_element_by_partial_link_text(process(link_text)).verify_present()

@step('assert "(.*)" is visible')
def asseet_is_visible(context, loc):
    PAFWebElement(loc).assert_visible()

@step('verify "(.*)" is visible')
def verify_is_visible(context, loc):
    PAFWebElement(loc).verify_visible()

@step('get "(.*)"')
def get(context, url):
    if not str(process(url)).startswith("http"):
                url = ConfigurationsManager().get_str_for_key(
                ApplicationProperties.SELENIUM_BASE_URL)
    BaseDriver().get_driver().get(process(url))

@step('switch to "(?P<driver_name>.*)"')
def switch_to(context, driver_name):
    raise NotImplemented

@step('tear down driver')
def tear_down_driver(context):
    raise NotImplemented

@step('switch to "(?P<name_or_index>\S+)" window')
def switch_to_window(context, name_or_index):
    if isinstance(name_or_index, int):
        windows = BaseDriver().get_driver().window_handles()
        BaseDriver().get_driver().switch_to_window(windows[name_or_index])
    else:
        BaseDriver().get_driver().switch_to_window(name_or_index)

@step('clear "(.*)"')
def clear(context, loc):
    PAFWebElement(loc).clear()

@step('get text of "(.*)"')
def get_text_of(context, loc):
    # PAFWebElement(loc).wait_for_present(wait_time=30000)
    ConfigurationsManager().set_object_for_key(
        "lastStepResult", PAFWebElement(loc).text)

@step('submit "(.*)"')
def submit(context, loc):
    PAFWebElement(loc).submit()

@step('click on "(.*)"')
def click_on(context, loc):
    PAFWebElement(loc).click()

@step('wait until "(\S+)" to be visible')
def wait_until_to_be_visible(context, loc):
    PAFWebElement(loc).wait_for_visible()

@step('wait until "(\S+)" not to be visible')
def wait_until_not_to_be_visible(context, loc):
    PAFWebElement(loc).wait_for_not_visible()

@step('wait until "(\S+)" to be disable')
def wait_until_to_be_desable(context, loc):
    PAFWebElement(loc).wait_for_disabled()

@step('wait until "(\S+)" to be enable')
def wait_until_not_to_be_enable(context, loc):
    PAFWebElement(loc).wait_for_enabled()

@step('wait until "(\S+)" to be present')
def wait_until_to_be_present(context, loc):
    PAFWebElement(loc).wait_for_present()

@step('wait until "(\S+)" is not present')
def wait_until_is_not_present(context, loc):
    PAFWebElement(loc).wait_for_not_present()

@step('wait until "(\S+)" text "(?P<text>.*)"')
def wait_until_text(context, loc, text):
    PAFWebElement(loc).wait_for_text(process(text))

@step('wait until "(\S+)" text is not "(?P<text>.*)"')
def wait_until_text_is_not(context, loc, text):
    PAFWebElement(loc).wait_for_not_text(process(text))

@step('wait until "(\S+)" value is "(?P<value>.*)"')
def wait_until_value_is(context, loc, value):
    PAFWebElement(loc).wait_for_value(process(value))

@step('wait until "(\S+)" value is not "(?P<value>.*)"')
def wait_until_value_is_not(context, loc, value):
    PAFWebElement(loc).wait_for_not_value(process(value))

@step('wait until "(\S+)" to be selected')
def wait_until_to_be_selected(context, loc):
    PAFWebElement(loc).wait_for_selected()

@step('wait until "(\S+)" is not selected')
def wait_until_is_not_selected(context, loc):
    PAFWebElement(loc).wait_for_not_selected()

@step('wait until "(\S+)" for attribute "(?P<attr>\S+)" value is "(?P<value>.*)"')
def wait_until_for_attribute_value_is(context, loc, attr, value):
    PAFWebElement(loc).wait_for_attribute(process(attr), process(value))

@step('wait until "(\S+)" attribute "(?P<attr>\S+)" value is not "(?P<value>.*)"')
def wait_until_for_attribute_value_is_not(context, loc, attr, value):
    PAFWebElement(loc).wait_for_not_attribute(process(attr), process(value))

@step('wait until "(\S+)" css class name is "(?P<class_name>.*)"')
def wait_until_css_class_name_is(context, loc, class_name):
    PAFWebElement(loc).wait_for_css_class(process(class_name))

@step('wait until "(\S+)" css class name is not "(?P<class_name>.*)"')
def wait_until_css_class_name_is_not(context, loc, class_name):
    PAFWebElement(loc).wait_for_not_css_class(process(class_name))

@step('wait until "(\S+)" property "(?P<prop>\S+)" value is "(?P<value>.*)"')
def wait_until_property_value_is(context, loc, prop, value):
    PAFWebElement(loc).wait_for_attribute(process(prop), process(value))

@step('wait until "(\S+)" property "(?P<prop>\S+)" value is not "(?P<value>.*)"')
def wait_until_property_value_is_not(context, loc, prop, value):
    PAFWebElement(loc).wait_for_not_attribute(process(prop), process(value))

@step('verify "(\S+)" not present')
def verify_not_present(context, loc):
    PAFWebElement(loc).verify_not_present()

@step('wait until ajax call complete')
def wait_until_ajax_call_complete(context):
    BaseDriver().get_driver().wait_for_ajax()

@step('wait until "(?P<jstoolkit>\S+)" ajax call complete')
def wait_until_ajax_value_call_complete(context, jstoolkit):
    BaseDriver().get_driver().wait_for_ajax(jstoolkit=jstoolkit)

@step('verify "(\S+)" not visible')
def verify_not_visible(context, loc):
    PAFWebElement(loc).verify_not_visible()

@step('verify "(\S+)" enabled')
def verify_enable(context, loc):
    PAFWebElement(loc).verify_enabled()

@step('verify "(\S+)" disabled')
def verify_disable(context, loc):
    PAFWebElement(loc).verify_disabled()

@step('verify "(\S+)" text is "(?P<text>.*)"')
def verify_text_is_present(context, loc, text):
    PAFWebElement(loc).verify_text(process(text))

@step('verify "(\S+)" text is not "(?P<text>.*)"')
def verify_text_is_not_present(context, loc, text):
    PAFWebElement(loc).verify_not_text(process(text))

@step('verify "(\S+)" value is "(?P<value>.*)"')
def verify_value_is(context, loc, value):
    PAFWebElement(loc).verify_value(process(value))

@step('verify "(\S+)" value is not "(?P<value>.*)"')
def verify_value_is_not(context, loc, value):
    PAFWebElement(loc).verify_not_value(process(value))

@step('verify "(\S+)" is selected')
def verify_is_selected(context, loc):
    PAFWebElement(loc).verify_selected()

@step('verify "(\S+)" is not selected')
def verify_is_not_selected(context, loc):
    PAFWebElement(loc).verify_not_selected()

@step('verify "(\S+)" attribute "(?P<attr>\S+)" value is "(?P<value>.*)"')
def verify_attribute_value_is(context, loc, attr, value):
    PAFWebElement(loc).verify_attribute(process(attr), process(value))

@step('verify "(\S+)" attribute "(?P<attr>\S+)" value is not "(?P<value>.*)"')
def verify_attribute_value_is_not(context, loc, attr, value):
    PAFWebElement(loc).verify_not_attribute(process(attr), process(value))

@step('verify "(\S+)" css class name is "(?P<class_name>.*)"')
def verify_css_class_name_is(context, loc, class_name):
    PAFWebElement(loc).verify_css_class(process(class_name))

@step('verify "(\S+)" css class name is not "(?P<class_name>.*)"')
def verify_css_class_name_is_not(context, loc, class_name):
    PAFWebElement(loc).verify_not_css_class(process(class_name))

@step('verify "(\S+)" property "(?P<prop>\S+)" value is "(?P<value>.*)"')
def verify_property_value_is(context, loc, prop, value):
    PAFWebElement(loc).verify_attribute(process(prop), process(value))

@step('verify "(\S+)" property "(?P<prop>\S+)" value is not "(?P<value>.*)"')
def verify_property_value_is_not(context, loc, prop, value):
    PAFWebElement(loc).verify_not_attribute(process(prop), process(value))

@step('assert "(\S+)" is not present')
def assert_is_not_present(context, loc):
    PAFWebElement(loc).assert_not_present()

@step('assert "(\S+)" is not visible')
def assert_is_not_visible(context, loc):
    PAFWebElement(loc).assert_not_visible()

@step('assert "(\S+)" is enable')
def assert_is_enable(context, loc):
    PAFWebElement(loc).assert_enabled()

@step('assert "(\S+)" is disable')
def assert_is_desable(context, loc):
    PAFWebElement(loc).assert_disabled()

@step('assert "(\S+)" text is "(?P<text>.*)"')
def assert_text_is(context, loc, text):
    PAFWebElement(loc).assert_text(process(text))

@step('assert "(\S+)" text is not "(?P<text>.*)"')
def assert_text_is_not(context, loc, text):
    PAFWebElement(loc).assert_not_text(process(text))

@step('assert "(\S+)" value is "(?P<value>.*)"')
def assert_value_is(context, loc, value):
    PAFWebElement(loc).assert_value(process(value))

@step('assert "(\S+)" value is not "(?P<value>.*)"')
def assert_value_is_not(context, loc, value):
    PAFWebElement(loc).assert_not_value(process(value))

@step('assert "(\S+)" is not selected')
def assert_is_not_selected(context, loc):
    PAFWebElement(loc).assert_not_selected()

@step('assert "(\S+)" attribute "(?P<attr>\S+)" value is "(?P<value>.*)"')
def assert_attribute_value_is(context, loc, attr, value):
    PAFWebElement(loc).assert_attribute(process(attr), process(value))

@step('assert "(\S+)" attribute "(?P<attr>\S+)" value is not "(?P<value>.*)"')
def assert_attribute_value_is_not(context, loc, attr, value):
    PAFWebElement(loc).assert_not_attribute(process(attr), process(value))

@step('assert "(\S+)" css class name is "(?P<class_name>.*)"')
def assert_css_class_name_is(context, loc, class_name):
    PAFWebElement(loc).assert_css_class(process(class_name))

@step('assert "(\S+)" css class name is not "(?P<class_name>.*)"')
def assert_css_class_name_is_not(context, loc, class_name):
    PAFWebElement(loc).assert_not_css_class(process(class_name))

@step('assert "(\S+)" property "(?P<prop>\S+)" value is "(?P<value>.*)"')
def assert_property_value_is(context, loc, prop, value):
    PAFWebElement(loc).assert_attribute(process(prop), process(value))

@step('assert "(\S+)" property "(?P<prop>\S+)" value is not "(?P<value>.*)"')
def assert_property_value_is_not(context, loc, prop, value):
    PAFWebElement(loc).assert_not_attribute(process(prop), process(value))

@step('set "(.*)" attribute "(?P<attr>\S+)" value is "(?P<value>.*)"')
def set_attribute_value_is(context, loc, attr, value):
    element = PAFWebElement(loc)
    BaseDriver().get_driver().execute_script(
        "arguments[0].{attr} = arguments[1]".format(attr=process(attr)), element, process(value))

@step('add cookie "(?P<name>\S+)" with value "(?P<value>.*)"')
def add_cookie_with_value(context, name, value):
    BaseDriver().get_driver().add_cookie({process(name): process(value)})

@step('delete cookie with name "(?P<name>.*)"')
def delete_cookie_with_name(context, name):
    BaseDriver().get_driver().delete_cookie(process(name))

@step('delete all cookies')
def delete_all_cookies(context):
    BaseDriver().get_driver().delete_all_cookies()

@step('get a cookie with a name "(?P<name>.*)"')
def get_a_cookie_with_a_name(context, name):
    BaseDriver().get_driver().get_cookie(process(name))

@step('mouse move on "(.*)"')
def mouse_move_on(context, loc):
    location = PAFWebElement(loc).location
    ActionChains(BaseDriver().get_driver()).move_by_offset(
        location['x'], location['y'])

@step('switch to frame "(?P<frame_name>.*)"')
def switch_to_frame(context, frame_name):
    BaseDriver().get_driver().switch_to_frame(PAFWebElement(frame_name).locator)

@step('switch to default content')
def switch_to_parent_frame(context):
    BaseDriver().get_driver().switch_to_default_content()

@step('switch to "(.*)" platform')
def switch_to_platform(context, platform):
    BaseDriver().stop_driver()
    ResourcesManager().load_directory(["resources/"+process(platform)])

@step('type Enter "(.*)"')
def click_on(context, loc):
    PAFWebElement(loc).send_keys(Keys.RETURN)

@step('close "(.*)"')
def close(context, loc) :
    BaseDriver().get_driver().close()


@step('switchWindow "(.*)"')
def switchWindow(context, index) :
    BaseDriver().get_driver().switch_to_window(BaseDriver().get_driver().window_handles[int(index)])

@step('implicit wait "(.*)" millisec')
def implicitWait(context, sec):
    millisec = (int(sec)/1000)
    time.sleep(millisec)

@step('setBeforeLambdaCap "(.*)"')
def setbeforeLambdaCap(context,index):
    print("setbeforeLambdaCap method called : ")
    BaseDriver().stop_driver()
    capObj=json.loads(index)
    capNew =  (json.dumps(capObj['cap'])).replace("'", "\"")
    ConfigurationsManager().set_object_for_key(ApplicationProperties.DRIVER_NAME,'lambdaTest')
    ConfigurationsManager().set_object_for_key(ApplicationProperties.REMOTE_SERVER,capObj['remote.server'])
    ConfigurationsManager().set_object_for_key('lambda.additional.capabilities',capNew)

@step('setAfterLamdaCap')
def setAfterLamdaCap(context):
    print("setAfterLamdaCap method called : ")
    ConfigurationsManager().set_object_for_key(ApplicationProperties.REMOTE_SERVER,'http://localhost:')
    ConfigurationsManager().set_object_for_key(ApplicationProperties.DRIVER_NAME,'chromeDriver')
    BaseDriver().stop_driver()

@step('maximizeWindow')
def maximizeWindow(self):
    BaseDriver().get_driver().maximize_window()

@step('drag "(.*)" and drop on "(.*)" perform')
def dragAndDropPerform(context,source,target):
    x = target.split("=")
    s="="
    typeBy=x[0]
    x.pop(0)
    loc = s.join(x)
    # ActionChains(BaseDriver().get_driver()).drag_and_drop(BaseDriver().get_driver().find_element_by_xpath("//a[contains(text(),'BANK')]"), BaseDriver().get_driver().find_element_by_xpath("//ol[@id='bank']/li")).perform()
    ActionChains(BaseDriver().get_driver()).click_and_hold(Find_PAFWebElement(PAFWebElement(source).by,PAFWebElement(source).locator)).release(Find_PAFWebElement(typeBy,loc)).perform()
    # ActionChains(BaseDriver().get_driver()).click_and_hold(BaseDriver().get_driver().find_element_by_xpath("//a[contains(text(),'BANK')]")).release(BaseDriver().get_driver().find_element_by_xpath("//ol[@id='bank']/li")).perform()

@step('offsetdrag "(.*)" and drop on "(.*)" and "(.*)" perform')
def offsetDragAndDropPerform(context,source,xtarget,ytarget):
    # ActionChains(BaseDriver().get_driver()).drag_and_drop_by_offset(source_element,int(xtarget),int(ytarget)).perform()
    ActionChains(BaseDriver().get_driver()).click_and_hold(Find_PAFWebElement(PAFWebElement(source).by,PAFWebElement(source).locator)).move_by_offset(int(xtarget),int(ytarget)).release().perform()

def Find_PAFWebElement(by,locator):
    loc = str(locator)
    if str(by) == "id":
        rdata = BaseDriver().get_driver().find_element_by_id(loc)
        return rdata
    if str(by) == 'xpath':
        rdata = BaseDriver().get_driver().find_element_by_xpath(loc)
        return rdata
    elif str(by) == "name":
        rdata = BaseDriver().get_driver().find_element_by_name(loc)
        return rdata
    elif str(by) == "link text":
        rdata = BaseDriver().get_driver().find_element_by_link_text(loc)
        return rdata
    elif str(by) == "partial link text":
        rdata = BaseDriver().get_driver().find_element_by_partial_link_text(loc)
        return rdata
    elif str(by) == "tag name":
        rdata = BaseDriver().get_driver().find_element_by_tag_name(loc)
        return rdata
    elif str(by) == "css selector":
        rdata = BaseDriver().get_driver().find_element_by_css_name(loc)
        return rdata
    elif str(by) == "class name":
        rdata = BaseDriver().get_driver().find_element_by_class_selector(loc)
        return rdata
    else:
        print("Type of element is not recognised")
