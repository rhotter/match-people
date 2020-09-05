from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import random

import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_raw_spreadsheet_data(spreadsheet_id, spreadsheet_range):
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)

	# Call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=spreadsheet_id,
								range=spreadsheet_range).execute()
	values = result.get('values', [])

	return values

def extract_person(topic_name):
	person = re.findall(r'\(([^()]*)\)$', topic_name)
	if person != []:
		person = person[0]
		person = person.split(",")[0] # TODO: should combine this in regex above
		
		# capitalize first letter
		person = person[0].upper() + person[1:]

		# remove trailing whitespaces
		while person[-1] == ' ':
			person = person[:-1]
	else:
		person = ''
	return person

def _get_out_people(row, cols, people_names):
	data_cols_vals = [row[i] for i in cols if i < len(row)]
	out, topics = [], []
	for topic_name in data_cols_vals:
		person_name = extract_person(topic_name)
		if person_name in out:
			print(f"{person_name} already selected.")
		elif person_name in people_names and person_name not in out: # if a valid new person
			out.append(person_name)
			
			if "," in re.findall('\((.*?)\)',topic_name)[-1]:
				processed_topic_name = re.sub('\(.*, ','(', topic_name) # TODO handle the case without comma
			else:
				last_parantheses_index = topic_name[::-1].find("(") # reverse string first since find() returns first occurence (we want last occurence)
				processed_topic_name = topic_name[:-last_parantheses_index-2]

			topics.append(processed_topic_name)
	return out, topics

def _get_out_topics(row, cols):
	topics = [row[i] for i in cols]
	return topics

def _process_raw_spreadsheet_data(values, cols, people=True, ignore_topics={}):
	data = []
	people_to_topics = {}
	name_col = cols[0]
	out_cols=cols[1:]
	start_row=1
	people_names = {row[name_col] for row in values[start_row:]}
	for row in values[start_row:]:
		if people:
			out, topics = _get_out_people(row, out_cols, people_names)
			for person, topic in zip(out, topics):
				people_to_topics[person] = topic
		else:
			out = _get_out_topics(row, out_cols)
		out = [x for x in out if x not in ignore_topics]
		data.append({
			'name': row[name_col],
			'out': out
		})
	return data, people_to_topics

def get_data(spreadsheet_id, spreadsheet_range, ignore_topics={}, cols=[1,2,3,4], people=True):
	values = get_raw_spreadsheet_data(spreadsheet_id, spreadsheet_range)
	data, people_to_topics = _process_raw_spreadsheet_data(values, cols, people, ignore_topics)
	
	if people:
		return data, people_to_topics
	else:
		return data
# def get_generated_data(n_people, n_preferences):
# 	fake_names = {'Avery', 'Riley', 'Jordan', 'Angel', 'Parker', 'Sawyer', 'Peyton', 'Quinn', 'Blake', 'Hayden', 'Taylor', 'Alexis', 'Rowan', 'Charlie', 'Emerson', 'Finley', 'River', 'Ariel', 'Emery', 'Morgan', 'Elliot', 'London', 'Eden', 'Elliott', 'Karter', 'Dakota', 'Reese', 'Zion', 'Remington', 'Payton', 'Amari', 'Phoenix', 'Kendall', 'Harley', 'Rylan', 'Marley', 'Dallas', 'Skyler', 'Spencer', 'Sage', 'Kyrie', 'Lyric', 'Ellis', 'Rory', 'Remi', 'Justice', 'Ali', 'Haven', 'Tatum', 'Kamryn'}
# 	data = []
# 	for name in fake_names:
# 		other_people = fake_names.difference(set({name}))
# 		data.append({'name': name, 'out': random.sample(other_people, n_preferences)})
# 	return data

def get_generated_data(n_people, n_preferences):
	data = []
	for i in range(n_people):
		other_people = set(range(n_people)).difference(set({i}))
		data.append({'name': i, 'out': random.sample(other_people, n_preferences)})
	return data

# data = [
#   {'name': 'Raffi',
#   'out': ['Santi', 'Erin'] # in priority ordering
#   },
#   {'name': 'Santi',
#   'out': ['Raffi', 'Marley'],
#   },
#   {'name': 'Marley',
#   'out': ['Santi', 'Erin']
#   },
#   {'name': 'Erin',
#   'out': ['Raffi', 'Marley']
#   }]
# optimal grouping is (Marley, Santi, Erin), (Raffi, Erin, Santi), (Erin, Raffi, Marley), (Santi, Raffi, Marley)
if __name__ == "__main__":
	spreadsheet_id="1cXR2-jds_mFykHLvTU06eV07wGmjSmGLthkzo94k5Nc"
	spreadsheet_range="Form Responses 1"
	data = get_data(spreadsheet_id, spreadsheet_range, cols=[1,2,3,4,5])