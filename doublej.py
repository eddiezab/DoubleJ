#!/usr/bin/python

import sys
import jinja2, json

class TemplateRenderer:

	template_data = None
	jinja2_env = None

	def __init__(self, variable_file, latex_environment=False):
		if not latex_environment:
			self.jinja2_env = jinja2.Environment(
				loader = jinja2.PackageLoader('doublej', 'templates')
			)
		else:
			self.jinja2_env = jinja2.Environment(
				loader = jinja2.PackageLoader('doublej', 'templates'),
				block_start_string = '[%',
				block_end_string = '[%',
				variable_start_string = '[[',
				variable_end_string = ']]',
				comment_start_string = '[#',
				comment_end_string = '#]',
			)

		with open(variable_file, 'r') as json_data:
			self.template_data = json.loads(json_data.read())

	def addVariableFile(self, variable_file):
		with open(variable_file, 'r') as json_data:
			self.template_data = dict(self.template_data.items() + json.loads(json_data.read()).items())

	def renderTemplate(self, template_file, out_file):
		try:
			template = self.jinja2_env.get_template(template_file)
		except jinja2.TemplateNotFound:
			print('Template not found: %s' % template_file) 
			sys.exit(1)
		except jinja2.TemplateSyntaxError:
			print('Template syntax error: %s' % template_file)
			sys.exit(2)
		with open(out_file, 'w') as rendered_outfile:
			rendered_outfile.write(
				template.render(self.template_data)
			)

if __name__ == '__main__':	
	testRenderer = TemplateRenderer(sys.argv[1], latex_environment=True)
	testRenderer.renderTemplate(sys.argv[2],sys.argv[3])
	if 4 in sys.argv:
		testRenderer.addVariableFile(sys.argv[4])