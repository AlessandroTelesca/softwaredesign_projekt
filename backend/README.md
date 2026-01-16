# Backend

This directory contains the Python backend of the Software Design project.
The backend is implemented using **Flask** and provides API endpoints as well
as map and routing functionality based on OpenStreetMap data.

All API and middleware logic is located in the `api/` directory.

---

## Structure
```
backend/
├── api/
│ ├── debug.py
│ ├── map.py
│ ├── pkg.py
│ ├── robot.py
│ └── sim.py
├── app.py
├── db/
│ ├── KVV_Haltestellen_v2.json
│ ├── KVVLinesGeoJSON_v2.json
│ ├── KVV_Lines_v2.json
│ └── KVV_Transit_Information.json
├── emoji/
│ ├── *.png
├── geography.py
├── icons/
│ ├── *.png
├── __init__.py
├── packages.py
├── robot.py
├── route_animation.py
├── simulation.py
└── test.py
```
---

## Notes

- The backend is intended to be run from `app.py`.
- Map generation may require an active internet connection
  (OSMnx geocoding and data download).
- Integration of official KVV tram line data and icons
  is tracked as a TODO in the codebase.
