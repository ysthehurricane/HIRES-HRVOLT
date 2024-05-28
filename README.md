There are mainly two folders:

- hrvolt : Backend Django API
- recruiter_side_hrvolt : Fronted React Project

## Setup & Installation of hrvolt (Backend Django API)

#### Prerequisites:

- Install Python : 3.9.0 >= 3.11.0
- Postgres Database : version 14
- Pgadmin 4 : https://www.pgadmin.org/download/ 


#### Step 1: Clone the repository:

git clone https://github.com/yourusername/yourproject.git
cd hrvolt

#### Step 2: Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

#### Step 3: Install the dependencies:

pip install -r requirements.txt

#### Step 4: Create a empty database in postgre with the name "hrvolt_new_database"

#### Step 5: Configure settings.py ( hrvolt/hrvolt/settings.py)

- Change your postgres password


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hrvolt_new_database',
        'USER': 'postgres',
        'PASSWORD': 'xxxxxx',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#### Step 6: Apply the database migratw:

python manage.py makemigrations

 
#### Step 7: After run above command, apply migrations:  

python manage.py migrate
  

#### Step 8: Start the development server:

python manage.py runserver


#### Step 9: Open your browser and navigate to:

http://127.0.0.1:8000/
