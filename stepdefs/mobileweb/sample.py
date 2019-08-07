from behave import *

from model.home_page import HomePage

use_step_matcher("re")

class SampleSteps:

	@given('sample step')
	def sample_Step(context):
		#write code here
		pass