import os

os.environ["DEBUG"] = "TRUE"

os.environ["PROJECT_NAME"] = "Metro Alarm Server (auth microservice)"

os.environ["LOGGING_PATH"] = "neverused"
os.environ["PRIVATE_KEY_PATH"] = "certs/private.pem"
os.environ["PUBLIC_KEY_PATH"] = "certs/public.pem"

os.environ["DOCS_URL"] = "neverused"
os.environ["OPENAPI_URL"] = "neverused"

os.environ["HTTP_HOST"] = "0.0.0.0"
os.environ["HTTP_PORT"] = "8081"

os.environ["DB_USER"] = "neverused"
os.environ["DB_PASS"] = "neverused"
os.environ["DB_NAME"] = "neverused"
os.environ["DB_PORT"] = "404"
os.environ["DB_HOST"] = "neverused"

os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "5"
os.environ["REFRESH_TOKEN_EXPIRE_DAYS"] = "1"
os.environ["ALGORITHM"] = "RS256"
