from restfly.endpoint import APIEndpoint


class AdminAPI(APIEndpoint):
    def get_departments(self):
        return self._get("administration/departments")
