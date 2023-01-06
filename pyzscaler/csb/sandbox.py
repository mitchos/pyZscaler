from box import Box
from restfly import APISession
from restfly.endpoint import APIEndpoint


class CloudSandboxAPI(APIEndpoint):
    def submit_file(self, file: str, force: bool = False) -> Box:
        """
        Submits a file to the ZIA Advanced Cloud Sandbox for analysis.

        Args:
            file (str): The filename that will be submitted for sandbox analysis.
            force (bool): Force ZIA to analyse the file even if it has been submitted previously.

        Returns:
            :obj:`Box`: The Cloud Sandbox submission response information.

        Examples:
            Submit a file in the current directory called malware.exe to the cloud sandbox, forcing analysis.

            >>> zia.sandbox.submit_file('malware.exe', force=True)

        """
        with open(file, "rb") as f:
            data = f.read()

        params = {
            "api_token": self.sandbox_token,
            "force": int(force),  # convert boolean to int 
        }

        return self._post(params=params, data=data)
