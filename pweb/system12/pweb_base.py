import os
from flask import Flask


class PWebBase(Flask):

    def is_app_loaded(self):
        if not self.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            return True
        return False
