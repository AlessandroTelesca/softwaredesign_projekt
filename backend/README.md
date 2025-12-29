# Backend

Python with Flask.  
All API/middleware goes into the api/ directory.  

### Structure
```
backend/
├── api
│   ├── debug.py
│   ├── map.py
│   ├── pkg.py
│   ├── robot.py
│   └── sim.py
├── app.py
├── db
│   ├── KVV_Haltestellen_v2.json
│   ├── KVVLinesGeoJSON_v2.json
│   ├── KVV_Lines_v2.json
│   └── KVV_Transit_Information.json
├── emoji
│   ├── *.png
├── geography.py
├── icons
│   ├── *.png
├── __init__.py
├── packages.py
├── README.md
├── robot.py
├── route_animation.py
├── simulation.py
└── test.py
```
app.py: Main Flask app.  
geography.py: Map generation and handling.  
robot.py: Handles singular robots and their creation.  
route_animation.py: Handles the animations for the routing.  
simulation.py: Handles the Simulation singleton instance.  
test.py: Creating test cases for the backend.
