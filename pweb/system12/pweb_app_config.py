import os
from ppy_jsonyml import YAMLConfigObj
from pweb_orm import PWebSaaSTenantResolver


class PWebAppConfig(YAMLConfigObj):
    APP_NAME: str = "PWeb"
    PORT: int = 1200
    HOST: str = "127.0.0.1"

    BASE_DIR: str = None
    APP_CONFIG_PATH: str = None
    DEBUG: bool = True
    SECRET_KEY: str = 'random_secret_key_base'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = None
    SQLALCHEMY_ECHO: bool = False

    # Resource Management
    TEMP_DIR: str = None
    INTERNAL_DATA_DIR: str = None
    UPLOADED_STATIC_RESOURCES: str = None
    UPLOADED_STATIC_RESOURCES_URL: str = "/assets"

    STRING_IMPORT_SILENT: bool = False
    APPLICATION_CONFIGURATION: str = "application.config.app_config.Config"
    APPLICATION_MODULE_REGISTRY: str = "application.config.module_registry.Register"

    # CORS
    REST_URL_START_WITH = "api"
    ALLOW_CORS_ORIGINS: list = ["*"]
    ALLOW_ACCESS_CONTROL_ORIGIN: str = "*"

    # SaaS
    TENANT_RESOLVER: PWebSaaSTenantResolver = None

    def set_base_dir(self, path):
        if not self.BASE_DIR:
            self.BASE_DIR = path
            self.APP_CONFIG_PATH = path
            if not self.SQLALCHEMY_DATABASE_URI:
                self.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(self.BASE_DIR, 'pweb.sqlite3')
        if not self.UPLOADED_STATIC_RESOURCES:
            self.UPLOADED_STATIC_RESOURCES = os.path.join(self.BASE_DIR, "uploaded-resources")
        if not self.TEMP_DIR:
            self.TEMP_DIR = os.path.join(self.BASE_DIR, "pweb-temp")
        if not self.INTERNAL_DATA_DIR:
            self.INTERNAL_DATA_DIR = os.path.join(self.BASE_DIR, "pweb-internal")
        return self
