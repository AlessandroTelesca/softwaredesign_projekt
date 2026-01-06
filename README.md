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

### Python Virtual Environment
Get Python virtual environment and install dependencies.  
Install dependencies: `pip install -r requirements.txt`  
Add new module dependencies: `pip freeze > requirements.txt`  

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
#### /api/robot/read
`/api/robot/read` _/ GET_ gets a specified robot by its ID.
```
robot_id: int
```

#### /api/robot/update/<int::robot_id>
TODO

#### /api/robot/delete
`/api/robot/delete` _/ POST_ deletes a specified robot by its ID.
```
robot_id: int
```

### Packages
To handle packages, there must at least be one robot in the simulation.  
Packages are assigned to a robot; any robot can have a maximum of eight packages (two large, eight small).  
Start defaults to Karlsruhe Hauptbahnhof; destination to Karlsruhe Durlach Bahnhof.
#### /api/pkg/create
`/api/pkg/create` _/ POST_ creates a new package and assigns it to a robot with a given ID.  
```
robot_id: int
start: str
destination: str
size: PackageSize[SMALL, LARGE]
```

### Simulation
Simulation (number of robots, packages, etc.) is tracked within runtime code. 
#### /api/sim/reset
`/api/sim/reset` _/ POST_ resets the simulation; removes all robots and packages.
#### /api/sim/time  
`/api/sim/time` _/ GET_ checks the current datetime within the simulation. This isn't necessarily the current real time.  
#### /api/sim/heartbeat TODO
`/api/sim/heartbeat` _/ GET_ is a heartbeat monitor; tracks new happenings since the last heartbeat call.
   

## Frontend
### Install

- From the repository root, install frontend dependencies by running:

```powershell
cd frontend; npm install
```

### Start

- Start the backend (run `app.py` from the `backend` folder):

```powershell
cd backend; python app.py
```

- Start the frontend (from the `frontend` folder):

```powershell
cd frontend; npm start
```

- After the frontend starts a browser will open itself with to tabs.
    if not: open your browser at `http://localhost:4200/map` and `http://localhost:4200/robot`.

### Notes

- Ensure the backend is running and its URL is configured in `src/app/env.ts` if needed.
- If `npm start` is not defined, `npm run start` or `ng serve` can be used instead.
Start web app inside frontend/. `ng serve --open --port 8080`

## Sources
[Build a CRUD App with Python, Flask, and Angular](https://developer.okta.com/blog/2019/03/25/build-crud-app-with-python-flask-angular)  
[Open Street Map using OSMNX: how to retrieve the Hannover subway network?](https://stackoverflow.com/questions/62067243/open-street-map-using-osmnx-how-to-retrieve-the-hannover-subway-network)  
[GeoJSON](https://geojson.io/#map=9.2/48.9302/8.5221)  
[How To Structure a Large Flask Application-Best Practices for 2025](https://dev.to/gajanan0707/how-to-structure-a-large-flask-application-best-practices-for-2025-9j2)  
[Flask HTTP methods, handle GET & POST requests](https://www.geeksforgeeks.org/python/flask-http-methods-handle-get-post-requests/)