#!/usr/bin/env python

import requests
import json
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

plans = []
response = ''

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    error = None

    if request.form:
        ticket, text = request.form.get("ticket"), request.form.get("plans")
        if text != '':
            print(text)
            if ticket == '':
                ticket_number = '*'
            else:
                ticket_number = f"<https://jira/browse/{ticket}|{ticket}>"
            plans.append({"ticket": ticket_number, "comment": text})

    return render_template("index.html", plans=plans, response=response, error=error)

@app.route('/slack', methods = ['POST', 'GET'])
def slack_post():
    error = None
    message = []
    response = ''

    for line in plans:
        message.append(f"{line.get('ticket')} - {line.get('comment')}")

    auth_token = ''
    headers = {'Authorization': 'Bearer ' + auth_token,
            'Content-type': 'application/json'}
    url = 'https://slack.com/api/chat.postMessage'
    data = {'channel': 'UM20TMCJK',
            'as_user': True,
            'text': '\n'.join(message)}

    answer = requests.post(url, data=json.dumps(data), headers=headers)
    print(answer)
    response = json.dumps(answer.json(), indent=2, sort_keys=True)
    print(response)

    return '''
<html>
  <head>
    <title>Report</title>
  </head>
  <body>
    <h3>''' + str(answer).strip("<>") + '''</h3>
    <p> ''' + response + ''' </p>
  </body>
</html>
'''

if __name__ == '__main__':
    app.run()

