# Requirements

- pip 26
- python 3.14
- node v26
- npm 11.*

# Package Installation

In the *backend* directory, run the following commands:
```sh
python3 -m venv venv
```
```sh
source venv/bin/activate && pip install -r requirements.txt
```

Then head into the *frontend* directory and run the following command:
```sh
npm install
```

# Running the application

In the root directory, add the .vscode folder and create this launch.json file:

```json
{
    "version": "0.1.0",
    "compounds": [
        {
            "name": "Run Backend + Frontend",
            "configurations": [
                "Run Server (Uvicorn)",
                "Run Frontend"
            ]
        }
    ],
    "configurations": [
        {
            "name": "Run Server (Uvicorn)",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app", "--reload"],
            "cwd": "${workspaceFolder}/backend",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/backend"
            },
            "console": "integratedTerminal"
        },
        { 
            "name": "Run Frontend",
            "type":"node",
            "request":"launch",
            "runtimeExecutable":"npm",
            "runtimeArgs": ["run", "dev"],
            "cwd": "${workspaceFolder}/frontend",
            "console": "integratedTerminal"
        }
    ]
}
```

Then in the vscode sidebar, run the frontend and backend via the GUI. You can start the frontend and backend seperately or run them together via the "Run Backend + Frontend" Option.

Make sure you are using the right Python Interpreter (The one in the virtual environment from this project). In VS Code, press "Ctrl + Shift + P" and then type "Select Python Interpreter" in the Search Bar. Select the python interpreter located at "venv/bin/python".

 The application will then be running on http://localhost:5173/
