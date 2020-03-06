import argparse

from pyfiglet import Figlet

from clasess.Certificate import Certificate
from clasess.CertificateProperties import CertificateProperties
from clasess.Csr import Csr

SOFTWARE_NAME = 'OpenSSL Config Creator'
SOFTWARE_VERSION = '1.0.0'


def main():

    parser = argparse.ArgumentParser(description='Create openSSL config files with one command')
    parser.add_argument('-v', '--version', action='version', version=SOFTWARE_VERSION)
    parser.add_argument('-c', '--create', dest='create_config_file', action='store_true', help='creates openSSL config file')
    parser.add_argument('-k', '--key', dest='create_csr', action='store_true', help='creates CSR')

    args = parser.parse_args()
    file_path = '/Users/ppuczka/Desktop/Projects_v2/py_cli/test3.conf'

    if args.create_config_file:
        figlet = Figlet(font='slant')
        print(figlet.renderText(SOFTWARE_NAME))
        user_input = ""
        certificate_properties = CertificateProperties.from_default_properties()
        while user_input.capitalize() != "Y":
            print(certificate_properties)
            user_input = input("Is this correct Y/N ? ")
            if user_input.capitalize() == "N":
                certificate_properties.from_user_input()

        user_input = ""
        while user_input.capitalize() != "Y":
            openssl_config_file = Certificate.from_user_input()

            print(openssl_config_file)
            user_input = input("Is this correct Y/N ? ")

        openssl_config_file.create_config_file(certificate_properties, SOFTWARE_NAME, SOFTWARE_VERSION)

    if args.create_csr:
        figlet = Figlet(font='slant')
        print(figlet.renderText(SOFTWARE_NAME))
        try:
            csr_creator = Csr.from_config_file(file_path)

        except KeyError:
            print("Error: no such file in path, please provide correct path")


if __name__ == "__main__":
    main()
