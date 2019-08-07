Feature: Python Test suite

Scenario Outline: Mobile

  Given get "http://www.gmail.com"
  When  clear "test"
  And sendKeys "demoqas2019@gmail.com" into "test"
  And click on "div.div2111"
  Then verify "test" value is "demoqas2019@gmail.com"
  When click on "test1"
  And  clear "test2"
  And sendKeys "${Password}" into "test2"
  # And click on "div.div111_2"
  Then verify "test2" value is "${Password}"
  When click on "span.span1111_1_1"


Examples:
    |Data-1|Data-2|Password|
    |||test|
    |||qastest|
    |||QAS@2019|

