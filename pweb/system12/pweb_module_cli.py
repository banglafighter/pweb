from flask.cli import AppGroup, with_appcontext
from pweb.system12.pweb_module_manager import PWebModuleManager

pweb_module_cli = AppGroup("module", help="PWeb Module CLI System")
_pweb_app = None
_pweb_config = None


@pweb_module_cli.command("init", help="Initialize module CLI init")
@with_appcontext
def run_init_module_cli():
    pweb_module_manager = PWebModuleManager()
    pweb_module_manager.run_module_cli_init(_pweb_config, _pweb_app)


def init_pweb_module_cli(pweb, config):
    global _pweb_app
    global _pweb_config
    _pweb_app = pweb
    _pweb_config = config
    if pweb:
        pweb.cli.add_command(pweb_module_cli)
