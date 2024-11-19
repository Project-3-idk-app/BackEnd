# CST438Proj3-BackEnd

## First Steps 

Creating the environment for the code and donloading dependencies

```
python -m venv idkEnv
.\idkEnv\Scripts\activate
pip install -r requirements.txt
```
copy your ```.env``` file into the root directory

## Running the code

To run the API, you run this code on the root directory
```
python .\manage.py runserver
```
If you make any modifications to the the code make sure to run migrations.  (This will also show any errors)

```
python .\manage.py makemigrations
python .\manage.py migrate
```