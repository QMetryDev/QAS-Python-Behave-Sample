from abc import ABC, abstractmethod


class DriverListener(ABC):
    @abstractmethod
    def before_command(self, driver, command_tracker):
        pass

    @abstractmethod
    def after_command(self, driver, command_tracker):
        pass

    @abstractmethod
    def on_exception(self, driver, command_tracker):
        pass


class ElementListener:
    @abstractmethod
    def before_command(self, element, command_tracker):
        pass

    @abstractmethod
    def after_command(self, element, command_tracker):
        pass

    @abstractmethod
    def on_exception(self, element, command_tracker):
        pass
