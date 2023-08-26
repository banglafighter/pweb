import os
import typing as t
from ppy_jsonyml import YAMLConfigLoader
from pweb.system12.pweb_registry import PWebRegistry
from pweb.system12.pweb_base import PWebBase
from pweb.system12.pweb_app_config import PWebAppConfig
from pweb.system12.pweb_starter import PWebStarter
from ppy_common import PyCommon


class PWebBismillah(object):
    _pweb_app: PWebBase
    _config: PWebAppConfig = None
    _bootstrap: PWebStarter = PWebStarter()

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
        self._process_resource_path(root_path=project_root_path)
        self._init_config()

    def run(self):
        self._pweb_app.run(host=self._config.HOST, port=self._config.PORT, load_dotenv=False, debug=self._config.DEBUG)

    def _process_resource_path(self, root_path):
        root_dir = os.path.dirname(os.path.abspath(root_path))
        self._config.set_base_dir(root_dir)

    def _init_config(self):
        self._merge_config()
        PWebRegistry.config = self._config

    def _merge_config(self):
        yaml_env = YAMLConfigLoader()
        confi_class = PyCommon.import_from_string(self._config.APPLICATION_CONFIGURATION, self._config.STRING_IMPORT_SILENT)
        if confi_class:
            config_map = dir(confi_class)
            for key in config_map:
                if key.isupper() and hasattr(self._config, key):
                    setattr(self._config, key, getattr(confi_class, key))

        self._config = yaml_env.load(project_root_path=self._config.APP_CONFIG_PATH, config_obj=self._config)

        if confi_class:
            yaml_env.merge_config(confi_class)
