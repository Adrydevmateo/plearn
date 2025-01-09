from decouple import config

# JWT Configuration
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = str(config("ALGORITHM", default="HS256"))
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)
