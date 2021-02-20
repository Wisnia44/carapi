# CarApi web app
### Rest API to create, read and delete info about cars and their ratings
#### Realisation of recrutation task *Netguru.PythonWebDeveloper*. Task described in task.txt

**Using instruction:**
The project is hosted on heroku at *https://protected-savannah-45082.herokuapp.com*.

Api documentation build with *drf-yasg* is accesible at that address.

**Using instruction (local version):**
1. Clone the repository with `$git clone https://github.com/Wisnia44/carapi.git`;
2. Build docker images and run containers `$docker-compose up --build`;
3. Server is up and running at *http://0.0.0.0:8000/* !
4. Api documentation build with *drf-yasg* is accesible at *http://0.0.0.0:8000/redoc/*;
5. To test provided entpoints use *docker exec -it carapi_django_1 python manage.py test*.
