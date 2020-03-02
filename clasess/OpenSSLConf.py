import configparser
import sys
import re

from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate_request, dump_privatekey, PKey, TYPE_RSA, X509Req)


class OpenSSLConfig:

    # Describe the Subject (ie. the organisation).
    # The first 6 below could be shortened to: C ST L O OU CN
    # The short names are what are shown when the certificate is displayed.
    # Eg the details below would be shown as:
    # Subject: C=UK, ST=Hertfordshire, L=My Town, O=Some Organisation,
    # OU=Some Department, CN=www.example.com/emailAddress=bofh@example.com

    def __init__(self, from_config_file=False):

        if from_config_file:
            config_file_reader = configparser.ConfigParser()
            conf_file_path = input('enter config file path: ')

            with open(f'{conf_file_path}', 'r') as config_file:
                config_param_dict = config_file_reader.read_dict(config_file)
            print(config_param_dict)
        else:
            self.countryName = input(f"provide value for countryName ")
            self.stateOrProvinceName = input(f"provide value for stateOrProvinceName ")
            self.localityName = input(f"provide value for localityName ")
            self.organizationName = input(f"provide value for organizationName ")
            self.organizationalUnitName = input(f"provide value for organizationalUnitName ")
            self.emailAddress = self.validate_email()
            self.commonName = input(f"provide value for commonName ")
            self.dns = input(f"provide value for dns ")
            self.ip = self.validate_ip()

    def create_config_file(self, certificate_properties, software_name, software_version):
        end_file_comment = f'#Created with {software_name} version: {software_version}'

        file_creator = configparser.ConfigParser()
        file_name = input("Provide filename: ")

        file_creator.add_section('crt')
        file_creator.set('crt', 'default_bits',  certificate_properties.default_bits)
        file_creator.set('crt', 'prompt', certificate_properties.prompt)
        file_creator.set('crt', 'default_md', certificate_properties.default_md)
        file_creator.set('crt', 'req_extensions', 'req_ext')
        file_creator.set('crt', 'distinguished_name', 'dn')

        file_creator.add_section('dn')
        file_creator.set('dn', 'C', self.countryName)
        file_creator.set('dn', 'ST', self.stateOrProvinceName)
        file_creator.set('dn', 'L', self.stateOrProvinceName)
        file_creator.set('dn', 'O', self.organizationalUnitName)
        file_creator.set('dn', 'OU', self.organizationalUnitName)
        file_creator.set('dn', 'emailAddress', self.emailAddress)
        file_creator.set('dn', 'CN', self.commonName)
        file_creator.add_section('req_ext')
        file_creator.set('req_ext', 'subjectAltName', '@alt_names')
        file_creator.add_section('alt_names')
        file_creator.set('alt_names', 'DNS.1', self.dns)
        file_creator.set('alt_names', 'IP.1', self.ip)
        file_creator.write(sys.stdout)

        with open(f'{file_name}.conf', 'a') as conf:
            file_creator.write(conf)

        with open(f'{file_name}.conf', 'a') as conf:
            conf.write(end_file_comment)

    @staticmethod
    def create_csr(conf_file_path):

        config_file_reader = configparser.ConfigParser()

        with open(f'{conf_file_path}', 'r') as config_file:
            config_param_dict = config_file_reader.read_dict(config_file)
        print(config_param_dict)

        # private_key_path = re.sub(r".(pem|crt)$", ".key", cert_file_path, flags=re.IGNORECASE)
        #
        # # create public/private key
        # key = PKey()
        # key.generate_key(TYPE_RSA, 2048)
        #
        # # Generate CSR
        # req = X509Req()
        # req.get_subject().CN = 'localhost'
        # req.get_subject().O = 'XYZ Widgets Inc'
        # req.get_subject().OU = 'IT Department'
        # req.get_subject().L = 'Seattle'
        # req.get_subject().ST = 'Washington'
        # req.get_subject().C = 'US'
        # req.get_subject().emailAddress = 'e@example.com'
        # req.set_pubkey(key)
        # req.sign(key, 'sha256')
        #
        # with open(csr_file_path, 'wb+') as f:
        #     f.write(dump_certificate_request(FILETYPE_PEM, req))
        # with open(private_key_path, 'wb+') as f:
        #     f.write(dump_privatekey(FILETYPE_PEM, key))

    @staticmethod
    def validate_ip():
        ip_regex = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        entered_ip = input("provide value for ip ")
        if ip_regex.match(entered_ip):
            return entered_ip
        else:
            entered_ip = input('entered IP is not valid, please provide correct IP: ')
            return entered_ip

    @staticmethod
    def validate_email():
        email_regex = re.compile("/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\."
                                 "[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/igm")
        entered_email = input(f"provide value for emailAddress ")
        if email_regex.match(entered_email):
            return entered_email
        else:
            entered_ip = input('entered email is not valid, please provide correct email: ')
            return entered_ip

    def __str__(self):
        return 'Entered values:\n' + ', '.join(['{key} = {value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

