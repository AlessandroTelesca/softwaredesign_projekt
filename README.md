# Software Design Project


## Config
Create a Python Virtual Environment using Python >=3.12.  
Use the recommended extensions from `.vscode/extensions.json` if you use VSCode.  

  
## Backend 
Uses Flask with OSMnx and sqlite.  
Serves API end points for Angular frontend. Generates an interactive map of Karlsruhe.  
Run: `flask --app backend/app.py run`  
Debug Mode: `flask --app backend/app.py run --debug`  
Open: http://127.0.0.1:5000  
Debug mode enables on-the-fly changes to the app as well as additional logging statements through Flask.logger.info(). 

## Middleware API
The API is called through either POST, or GET requests.  
Below is a documentation of the possible interactions with the frontend.

### Debug / Testing
`/api/hello` _/ GET_ checks if connection with backend exists and API is online.  
`/api/string/<text>` _/ GET_ same as /api/hello, but returns the string given to it.

### Robots
Robots can easily be created through API requests; they are assigned an ID. It is possible to get their current status.  
TODO Update robot info, add them to maps
#### /api/robot/create
`/api/robot/create` _/ POST_ creates a new robot.
```
is_parked: bool
is_door_opened: bool
is_reversing: bool
is_charging: bool

battery_status: float
message: str
led_rgb: tuple[int, int, int]
packages: list[Package]
```
Returns the status of the robot as well as its ID.  
#### /api/robot/read/<int::robot_id>
`/api/robot/read/<int:robot_id>` _/ GET_ gets a specified robot by its ID.

#### /api/robot/update/<int::robot_id>
TODO

#### /api/robot/delete/<int::robot_id>
`/api/robot/delete/<int:robot_id>` _/ POST_ deletes a specified robot by its ID.

### Packages
TODO

### Simulation
Simulation (number of robots, packages, etc.) is tracked within runtime code. 
#### /api/sim/reset
`/api/robot/delete/<int::robot_id>` _/ POST_ resets the simulation; removes all robots and packages.
   
## Python Virtual Environment
Get Python virtual environment and install dependencies.  
Install dependencies: `pip install -r requirements.txt`  
Add new module dependencies: `pip freeze > requirements.txt`  

## Frontend
TODO: DOC  
Start web app inside frontend/. `ng serve --open --port 8080`

## Sources
[Build a CRUD App with Python, Flask, and Angular](https://developer.okta.com/blog/2019/03/25/build-crud-app-with-python-flask-angular)  
[Open Street Map using OSMNX: how to retrieve the Hannover subway network?](https://stackoverflow.com/questions/62067243/open-street-map-using-osmnx-how-to-retrieve-the-hannover-subway-network)  
[GeoJSON](https://geojson.io/#map=9.2/48.9302/8.5221)

