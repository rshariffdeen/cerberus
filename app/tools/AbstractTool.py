import abc


class AbstractTool:
    @abc.abstractmethod
    def create_docker_image(self, input):
        """Method documentation"""
        return

    @abc.abstractmethod
    def create_docker_container(self, input):
        """Method documentation"""
        return


    @abc.abstractmethod
    def instrument(self, input):
        """Method documentation"""
        return

    @abc.abstractmethod
    def repair(self, input):
        """Method documentation"""
        return

    @abc.abstractmethod
    def preprocess(self, input):
        """Method documentation"""
        return

    @abc.abstractmethod
    def postprocess(self, input):
        """Method documentation"""
        return

    @abc.abstractmethod
    def archive(self, input):
        """Method documentation"""
        return

