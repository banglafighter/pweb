from flask.cli import AppGroup, with_appcontext
from pweb.system12.pweb_module_manager import PWebModuleManager

pweb_module_cli = AppGroup("module", help="PWeb Module CLI System")
_cli_pweb_app = None
_cli_pweb_config = None


@pweb_module_cli.command("init", help="Initialize module CLI init")
@with_appcontext
def run_init_module_cli():
    pweb_module_manager = PWebModuleManager()
    pweb_module_manager.run_module_cli_init(_cli_pweb_config, _cli_pweb_app)


def init_pweb_module_cli(pweb, config):
    global _cli_pweb_app
    global _cli_pweb_config
    _cli_pweb_app = pweb
    _cli_pweb_config = config
    if pweb:
        pweb.cli.add_command(pweb_module_cli)
