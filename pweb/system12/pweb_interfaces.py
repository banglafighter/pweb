from abc import ABC, abstractmethod


class PWebModuleRegister(ABC):

    @abstractmethod
    def get_module_list(self) -> list:
        pass


class PWebModuleDetails:
    systemName: str = None  # Should be alphabet & number with - (hyphen)
    displayName: str = None

    def __init__(self, system_name: str, display_name: str = None):
        self.systemName = system_name


class PWebComponentRegister(ABC):

    @abstractmethod
    def register_model(self, pweb_db) -> list:
        pass

    @abstractmethod
    def register_controller(self, pweb_app):
        pass

    @abstractmethod
    def run_on_start(self, pweb_app, config):
        pass

    @abstractmethod
    def run_on_cli_init(self, pweb_app, config):
        pass

    @abstractmethod
    def app_details(self) -> PWebModuleDetails:
        pass
