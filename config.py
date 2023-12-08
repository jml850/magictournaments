SECRET_KEY = 'MAGICTOURNAMENTS'

class Config:
    DEBUG = False  # Modo depuración (False en producción)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # URL de la base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evitar seguimiento de modificaciones

class DevelopmentConfig(Config):
    DEBUG = True  # Habilita el modo depuración en desarrollo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'  # Base de datos de desarrollo

