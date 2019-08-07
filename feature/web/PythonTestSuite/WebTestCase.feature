Feature: Python Test suite

Scenario Outline: Web test case

  Given get "http://www.gmail.com"
  When  clear "email.identifierid"
  And sendKeys "demoqas2019@gmail.com" into "email.identifierid"
  And click on "div.div111"
  Then verify "email.identifierid" value is "demoqas2019@gmail.com"
  When click on "span.span1111"
  And  clear "password.qas2019"
  And sendKeys "${Password}" into "password.qas2019"
  And click on "div.div111_1"
  Then verify "password.qas2019" value is "${Password}"
  When click on "span.span1111_1"


Examples:
    |Data-1|Data-2|Password|
    |||test|
    |||qastest|
    |||QAS@2019|

