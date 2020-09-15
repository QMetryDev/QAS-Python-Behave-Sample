# Python Behave

### To Get Started
	This is sample project with Python Behave directory structure.
#### Pre-requisites

1.Install python latest version and set environment variable to execute pip and behave.

2.Python must be above 3.0 version.you can use pip with `alias name` like 3 etc based on your python installed.

3.Compatible chromedriver path should be set in your system and in application.properties file if it is present in your project folder for command line execution.

Python must be above 3.0 version.you can use pip with `alias name` like 3 etc based your pip installed.
* All the dependencies use following command.
```
pip(Alias Name) install -r requirements.txt

brew tap homebrew/cask && brew cask install chromedriver
```

it will install all dependencies from requirements.txt and You can add your own dependencies also.
#### Now just run the test , switched to the Features folder.Use the following commands

* To run a specific scenario :
	```
	behave -n "<SCENARIO_NAME>"
	```
* To run a feature file :
	```
	behave "<FEATURE_FILE_PATH>"
	```
* To run multiple feature file :
	```
	<!-- behave "<FEATURE_ONE.feature>" "<FEATURE_TWO.feature>" -->
	```
* To run all feature file using CI/CD :
	```
	behave feature
	```


#### View Results.
	'QMetry' Menu > Automation Test Report
