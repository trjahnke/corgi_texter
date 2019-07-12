# corgi_texter
[![Known Vulnerabilities](https://snyk.io//test/github/trjahnke/corgi_texter/badge.svg?targetFile=requirements.txt)](https://snyk.io//test/github/trjahnke/corgi_texter?targetFile=requirements.txt)
Corgi Texter is a two fold application. First and foremost it gives a user quick access to fun facts about corgis. By texting (612)324-8563 you will receive a text with a fun fact and source for that fact to impress your friends and family. This section uses Twilio to handle the number and routing for it. Second, is the front end of the system. It has a mostly fully fledged site which allows you to view all facts that are possible to get via the text. The site also allows users to create an account in order to submit their own facts to help grow the community. This section utilizes the Flask framework with hosting taking place at Heroku with a basic postgres database attachment.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
You will need Python3. Recommended to first start a virtualenv before moving forward.

You will also need a Twilio account along with a number. (https://www.twilio.com/docs/quickstart/python)

```sh
git clone https://github.com/trjahnke/corgi_texter.git
```

Once you have the repo to cloned to wherever you would like it install all the dependencies from the requirements.txt file
```sh
pip install -r requirements.txt
```

Now to set your secret vars. I have made a basic env file with export commands for the few vars that need to filled in. Replace my placeholders with your secrets and while in you are in your virtualenv run those export commands to make them available to the application. 


### Running
Now that those quick prereqs are done we can now start to tinker with the application itself. There is only a few more steps before we have a live testing environment.

First go into 'run.py' and change the debug flag to 'True'. 

Second, we need to create the database initially. 
Run the following to start a basic database with the models provided:
```python
python

from corgiTexter import db
db.create_all()
exit()
```

Once that is done we can start up the flask server by running 
```
python run.py
```

Now we have Corgi Texter running locally and you can mess around with it.



## ToDo
- [ ] Add automatic ping to keep the server awake
- [ ] Allow users to see post edit history
- [ ] Add column for last login
- [ ] Use and implement the is_active boolean
- [ ] Theme and color changes
- [ ] Add testing files

