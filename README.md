# IS212T8 Scrum Project User Manual: Setting Up the Application

## Step 1: Clone the Repository and Open in IDE
- Clone the application repository from: https://github.com/yirenong/IS212T8
- Use git clone to clone the repo `git clone https://github.com/ong-zijian/ESD_Tour_Project.git`
- Open the cloned repository in your preferred Integrated Development Environment (IDE).

## Step 2: Set up the Database
- Start WAMP/MAMP server.
- Open PHPMyAdmin.
- Navigate to the "Import" tab.
- Upload the `is212(3).sql` file located in the database folder at the application's root directory.

## Step 3: Run the Vue.js Application
- Open a command prompt or terminal.
- Navigate to the vue folder using the `cd vue` command.
- Run `npm install` to install dependencies.
- Run `npm run serve` to start the Vue.js application.

## Step 4: Run the Flask Server
- Open another command prompt or terminal.
- Navigate to the Flask folder using the `cd Flask` command.
- Run the requirments.txt installation `py -m pip install --no-cache-dir -r requirements.txt`
- Run `python app.py` to start the Flask server.
