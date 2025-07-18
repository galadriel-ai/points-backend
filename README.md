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

### Run unit test coverage
```bash
python -m pytest tests/unit \
    --cov-report html:tests/reports/coverage/htmlcov \
    --cov-report xml:tests/reports/coverage/cobertura-coverage.xml \
    --cov-report term \
    --cov points
```

### Deployment
```bash
./deploy.sh
```


## Whitelisting users

To whitelist some twitter user, add their twitter user ID to a new line in `data/whitelist.txt` file.  
To get the ID can use some site like this: https://findidfb.com/find-twitter-id/#
(Double check profile)
