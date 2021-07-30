from restfly.endpoint import APIEndpoint
from pyzscaler.utils import snake_to_camel
from box import BoxList


class SSLInspectionAPI(APIEndpoint):
    def get_csr(self):
        return self._get("sslSettings/downloadcsr", box=False).text

    def get_intermediate_ca(self):
        return self._get("sslSettings/showcert")

    def generate_csr(
            self,
            cert_name: str,
            cn: str,
            org: str,
            dept: str,
            city: str,
            state: str,
            country: str,
            signature: str,
    ):
        payload = {
            "certName": cert_name,
            "commName": cn,
            "orgName": org,
            "deptName": dept,
            "city": city,
            "state": state,
            "country": country,
            "signatureAlgorithm": signature,
        }

        return self._post("sslSettings/generatecsr", json=payload)

    def upload_int_cert(self, cert: str):
        payload = {}

        return self._post("sslSettings/uploadcert/text", files=payload)

    def upload_int_chain(self, cert: str):
        payload = {}

        return self._post("sslSettings/uploadcertchain/text", files=payload)

    def delete_int_chain(self):
        return self._delete("sslSettings/certchain")
