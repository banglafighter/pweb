from typing import Optional
from pweb.system12.pweb_base import PWebBase
from pweb.system12.pweb_app_config import PWebAppConfig
from pweb.system12.pweb_interfaces import PWebModuleRegister
from pweb.system12.pweb_interfaces import PWebComponentRegister
from ppy_common import PyCommon, PPyCException
from pweb.system12.pweb_registry import PWebRegistry


class PWebModuleManager:
    _pweb_app: PWebBase
    _config: PWebAppConfig = None
    _pweb_orm = None

    def init_app(self, pweb_app, config: PWebAppConfig, pweb_orm):
        self._config = config
        self._pweb_app = pweb_app
        self._pweb_orm = pweb_orm
        self._register_modules()

    def run_module_cli_init(self, config, pweb_app):
        modules = self._get_application_module_registry(config=config)
        if modules:
            self._call_run_module_cli_init(list_of_module=modules.get_module_list(), config=config, pweb_app=pweb_app)

    def add_module_to_pweb_registry(self, list_of_module):
        for module in list_of_module:
            if issubclass(module, PWebComponentRegister):
                instance = module()
                if instance and instance.app_details():
                    app_details = instance.app_details()
                    if app_details.systemName not in PWebRegistry.registerModules:
                        PWebRegistry.registerModules[app_details.systemName] = app_details

    def _call_run_module_cli_init(self, list_of_module, config, pweb_app):
        with pweb_app.app_context():
            if not list_of_module:
                return

            self.add_module_to_pweb_registry(list_of_module=list_of_module)

            # Run CLI Init
            for module in list_of_module:
                if issubclass(module, PWebComponentRegister):
                    instance = module()
                    if hasattr(instance, "run_on_cli_init"):
                        instance.run_on_cli_init(pweb_app, config)

    def _register_module_list(self, list_of_module):
        with self._pweb_app.app_context():
            if not list_of_module:
                return

            self.add_module_to_pweb_registry(list_of_module=list_of_module)

            # Register Model First
            for module in list_of_module:
                if issubclass(module, PWebComponentRegister):
                    instance = module()
                    instance.register_model(self._pweb_orm)

            # After Model Registration Run Other Init
            for module in list_of_module:
                if issubclass(module, PWebComponentRegister):
                    instance = module()
                    instance.register_controller(self._pweb_app)
                    instance.run_on_start(self._pweb_app, self._config)

    def _register_modules(self):
        modules = self._get_application_module_registry()
        if modules:
            self._register_module_list(list_of_module=modules.get_module_list())

    def _get_application_module_registry(self, config=None) -> Optional[PWebModuleRegister]:
        if not config:
            config = self._config

        app_config = PyCommon.import_from_string(config.APPLICATION_MODULE_REGISTRY, config.STRING_IMPORT_SILENT)
        if app_config:
            if not issubclass(app_config, PWebModuleRegister):
                raise PPyCException("Register Should be Implementation of PWebModuleRegister")
            return app_config()
        return None
