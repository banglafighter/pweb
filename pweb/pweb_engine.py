import os
import sys
from setuptools import setup
from ppy_common.ppyc_console_log import Console
from ppy_file_text import StringUtil
from pweb.system12.pweb_bismillah import PWebBismillah

env = os.environ.get('source')


class PWebEngine(PWebBismillah):
    _project_name = "PWebApp"
    version = '1.0.0'

    def __init__(self, name, project_root_path, **kwargs):
        self._project_name = name
        super().__init__(name=name, project_root_path=project_root_path, *kwargs)

    def setup_script(self):
        if self._project_name:
            name = self._project_name
            name = name.lower()
            name = StringUtil.find_and_replace_with(name, " ", "-")
            name = name.strip()
            name = f"{StringUtil.remove_special_character(name)}-pweb-system"
            setup(
                version=self.version,
                name=name,
                entry_points={'console_scripts': ['pweb=pweb_app:cli']},
                py_modules=[]
            )

    def run(self):
        cli_args = sys.argv
        if "develop" in cli_args or "install" in cli_args:
            self.setup_script()
            Console.green("Successfully Install Completed!", bold=True)
        else:
            super(PWebEngine, self).run()

    @staticmethod
    def bstart(name, project_root_path, **kwargs):
        return PWebEngine(name=name, project_root_path=project_root_path, **kwargs)
