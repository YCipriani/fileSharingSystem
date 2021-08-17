from filesharing.domains.base_model_ import Model


class Request(Model):
    def __init__(
        self, file_name_and_extension, file_location, time=None, number_of_checks=None
    ):
        self.file_name = file_name_and_extension
        self.file_location = file_location
        self.time = time
        self.number_of_checks = number_of_checks
