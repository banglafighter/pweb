import os
from pweb.system12.pweb_bismillah import PWebBismillah

env = os.environ.get('source')


class PWebEngine(PWebBismillah):
    _project_name = "PWebApp"
    version = '1.0.0'

    def __init__(self, name, project_root_path, **kwargs):
        super().__init__(project_root_path=project_root_path, *kwargs)
        self._project_name = name

    def run(self):
        super(PWebEngine, self).run()

    @staticmethod
    def bstart(name, project_root_path, **kwargs):
        return PWebEngine(name=name, project_root_path=project_root_path, **kwargs)
