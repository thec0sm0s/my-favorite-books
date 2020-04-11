# Application configs.
DEBUG = True

SECRET_KEY = b'\x83\xe9\x8aZKfv-{/\xad\x0c0IO\x80'
JWT_SECRET_KEY = b' \xe62;l\x8a\x8cB\x12\x98\x90\x89t\xd5\xe2;'

# PostgreSQL configs.
DB_USER = "postgres"
DB_PASSWORD = "7777"
DATABASE = "books"

# JWT configs.
JWT_TOKEN_EXPIRES_IN = 24 * 60 * 60    # Specify seconds after which the JWT token expires.
