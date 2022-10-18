from restfly.endpoint import APIEndpoint


class AppsAPI(APIEndpoint):
    def get_apps(self):
        return self._get("apps")
