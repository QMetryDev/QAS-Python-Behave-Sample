Feature: Python Test suite

Scenario: Android

  When sendKeys "Bob" into "email"
  Then verify "email" text is "Bob"
  When sendKeys "Bob" into "password"
  Then verify "password" text is "Bob"
  When click on "sign.in"
  And click on ".fund..transfer"
  And sendKeys "34" into "enter.amount"
  Then verify "enter.amount" text is "34"
  When click on "fund.transfer"
  And click on "transacations"
  And sendKeys "100" into "enter.amount"
  Then verify "credit" is present
  When click on "credit"

