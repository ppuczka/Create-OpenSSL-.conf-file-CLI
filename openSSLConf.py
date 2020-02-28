import argparse
import configparser
import sys
from pyfiglet import Figlet


class DistinguishedName:

    # Describe the Subject (ie the origanisation).
    # The first 6 below could be shortened to: C ST L O OU CN
    # The short names are what are shown when the certificate is displayed.
    # Eg the details below would be shown as:
    # Subject: C=UK, ST=Hertfordshire, L=My Town, O=Some Organisation,
    # OU=Some Department, CN=www.example.com/emailAddress=bofh@example.com

    def __init__(self):
        
        self.countryName = input(f"provide value for countryName ")
        self.stateOrProvinceName = input(f"provide value for stateOrProvinceName ")
        self.localityName = input(f"provide value for localityName ")
        self.organizationName = input(f"provide value for organizationName ")
        self.organizationalUnitName = input(f"provide value for organizationalUnitName ")
        self.emailAddress = input(f"provide value for emailAddress " )
        self.commonName = input(f"provide value for commonName ")
        self.dns = input(f"provide value for dns ")
        self.ip = input(f"provide value for ip ")
        
    def create_config_file(self):
        file_name = input("Provide filename: ")

        file_creator = configparser.ConfigParser()
        file_creator.add_section('crt')
        file_creator.set('crt', 'default_bits', '2048')
        file_creator.set('crt', 'prompt', 'no')
        file_creator.set('crt', 'default_md', 'sha256')
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

        with open(f"{file_name}.conf", "w") as conf:
            file_creator.write(conf)

    def __str__(self):
        return  'Entered values:\n' + ', '.join(['{key} = {value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__]) 


class Certificate:

    def __init__(self):
        self.default_bits = '2048'
        self.prompt = 'no'
        self.default_md = 'sha256'
        self.req_extensions ='req_ext'
        self.distinguished_name = 'dn'

    def __str__(self):
        return 'Entered values:\n' + ', '.join(['{key} = {value}'.
                                                format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


def main():

    parser = argparse.ArgumentParser(description='Create openSSL config files with one command')
    parser.add_argument('-v', '--version', action = 'version', version = '1.0.0')
    parser.add_argument('-c', '--create', dest = 'create_file', action = 'store_true', help = "creates openSSL config file")
    args = parser.parse_args()

    if args.create_file:
        figlet = Figlet(font='slant')
        print(figlet.renderText('OpenSSL Config'))
        user_input = ""
        while user_input.capitalize() != "Y":
            new_file = DistinguishedName()
            print(new_file)
            user_input = input("Is this correct Y/N ? ")
        new_file.create_config_file()


if __name__=="__main__":
    main()