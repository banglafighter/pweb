from typing import Optional
from pweb.system12.pweb_base import PWebBase
from pweb.system12.pweb_app_config import PWebAppConfig
from pweb.system12.pweb_interfaces import PWebModuleRegister
from pweb.system12.pweb_interfaces import PWebComponentRegister
from ppy_common import PyCommon, PPyCException


class PWebModuleManager:
    _pweb_app: PWebBase
    _config: PWebAppConfig = None

    def init_app(self, pweb_app, config: PWebAppConfig):
        self._config = config
        self._pweb_app = pweb_app
        self._register_modules()

    def run_module_cli_init(self, config, pweb_app):
        module_registry_packages = config.MODULE_REGISTRY_PACKAGE
        if module_registry_packages and isinstance(module_registry_packages, list):
            for module_registry_package in module_registry_packages:
                modules = self._get_modules(module_registry_package, config)
                if modules:
                    with pweb_app.app_context():
                        list_of_module = modules.get_module_list()
                        if not list_of_module:
                            return
                        for module in list_of_module:
                            if issubclass(module, PWebComponentRegister):
                                instance = module()
                                if hasattr(instance, "run_on_cli_init"):
                                    instance.run_on_cli_init(pweb_app)

    def _register_modules(self):
        module_registry_packages = self._config.MODULE_REGISTRY_PACKAGE
        if module_registry_packages and isinstance(module_registry_packages, list):
            for module_registry_package in module_registry_packages:
                modules = self._get_modules(module_registry_package, self._config)
                if modules:
                    with self._pweb_app.app_context():
                        list_of_module = modules.get_module_list()
                        if not list_of_module:
                            return

                        # Register Model First
                        for module in list_of_module:
                            if issubclass(module, PWebComponentRegister):
                                instance = module()
                                # instance.register_model(pweb_db) # TODO: Init Module Later

                        # After Model Registration Run Other Init
                        for module in list_of_module:
                            if issubclass(module, PWebComponentRegister):
                                instance = module()
                                instance.register_controller(self._pweb_app)
                                instance.run_on_start(self._pweb_app)

    def _get_modules(self, module_registry_package, config) -> Optional[PWebModuleRegister]:
        app_config = PyCommon.import_from_string(module_registry_package, config.STRING_IMPORT_SILENT)
        if app_config:
            if not issubclass(app_config, PWebModuleRegister):
                raise PPyCException("Register Should be Implementation of PWebModuleRegister")
            return app_config()
        return None
