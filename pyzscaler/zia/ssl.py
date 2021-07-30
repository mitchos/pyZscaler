from restfly.endpoint import APIEndpoint


class SSLInspectionAPI(APIEndpoint):
    def get_csr(self):
        """
        Downloads a CSR after it has been generated.

        Returns:
            :obj:`str`: Base64 encoded PKCS#10 CSR text.

        Examples:
            Retrieve the CSR for use in another function.

            >>> csr = zia.ssl.get_csr()

        """
        return self._get("sslSettings/downloadcsr", box=False).text

    def get_intermediate_ca(self):
        """
        Returns information on the signed Intermediate Root CA certificate.

        Returns:
            :obj:`dict`: The Intermediate Root CA resource record.

        Examples:
            >>> pprint(zia.ssl.get_intermediate_ca())

        """
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
        """
        Generates a Certificate Signing Request.

        Args:
            cert_name (str): Certificate Name
            cn (str): Common Name
            org (str): Organisation
            dept (str): Department
            city (str): City
            state (str): State
            country (str): Country. Must be in the two-letter country code (ISO 3166-1 alpha-2) format and prefixed by
                `COUNTRY`. E.g.::

                    United States = US = COUNTRY_US
                    Australia = AU = COUNTRY_AU

            signature  (str): Certificate signature algorithm. Accepted values are `SHA_1` and `SHA_256`.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            >>> zia.ssl.generate_csr(cert_name='Example.com Intermediate CA 2',
            ...    cn='Example.com Intermediate CA 2',
            ...    org='Example.com',
            ...    dept='IT',
            ...    city='Sydney',
            ...    state='NSW',
            ...    country='COUNTRY_AU',
            ...    signature='SHA_256')

        """
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

        return self._post(
            "sslSettings/generatecsr", json=payload, box=False
        ).status_code

    def upload_int_ca_cert(self, cert):
        """
        Uploads a signed Intermediate Root CA certificate.

        Args:
            cert (tuple): The Intermediate Root CA certificate tuple in the following format, where `int_ca_pem` is a
                ``File Object`` representation of the Intermediate Root CA certificate PEM file::

                ('filename.pem', int_ca_pem)

        Returns:
            :obj:`str`: The status code for the operation.

        Examples:
            Upload an Intermediate Root CA certificate from a file:

            >>> zia.ssl.upload_int_ca_cert(('int_ca.pem', open('int_ca.pem', 'rb')))

        """

        payload = {"fileUpload": cert}

        return self._post(
            "sslSettings/uploadcert/text", files=payload, box=False
        ).status_code

    def upload_int_ca_chain(self, cert: tuple):
        """
        Uploads the Intermediate Root CA certificate chain.

        Args:
            cert (tuple): The Intermediate Root CA chain certificate tuple in the following format, where
                `int_ca_chain_pem` is a ``File Object`` representation of the Intermediate Root CA certificate chain
                PEM file::

                ('filename.pem', int_ca_chain_pem)


        Returns:
            :obj:`str`: The status code for the operation

        Examples:
            Upload an Intermediate Root CA chain from a file:

            >>> zia.ssl.upload_int_ca_chain(('int_ca_chain.pem', open('int_ca_chain.pem', 'rb')))

        """

        payload = {"fileUpload": cert}

        return self._post(
            "sslSettings/uploadcertchain/text", files=payload, box=False
        ).status_code

    def delete_int_chain(self):
        """
        Deletes the Intermediate Root CA certificate chain.

        Returns:
            :obj:`str`: The status code for the operation.

        """
        return self._delete("sslSettings/certchain", box=False).status_code
