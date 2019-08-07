from behave.runner_util import load_step_modules
import sys
import os

# site_packages = next(p for p in sys.path if (p.endswith('site-packages') and p.startswith('/Library')))
# SUBSTEP_DIRS = [os.path.join(site_packages, 'infostretch/automation/step_def')]
load_step_modules(['infostretch/automation/step_def'])
