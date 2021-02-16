# People Matcher
Form groups of k people that maximizes everyone's preferences subject to scheduling contraints. Solves the problem using [linear programming](https://en.wikipedia.org/wiki/Linear_programming).

Example Google Sheets to collect responses <a href="https://docs.google.com/spreadsheets/d/1OcAamihKvVBg3OZt_p4A6hxoeO1OEtTrZ6iT7CSLqDI" target="_blank">https://docs.google.com/spreadsheets/d/1OcAamihKvVBg3OZt_p4A6hxoeO1OEtTrZ6iT7CSLqDI</a>

## Getting Started
1. Clone this repository: `git clone https://github.com/rhotter/people-matcher.git`
2. Run `pip install -r requirements.txt`
3. In the `.env` file, change SPREADSHEET_ID to your own spreadsheet ID from your google sheets (the spreadsheet ID can be found in the URL of your google sheets. It comes after `/d/`. For example, in the Google Sheets link above, the spreadsheet ID would be `1OcAamihKvVBg3OZt_p4A6hxoeO1OEtTrZ6iT7CSLqDI`
4. Run `python teaching.py` for the teaching solver or `python collaboration.py` for the collaboration solver.

------

Experimental things on `devy` branch
