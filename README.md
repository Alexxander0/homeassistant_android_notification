# homeassistant_android_notification
Homeassistant notification app for android



Setup App for Android:
------------------------

Requirements:
1) firebase.google.com account
2) android studio program

Steps:
1) Setup firebase.google.com account for Cloud Messaging
2) Download google-services.json
3) Insert your google-services.json into the sourcecode of the app
4) Compile and upload to your smartphone

Setup Service for HA:
------------------------

Requirements:
1) google python api

Steps:
1) install pyopenssl, oauth2client, google-api-python-client
2) copy notify.py into custom_components
3) notify.py: enter your project id in PROJECT_ID = 'XXXXXXXXXXXX' 
4) notify.py: enter the path to your service-account.json in PATH_SERVICE_ACCOUNT 
4) restart HA

