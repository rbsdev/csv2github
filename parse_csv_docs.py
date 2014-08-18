# -*- coding: UTF-8 -*-
""" This module parses the data from a csv of Google Docs creating
the issues that will be inserted in Github. """


import csv
import config
import github_api

# def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
# 	csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
# 	for row in csv_reader:
# 		yield [unicode(cell, 'utf-8') for cell in row]

# class IssueTypes:
# 	USER_STORY = 1
# 	TASK = 2
# 	TEST_CASE = 3


class Issue:
	def __init__(self, repo, snumber, issue_name, people, hours):
		assert(len(people)==len(hours))
		if snumber != '' and float(snumber) > 0:
			self.number = float(snumber)
		self.name   = issue_name.strip()
		self.repo   = repo
		self.milestone_id = config.milestones_map[self.repo]
		
		self.hours = {}
		for x in range(len(hours)):
			self.hours[people[x]] = float(hours[x])
		
		# self.people = people
		# self.hours  = [float(h) for h in hours];

		# if I don't have a father I am a user story
		# self.father_us = father_us
		# if father_us == None:
		# 	self.type = IssueTypes.USER_STORY
		# else:
		# 	self.type = IssueTypes.TASK	

	def send_issue_github(self, issue_type, father_us):	
		github_issue = dict(title=self.name, milestone=self.milestone_id)		

		if issue_type == 'TASK' and father_us != None:
			github_issue['labels'] = 'Task'	        	
			github_issue['body'] = 'User Story: #'+str(father_us)+'\n'
			if len(self.hours) > 0:
				for h in self.hours:
					github_issue['body'] = github_issue['body']+h+'(@'+config.usernames_map[h]+'): '+str(self.hours[h])+'h\n'
			if len(self.hours) == 1:        			
				for h in self.hours:
					github_issue['assignee'] = config.usernames_map[h]
		elif issue_type == 'US/TASK':
			github_issue['labels'] = ['Task','Story']	        	
			github_issue['body'] = ''
			if len(self.hours) > 0:
				for h in self.hours:
					github_issue['body'] = github_issue['body']+h+'(@'+config.usernames_map[h]+'): '+str(self.hours[h])+'h\n'
			if len(self.hours) == 1:        			
				for h in self.hours:
					github_issue['assignee'] = config.usernames_map[h]
		elif issue_type == 'US':
			github_issue['labels'] = 'Story'
		else:
			print("Type not identified")        

		repo_name = config.repositories_map[self.repo];
		github_issue = github_api.request('/repos/{}/{}/issues'.format(config.owner, repo_name),
			'POST', github_issue, True)

		return github_issue['number']


	def debug(self):
		print("Repo: #"+str(self.repo))
		print("Name:"+self.name)
		print("Hours:"+str(self.hours))


def empty_row(row):
	return ''.join(row).strip() == ''


def extract_issues(filename):
	# with open('some.csv', newline='', encoding='utf-8') as f:
	#    reader = csv.reader(f)
	cvs_file = open(filename, newline='', encoding='utf8')

	with cvs_file as c:
		issue_reader = csv.reader(c)

		# remove all the lines that are empty or after the Total hours
		valid_lines = []
		for r in issue_reader:
			if not empty_row(r):	
				if ''.join(r).find('Total hours') >= 0: 
					break
				valid_lines.append(r)

		# TODO, I am assuming that first non-empty line is the header of the table
		first_line = valid_lines[0]
		us_col = -1
		number_col = -1
		tasks_col = -1
		repo_col = -1
		people = {} #dict: person -> column

		for c, ic in zip(first_line, range(len(first_line))):
			if c.lower() == 'us': us_col = ic
			elif c.lower() == 'number': number_col = ic
			elif c.lower() == 'tasks': tasks_col = ic
			elif c.lower() == 'repository': repo_col = ic
			elif c.strip() != '': people[c.lower()] = ic

		us_issue = None # user story issue
		repo_key = ''
		for line in valid_lines[1:]:
			print('(Line: '+str(line)+')')
		
			# see which people have associated hours in the sprint
			i_people, i_hours = [], []
			if line[us_col] != 'US':
				for p in people:
					shour = line[people[p]]
					if shour != '':
						hour = float(line[people[p]])
						i_people.append(p)
						i_hours.append(hour)

			# tries to create an issue
			# snumber, issue_name, people, hours, us=None):			
			if line[us_col] == 'US':				
				repo_key = line[repo_col]

			issue = Issue(repo_key, line[number_col], line[tasks_col], i_people, i_hours)
			print()
			issue.debug()


			# now send the issue
			if line[us_col].strip() == 'US':				
				us_issue = issue.send_issue_github('US', None)
			elif line[us_col].strip() == 'US/TASK':				
				us_issue = issue.send_issue_github('US/TASK', None)
			elif line[us_col].strip() == 'NOPE':
				pass # do nothing
			else: # task
				issue.send_issue_github('TASK', us_issue)
			













