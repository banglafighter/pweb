from abc import ABC, abstractmethod


class PWebModuleRegister(ABC):

    @abstractmethod
    def get_module_list(self) -> list:
        pass


class PWebComponentRegister(ABC):

    @abstractmethod
    def register_model(self, pweb_db) -> list:
        pass

    @abstractmethod
    def register_controller(self, pweb_app):
        pass

    @abstractmethod
    def run_on_start(self, pweb_app):
        pass

    def run_on_cli_init(self, pweb_app):
        pass
