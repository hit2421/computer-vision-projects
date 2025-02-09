## Setting Up a Virtual Environment in Python

### Step 1: Check Python Installation
Ensure you have Python installed by running the following command:
```sh
python --version
```
Or for systems using `python3`:
```sh
python3 --version
```

### Step 2: Install `venv` Module (if not installed)
For Python 3.3 and above, `venv` is included by default. However, if it's missing, install it using:
```sh
pip install virtualenv
```

### Step 3: Create a Virtual Environment
Run the following command to create a virtual environment:
```sh
python -m venv env
```
Or for `python3`:
```sh
python3 -m venv env
```
This will create a folder named `myenv` in your current directory containing the virtual environment.

### Step 4: Activate the Virtual Environment
#### On Windows:
```sh
myenv\Scripts\activate
```
#### On macOS/Linux:
```sh
source myenv/bin/activate
```
Once activated, your terminal prompt should change, indicating that the virtual environment is active.

### Step 5: Install Dependencies
You can now install dependencies within the virtual environment using pip:
```sh
pip install -r requirements.txt
```

### Step 6: Deactivate the Virtual Environment
To exit the virtual environment, simply run:
```sh
deactivate
