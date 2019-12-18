Feature: mobileweb

Scenario: VerifyCreditedAmount

  # Launch site
  Given get "https://qas.qmetry.com/bank"

  # Maximize browser window. (Custom bdd step - Find the definition at stepdefs.mobileweb)
  Then maximize window

  # Login 
  And wait until "text.txtusername" to be enable
  And clear "text.txtusername"
  And sendKeys "Bob" into "text.txtusername"
  Then wait until "password.txtpassword" to be enable
  And clear "password.txtpassword"
  And sendKeys "Bob" into "password.txtpassword"
  Then wait until "button.btnlogin" to be enable
  And click on "button.btnlogin"

  # Verify successful login
  And assert "button.logout" is present
    
  # Store the current balance into variable
  Then get text of "text.currentbalance"

  Then wait until "number.enteramountforcredit" to be enable
  And clear "number.enteramountforcredit"
  And sendKeys "1000" into "number.enteramountforcredit"
  And wait until "button.credit" to be enable
  And click on "button.credit"

  # Verify success message of credit operation
  Then assert "operation.success.message" is present

  # Verify current updated balance(Custom bdd step - Find the definition at stepdefs.mobileweb)
  And verify "1000" has been credited to "text.currentbalance"

  # Logout
  And wait until "button.logout" to be enable
  And click on "button.logout"

  # Verify successful logout
  And assert "button.btnlogin" is present

