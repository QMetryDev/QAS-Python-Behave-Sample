Feature: windows

Scenario: windowsTestcase

  When click on "..window..window.2...group..group.5...button.2."
  And click on "..window..window.2...group..group.4...button.4."
  And click on "..window..window.2...group..group.5...button.4."
  And click on "..window..window.2...group..group.4...button.5."
  Then verify "..window..window.2...group..text.2." is present

