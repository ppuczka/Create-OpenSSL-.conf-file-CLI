import argparse

from pyfiglet import Figlet

from clasess.Certificate import Certificate
from clasess.OpenSSLConf import OpenSSLConfig

SOFTWARE_NAME = 'OpenSSL Config Creator'
SOFTWARE_VERSION = '1.0.0'


def main():

    parser = argparse.ArgumentParser(description='Create openSSL config files with one command')
    parser.add_argument('-v', '--version', action='version', version=SOFTWARE_VERSION)
    parser.add_argument('-c', '--create', dest='create_file', action='store_true', help='creates openSSL config file')
    parser.add_argument('-k', '--key', dest='create_csr', action='store_true', help='creates CSR')

    args = parser.parse_args()

    if args.create_file:
        figlet = Figlet(font='slant')
        print(figlet.renderText(SOFTWARE_NAME))
        user_input = ""
        certificate_properties = Certificate()

        while user_input.capitalize() != "Y":
            print(certificate_properties)
            user_input = input("Is this correct Y/N ? ")
            if user_input.capitalize() == "N":
                certificate_properties.config()

        user_input = ""
        while user_input.capitalize() != "Y":
            openssl_config_file = OpenSSLConfig()

            print(openssl_config_file)
            user_input = input("Is this correct Y/N ? ")

        openssl_config_file.create_config_file(certificate_properties, SOFTWARE_NAME, SOFTWARE_VERSION)

    if args.create_csr:
        openssl_csr = OpenSSLConfig(True)
        figlet = Figlet(font='slant')
        print(figlet.renderText(SOFTWARE_NAME))




if __name__ == "__main__":
    main()
