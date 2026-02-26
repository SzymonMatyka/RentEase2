```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt

sudo -u postgres psql -c "CREATE USER rentease WITH PASSWORD 'postgres';"
sudo -u postgres psql -c "CREATE DATABASE rentease OWNER rentease;"
sudo -u postgres psql -d rentease -c "GRANT ALL ON SCHEMA public TO rentease;"
sudo -u postgres psql -d rentease -c "GRANT CREATE ON SCHEMA public TO rentease;"

python manage.py migrate

python manage.py runserver
```
