Short instructions to install dependencies and start the application.

Install

- From the repository root, install frontend dependencies by running (PowerShell):

```powershell
cd frontend; npm install
```

Start

- Start the backend (run `app.py` from the `backend` folder). Example (PowerShell):

```powershell
cd backend; python app.py
```

- Start the frontend (from the `frontend` folder):

```powershell
cd frontend; npm start
```

- After the frontend starts a browser will open itself with to tabs.
    if not: open your browser at `http://localhost:4200/map` and `http://localhost:4200/robot`.

Notes

- Ensure the backend is running and its URL is configured in `src/app/env.ts` if needed.
- If `npm start` is not defined, `npm run start` or `ng serve` can be used instead.

If you'd like, I can also add a single PowerShell script to run backend + frontend together.