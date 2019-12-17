Feature: mobileweb

Scenario Outline: VerifyLogin

  Given get "https://qas.qmetry.com/bank/"
  When  clear "text.txtusername"
  And sendKeys "<username>" into "text.txtusername"
  And  clear "password.txtpassword"
  And sendKeys "<password>" into "password.txtpassword"
  And click on "button.btnlogin"
  Then verify "button.button" is visible


Examples:
    |username|password|
    |Bob|Bob|
    |Sarah|Sarah|

