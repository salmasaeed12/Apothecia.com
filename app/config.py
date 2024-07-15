# mysql+pymysql://<stamony>:<stamony1234>@<localhost>/<Apothecia_db>
DATABASE_URL = "mysql+pymysql://stamony:stamony1234@localhost/Apothecia_db"
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 14400
