# weather-apirest

### Arquitectura
La aplicacion es basicamente un procesador de mensajes, tiene 2 entrypoints:
* FastApi(REST): La llamada Post para crear un viaje es procesada primero por la capa http de fast api, haciendo validaciones de los tipos de datos que se reciben,Se crea un commando y este se pasa al Bus de Mensajes quien hace el mapeo correspondiente y manda llamar el handler correcto. Si el bus de Mensajes ejecuto correctamente el commando lanza un evento `TravelCreated` el cual es enviado hacia Redis. Para que los microservicios que esten interesados puedan manejar esta informacion.

* Bus de Mensajes: Es simplemente un Bus de Mensajes que esta subscrito a ciertos canales de redis, cuando llega un nuevo mensaje lo procesa.

Se trato de implementar una arquitectura enfocada en Event Driven Design(microservicios) con el enfoque de que los test sean lo mas facil posible, sean rapidos y claros.

Estructura:
Basicamente existen 3 capas importantes en la aplicacion:
* Dominio:
* Service Layer: Son todos los casos de usos de nuestra aplicacion, aqui estan los handlers donde cada handler es un caso de uso, aqui se hace toda la orquestacion del nuestro dominio, cada handler es transaccionalmente atomico, si falla alguna operacion se hacer rollback lo cual garantiza el estado correcto de la aplicacion.
* Adapters(Puerto/adaptador): Todas las dependencias que hemos definido como plugeables, idealmente deberia de existir una interfaz(Puerto) para cada Adaptador implementado.

### Run local server
Configuration of the environment.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e src/
```
Run api server
```bash
uvicorn src.travels.entrypoints.fast_api:app --reload
```
#### Run event consumer server
```bash
python src/travels/entrypoints/redis_eventconsumer.py
```

Install Redis and send this json event on the chanel create_travel
```json
{"id": "123456789", "user_id": "ba89d055a1074b49bb918cae57831747", "origin": "C. Izcalli", "destination": "cdmx", "datetime_departure": "2021-08-10T18:00:00", "datetime_arrival":  "2021-08-11T05:00:00"}
```


### Database configuration
For manage the migrations we use alembic :)
First we need to create the database
```bash
sqlite3 database.db
(sqlite)>>>
```
1.- alembic init --template generic travels/adapters/orm/alembic
2.- On alembic.ini file set the path to the url `sqlalchemy.url = sqlite:///database.db`
3.- Generate the initial migrations
3.1.- on env.py import the schemas
`from travels.adapters.orm import schemas`
3.2 Set the below variable
`target_metadata = schemas.mapper_registry.metadata`
```bash
alembic revision --autogenerate -m "init"
```
3.3.- Run the migrations
```bash
alembic upgrade head
```

### Run tests
Los test se dividen en 3 tipos:
* unit: Estos estan enfocados en los modelos y handlers, para el caso de los handlers se hacen los test inyectando clases Fakes, esto mejora la velocidad de ejecucion(no se tiene que acceder a la db), y se prueba la logica de los handlers unicamente.
* Integracion: Culquier dependencia que pueda ser sustituida por alguna otra implementacion manteniendo la misma interfaz es considerado como de integracion, todos estos se encuentran en la carpeta adapters.
* E2E: Estos test son sobre los dos entrypoints que tiene la aplicacion -> FastApi y Redis events. En estos test unicamente hacemos clases Fakes sobre las dependencias externas.(por ejemplo el cliente del pronostico del clima)

```bash
pytest tests/
pytest tests/unit
pytest tests/integration
pytest tests/e2e
```

### Referencias:
* La mayoria de los conceptos son tomados de https://github.com/cosmicpython


