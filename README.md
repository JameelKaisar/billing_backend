# NIT Srinagar Billing System (Backend)

## Setup the app

### Clone the repository

#### HTTPS
```bash
git clone https://github.com/JameelKaisar/billing_backend.git
```

#### SSH
```bash
git clone git@github.com:JameelKaisar/billing_backend.git
```

### Change directory to project folder
```bash
cd billing_backend
```

### Create a virtual environment
```bash
python3 -m venv venv
```

### Activate the virtual environment

#### Unix
```bash
source venv/bin/activate
```

#### Windows
```bash
venv\Scripts\activate.bat
```

### Install requirements
```bash
pip install -r requirements.txt
```

### Initialize the app
```bash
python3 init.py
```

## Deactivate the virtual environment
```bash
deactivate
```

## Run the app

### Activate the virtual environment

#### Unix
```bash
source venv/bin/activate
```

#### Windows
```bash
venv\Scripts\activate.bat
```

## Start the application
```bash
uvicorn main:app --reload
```

## Deactivate the virtual environment
```bash
deactivate
```
