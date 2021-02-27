# Covid RiteAid Checker

## Disclaimer

Don't use this tool, it hits an open endpoint and may cause delays for people who are trying to get a vaccine. 
This is truly for educational purposes only as it's not very helpful. 
If you were to use it, as you cannot sign up through it. 
By the time you are notified that there is an appointment, and you jump through the hoops, the spot is likely taken. 
Your best bet is to keep the page open and click each link one at a time.

If this script **was** helpful I'd make it an AWS Lambda function that ran every few minutes.

**IF YOU ARE A PROJECT MANAGER AT RITEAID NOTE**

It would have been much more helpful for you to streamline your flow:

1) Fill out the eligability form
2) Enter a zipcode
3) They should you the locations available, and timeslot
4) Select the timeslot and continue

How it is now is barely usable.

## To get started

- `create virutalenv in .venv and install requirements`

If you want it to send you emails: (only runs on loop)

- `export GMAIL_UN=youremail@gmail.com`
- `export GMAIL_PW=YOURPASSWORD`

TO run:

- `.venv/bin/python3 ./main.py ZIPCODE`

Or if you want it to loop:

- `.venv/bin/python3 ./main.py ZIPCODE loop=True`
