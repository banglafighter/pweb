import os
import typing as t
import click
from flask import make_response, send_from_directory
from flask.cli import FlaskGroup
from flask_cors import CORS
from ppy_common.ppyc_console_log import Console
from ppy_jsonyml import YAMLConfigLoader
from pweb.system12.pweb_module_cli import init_pweb_module_cli
from pweb.system12.pweb_registry import PWebRegistry
from pweb.system12.pweb_base import PWebBase
from pweb.system12.pweb_app_config import PWebAppConfig
from ppy_common import PyCommon
from pweb.system12.pweb_module_manager import PWebModuleManager
from pweb_form_rest import PWebFR
from pweb_orm import pweb_orm, PWebSaaS


class PWebBismillah(object):
    _pweb_app: PWebBase
    _config: PWebAppConfig = None
    _application_config: PWebAppConfig = None
    _module_manager: PWebModuleManager = PWebModuleManager()

    def __init__(
            self,
            project_root_path,
            config=PWebAppConfig(),
            name: str = "PWeb",
            static_url_path: t.Optional[str] = None,
            static_folder: t.Optional[t.Union[str, os.PathLike]] = "static",
            static_host: t.Optional[str] = None,
            host_matching: bool = False,
            subdomain_matching: bool = False,
            template_folder: t.Optional[str] = "templates",
            instance_path: t.Optional[str] = None,
            instance_relative_config: bool = False,
            root_path: t.Optional[str] = None,
    ):
        self._pweb_app = PWebBase(
            name,
            static_url_path=static_url_path,
            static_folder=static_folder,
            static_host=static_host,
            host_matching=host_matching,
            subdomain_matching=subdomain_matching,
            template_folder=template_folder,
            instance_path=instance_path,
            instance_relative_config=instance_relative_config,
            root_path=root_path,
        )
        self._config = config
        self._init_config(root_path=project_root_path)
        self._init_cors()
        self._init_log_conf()
        self._copy_app_config_to_flask()
        self._init_orm()
        self._init_module_cli()
        self._module_manager.init_app(self._pweb_app, self._application_config, pweb_orm)
        self._init_form_rest_module()
        self._init_static_resource_mapping()

    def run(self):
        self._pweb_app.run(host=self._config.HOST, port=self._config.PORT, load_dotenv=False, debug=self._config.DEBUG)

    def get_app(self):
        return self._pweb_app

    def cli(self):
        Console.yellow("-------------------------")
        Console.green("   Welcome to PWeb CLI   ", True)
        Console.yellow("-------------------------")

        @click.group(cls=FlaskGroup, create_app=self.get_app)
        def invoke_cli_script():
            pass

        return invoke_cli_script()

    def _process_resource_path(self, root_path):
        root_dir = os.path.dirname(os.path.abspath(root_path))
        self._config.set_base_dir(root_dir)

    def _init_config(self, root_path):
        self._merge_config(root_path)
        PWebRegistry.config = self._config

    def _copy_app_config_to_flask(self):
        self._pweb_app.config.from_object(self._config)

    def _merge_config(self, root_path):
        yaml_env = YAMLConfigLoader()
        confi_class = PyCommon.import_from_string(self._config.APPLICATION_CONFIGURATION, self._config.STRING_IMPORT_SILENT)
        if confi_class:
            config_map = dir(confi_class)
            for key in config_map:
                if key.isupper() and hasattr(self._config, key):
                    setattr(self._config, key, getattr(confi_class, key))

        self._process_resource_path(root_path=root_path)
        self._config = yaml_env.load(project_root_path=self._config.APP_CONFIG_PATH, config_obj=self._config)

        if confi_class:
            config_map = dir(self._config)
            for key in config_map:
                if key.isupper() and hasattr(confi_class, key):
                    setattr(confi_class, key, getattr(self._config, key))
            yaml_env.merge_config(confi_class)
        self._application_config = confi_class

    def _init_cors(self):
        resources = {
            r"/" + str(self._config.REST_URL_START_WITH) + "/*": {"origins": self._config.ALLOW_CORS_ORIGINS, "Access-Control-Allow-Origin": self._config.ALLOW_ACCESS_CONTROL_ORIGIN},
            r"/static/*": {"origins": self._config.ALLOW_CORS_ORIGINS, "Access-Control-Allow-Origin": self._config.ALLOW_ACCESS_CONTROL_ORIGIN}
        }
        CORS(self._pweb_app, resources=resources)

    def _init_log_conf(self):
        Console.enable_log = self._config.DEBUG

    def _init_module_cli(self):
        init_pweb_module_cli(self._pweb_app, self._config)

    def _init_orm(self):
        PWebSaaS.tenantResolver = self._config.TENANT_RESOLVER
        pweb_orm.init_app(self._pweb_app)

    def _init_form_rest_module(self):
        form_rest = PWebFR()
        form_rest.init_app(self._pweb_app, self._application_config)

    def _init_static_resource_mapping(self):
        if self._config.UPLOADED_STATIC_RESOURCES_URL and self._config.UPLOADED_STATIC_RESOURCES_URL != "":
            url = self._config.UPLOADED_STATIC_RESOURCES_URL + "/<path:path>"
            self._pweb_app.add_url_rule(url, view_func=self.static_resource_endpoint)

    def static_resource_endpoint(self, path):
        response = make_response(send_from_directory(self._config.UPLOADED_STATIC_RESOURCES, path))
        response.headers['Access-Control-Allow-Origin'] = self._config.ALLOW_ACCESS_CONTROL_ORIGIN
        return response
