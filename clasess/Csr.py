import configparser

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

from clasess.Certificate import Certificate
from clasess.CertificateProperties import CertificateProperties


class Csr(Certificate, CertificateProperties):

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

        return cls(country_name, state_or_province_name, locality_name, organization_name,
                   organizational_unit_name, email_address, common_name, dns, ip,
                   default_bits, prompt_type, default_md, req_extensions, distinguished_name)

    def create_csr(self, path):
        private_key = rsa.generate_private_key(public_exponent=6553, key_size=int(self.default_bits),
                                               backend=default_backend())

        with open(f"{path}/{self.common_name}_key.pem", "wb") as f:
            f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                              format=serialization.PrivateFormat.TraditionalOpenSSL,
                                              encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase")
                                              ))
        print(f'{f.name} file created successfully')

        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.state_or_province_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, self.locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name),
        ])).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(self.dns),
                x509.DNSName(self.dns),
                x509.DNSName(self.ip),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256(), default_backend())

        with open(f"{path}/{self.common_name}_csr.pem", "wb") as f:
            f.write(csr.public_bytes(serialization.Encoding.PEM))

        print(f'{f.name} file created successfully')
