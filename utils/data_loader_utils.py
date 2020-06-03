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

def _get_raw_spreadsheet_data(spreadsheet_id, spreadsheet_range):
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

def _extract_person(topic_name):
	person = re.findall(r'\(.*\)', topic_name)
	person = person[0][1:-1]
	return person

def _process_raw_spreadsheet_data(values):
	data = []
	for row in values:
		data.append({
			'name': row[0],
			'out': [_extract_person(topic_name) for topic_name in row[1:]]
		})
	return data

def get_data(spreadsheet_id, spreadsheet_range):
	values = _get_raw_spreadsheet_data(spreadsheet_id, spreadsheet_range)
	data = _process_raw_spreadsheet_data(values)
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
