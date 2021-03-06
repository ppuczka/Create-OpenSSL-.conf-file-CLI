import configparser
import sys
import re


class Certificate:

    # Describe the Subject (ie. the organisation).
    # The first 6 below could be shortened to: C ST L O OU CN
    # The short names are what are shown when the certificate is displayed.
    # Eg the details below would be shown as:
    # Subject: C=UK, ST=Hertfordshire, L=My Town, O=Some Organisation,
    # OU=Some Department, CN=www.example.com/emailAddress=bofh@example.com

    def __init__(self, country_name, state_or_province_name, locality_name, organization_name, organizational_unit_name,
                 email_address, common_name, dns, ip):
        self.country_name = country_name
        self.state_or_province_name = state_or_province_name
        self.locality_name = locality_name
        self.organization_name = organization_name
        self.organizational_unit_name = organizational_unit_name
        self.email_address = email_address
        self.common_name = common_name
        self.dns = dns
        self.ip = ip

    @staticmethod
    def validate_ip():
        ip_regex = re.compile(
            "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
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

    @classmethod
    def from_config_file(cls, conf_file_path):
        config_file_reader = configparser.ConfigParser()
        config_file_reader.read(conf_file_path)

        country_name = config_file_reader['dn']['C']
        state_or_province_name = config_file_reader['dn']['ST']
        locality_name = config_file_reader['dn']['L']
        organization_name = config_file_reader['dn']['O']
        organizational_unit_name = config_file_reader['dn']['OU']
        email_address = config_file_reader['dn']['emailaddress']
        common_name = config_file_reader['dn']['CN']
        dns = config_file_reader['alt_names']['dns.1']
        ip = config_file_reader['alt_names']['ip.1']

        return cls(country_name, state_or_province_name, locality_name, organization_name, organizational_unit_name,
                   email_address, common_name, dns, ip)

    @classmethod
    def from_user_input(cls):
        country_name = input(f"provide value for countryName ")
        state_or_province_name = input(f"provide value for stateOrProvinceName ")
        locality_name = input(f"provide value for localityName ")
        organization_name = input(f"provide value for organizationName ")
        organizational_unit_name = input(f"provide value for organizationalUnitName ")
        email_address = cls.validate_email()
        common_name = input(f"provide value for commonName ")
        dns = input(f"provide value for dns ")
        ip = cls.validate_ip()

        return cls(country_name, state_or_province_name, locality_name, organization_name, organizational_unit_name,
                   email_address, common_name, dns, ip)

    def create_config_file(self, destination_folder_path, certificate_properties, software_name, software_version):
        end_file_comment = f'#Created with {software_name} version: {software_version}'

        file_creator = configparser.ConfigParser()
        file_name = input("Provide filename: ")

        file_creator.add_section('crt')
        file_creator.set('crt', 'default_bits', certificate_properties.default_bits)
        file_creator.set('crt', 'prompt', certificate_properties.prompt)
        file_creator.set('crt', 'default_md', certificate_properties.default_md)
        file_creator.set('crt', 'req_extensions', 'req_ext')
        file_creator.set('crt', 'distinguished_name', 'dn')

        file_creator.add_section('dn')
        file_creator.set('dn', 'C', self.country_name)
        file_creator.set('dn', 'ST', self.state_or_province_name)
        file_creator.set('dn', 'L', self.state_or_province_name)
        file_creator.set('dn', 'O', self.organizational_unit_name)
        file_creator.set('dn', 'OU', self.organizational_unit_name)
        file_creator.set('dn', 'emailAddress', self.email_address)
        file_creator.set('dn', 'CN', self.common_name)
        file_creator.add_section('req_ext')
        file_creator.set('req_ext', 'subjectAltName', '@alt_names')
        file_creator.add_section('alt_names')
        file_creator.set('alt_names', 'DNS.1', self.dns)
        file_creator.set('alt_names', 'IP.1', self.ip)
        file_creator.write(sys.stdout)

        with open(f'{destination_folder_path}/{file_name}.conf', 'a') as conf:
            file_creator.write(conf)

        with open(f'{destination_folder_path}/{file_name}.conf', 'a') as conf:
            conf.write(end_file_comment)

        print(f'{conf.name} file created successfully')

    def __str__(self):
        return 'Entered values:\n' + ', '.join(
            ['{key} = {value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])
