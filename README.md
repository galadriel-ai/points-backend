# Points backend


## Development setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Setup database
```bash
cd database
docker-compose up --build -d
alembic upgrade head
```

**Other relevant database operations**
```bash
# Generate a migration (CHECK THE GENERATED FILE)
alembic revision --autogenerate -m "Description"
# Downgrade by 1 (can modify number)
alembic downgrade -1
```


### Run unit tests
```bash
python -m pytest tests/unit
```
