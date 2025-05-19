# CS-499: Enhancement One
[![🐍  Python-tests](https://github.com/chris3024/CS_499_Enhancement_1/actions/workflows/python-tests.yml/badge.svg)](https://github.com/chris3024/CS_499_Enhancement_1/actions/workflows/python-tests.yml)
![pylint](https://img.shields.io/badge/PyLint-9.92-yellow?logo=python&logoColor=white)
[![CodeQL Advanced](https://github.com/chris3024/CS_499_Enhancement_1/actions/workflows/codeql.yml/badge.svg)](https://github.com/chris3024/CS_499_Enhancement_1/actions/workflows/codeql.yml)
___
This codebase holds the enhanced application from IT-145: Foundation in Application Development. In this improved codebase, we have added persistent data storage using JSON I/O. I have also implemented
a GUI to make the application more user-friendly.

<img src="Screenshot 2025-05-18 125114.png" alt="New GUI for application" width="436" height="252"/>
<img src="Screenshot 2025-05-18 125121.png" alt="New GUI for application" width="436" height="252"/>
___
## Installation Instructions

1. Clone the repository to the local machine
    ```bash
    git clone https://github.com/chris3024/CS_499_Enhancement_1.git
    cd CS_499_Enhancement_1
    ```
2. Set up and activate the virtual environment

   Linux/macOS
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   Windows (Command Prompt)
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
   Windows (Powershell)
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
3. Install requirements for the project
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application
   ```bash
   python main.py
   ```
