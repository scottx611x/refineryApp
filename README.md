# refineryApp
###A Flask-driven Web App by Scott Ouellette
####Tested within Ubuntu 14.10 & OSX 10.10.3

##Minimum Requirements
####Python 2.7.8
####pip 1.5.6
####git 2.1.0
####python virtualenv module 13.1.0

##Install instructions
####pip install virtualenv
####git clone git@github.com:scottx611x/refineryApp.git
####cd refineryApp
####virtualenv venv
####. venv/bin/activate
####pip install -r requirements.txt

##Running the App
####While in the root directory execute: "python run.py"
####This will startup a server instance

####The web app will be locally accessible from your browser at: http://127.0.0.1:5000/refineryApp

####Click on Categories and Workflows to bring up a web form for editing!

##Valid URL examples:
###View all existing workflows
####http://127.0.0.1:5000/refineryApp/workflows/
###Edit the Category where id == 1
####http://127.0.0.1:5000/refineryApp/categories/1 
###Create a new Workflow
####http://127.0.0.1:5000/refineryApp/workflows/new 
###Delete the Category where id == 2
####http://127.0.0.1:5000/refineryApp/categories/delete/2 



