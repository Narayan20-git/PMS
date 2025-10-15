🏗️ Project Setup Guide

Follow the steps below to set up the Property Management System (PMS) project in your local environment.

⚙️ Prerequisites

1) Git

2) Visual Studio / VS Code

3) Python 3.12.10

Setup Steps:

1️⃣ Clone the Repository

git clone https://github.com/Narayan20-git/PMS.git -b development

2️⃣ Verify Current Branch

Check if you are on the development branch

git status

3️⃣ Import Project

Open or import the project folder in Visual Studio (or VS Code).

4️⃣ Install Python

Download and install Python 3.12.10 from the official Python website
.
Ensure it’s added to your system PATH.

5️⃣ Install uv

pip install uv

uv handles virtual environments and installs packages super fast (Rust-based replacement for pip + venv).

6️⃣ Check Installed Python Versions

uv python list

This lists all Python versions installed on your system.

7️⃣ Install Specific Python Version (if missing)

uv python install ypy-3.12.10-windows-x86_64-none

Use this only if Python 3.12.10 is not already installed.

8️⃣ Create a Virtual Environment

uv venv venv

9️⃣ Activate the Virtual Environment

venv\Scripts\activate

10️⃣ Fix Permission Issue (if activation fails)

If you see an error like “running scripts is disabled on this system”, run:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

Then re-run:

venv\Scripts\activate

11️⃣ Install Dependencies

uv pip install -r requirements.txt

✅ You’re all set!
Your environment is ready. You can now run your FastAPI app with:

uv run uvicorn app.main:app --reload

