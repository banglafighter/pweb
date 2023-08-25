import os
import typing as t
from pweb.system12.pweb_base import PWebBase
from pweb.system12.pweb_app_config import PWebAppConfig
from pweb.system12.pweb_starter import PWebStarter


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

    def run(self):
        self._pweb_app.run(host=self._config.HOST, port=self._config.PORT, load_dotenv=False)
