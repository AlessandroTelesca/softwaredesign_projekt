# Software Design Project


## Config
Create a Python Virtual Environment using Python >=3.12.  
Use the recommended extensions from `.vscode/extensions.json` if you use VSCode.  

  
## Backend 
Uses Flask with OSMnx and sqlite.  
Serves API end points for Angular frontend. Generates an interactive map of Karlsruhe.  
Run: `--app backend/app.py run`  
Debug Mode: `flask --app backend/app.py run --debug`  
Open: http://127.0.0.1:5000  
Debug mode enables on-the-fly changes to the app as well as additional logging statements through Flask.logger.info().  
   
### Python Virtual Environment
Get Python virtual environment and install dependencies.  
Install dependencies: `pip install -r requirements.txt`  
Add new module dependencies: `pip freeze > requirements.txt`  

## Frontend
TODO: DOC  
Start web app inside frontend/. `ng serve --open --port 8080`

## Sources
[Build a CRUD App with Python, Flask, and Angular](https://developer.okta.com/blog/2019/03/25/build-crud-app-with-python-flask-angular)  
[Open Street Map using OSMNX: how to retrieve the Hannover subway network?](https://stackoverflow.com/questions/62067243/open-street-map-using-osmnx-how-to-retrieve-the-hannover-subway-network)  

