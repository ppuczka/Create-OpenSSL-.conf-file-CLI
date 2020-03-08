import configparser

from OpenSSL.crypto import PKey, TYPE_RSA, X509Req

from clasess.Certificate import Certificate
from clasess.CertificateProperties import CertificateProperties


class Csr (Certificate, CertificateProperties):

    def __init__(self, country_name, state_or_province_name, locality_name, organization_name, organizational_unit_name,
                 email_address, common_name, dns, ip, default_bits, prompt_type, default_md, req_extensions,
                 distinguished_name):

        Certificate.__init__(self, country_name, state_or_province_name, locality_name, organization_name,
                             organizational_unit_name, email_address, common_name, dns, ip)
        CertificateProperties.__init__(self, default_bits, prompt_type, default_md, req_extensions, distinguished_name)

    @classmethod
    def from_config_file(cls, conf_file_path):
        config_file_reader = configparser.ConfigParser()
        config_file_reader.read(conf_file_path)

        default_bits = config_file_reader['crt']['default_bits']
        prompt_type = config_file_reader['crt']['prompt']
        default_md = config_file_reader['crt']['default_md']
        req_extensions = config_file_reader['crt']['req_extensions']
        distinguished_name = config_file_reader['crt']['distinguished_name']

        country_name = config_file_reader['dn']['C']
        state_or_province_name = config_file_reader['dn']['ST']
        locality_name = config_file_reader['dn']['L']
        organization_name = config_file_reader['dn']['O']
        organizational_unit_name = config_file_reader['dn']['OU']
        email_address = config_file_reader['dn']['emailaddress']
        common_name = config_file_reader['dn']['CN']
        dns = config_file_reader['alt_names']['dns.1']
        ip = config_file_reader['alt_names']['ip.1']

        return cls(default_bits, prompt_type, default_md, req_extensions, distinguished_name,
                   country_name, state_or_province_name, locality_name, organization_name,
                   organizational_unit_name, email_address, common_name, dns, ip)

    @staticmethod
    def create_csr(self):

        # create public/private key
        key = PKey()
        key.generate_key(TYPE_RSA, object)

        # Generate CSR
        req = X509Req()
        req.get_subject().CN = object.cn
        req.get_subject().O = 'XYZ Widgets Inc'
        req.get_subject().OU = 'IT Department'
        req.get_subject().L = 'Seattle'
        req.get_subject().ST = 'Washington'
        req.get_subject().C = 'US'
        req.get_subject().emailAddress = 'e@example.com'
        req.set_pubkey(key)
        req.sign(key, 'sha256')

        with open(certificate_file_path, 'wb+') as f:
            f.write(dump_certificate_request(OpenSSL.SSL.FILETYPE_PEM, req))

        with open(private_key_path, 'wb+') as f:
            f.write(dump_privatekey(OpenSSL.SSL.FILETYPE_PEM, key))