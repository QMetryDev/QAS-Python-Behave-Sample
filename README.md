# python Behave

### To Get Started
	This is sample project with Python Behave directory structure.
#### Pre-requisites

1.Install python latest version and set environment variable to execute pip and behave.

* All the dependencies use following command.
```
pip install -r requirements.txt
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
