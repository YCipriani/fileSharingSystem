from filesharing.domains.base_model_ import Model


class Request(Model):
    def __init__(
        self,
        request_type,
        file_name_and_extension,
        file_location,
        time=None,
        number_of_checks=None,
    ):
        self.request_type = request_type
        self.file_name_and_extension = file_name_and_extension
        self.file_location = file_location
        self.time = time
        self.number_of_checks = number_of_checks
