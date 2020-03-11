import argparse
import os

from pyfiglet import Figlet

from clasess.Certificate import Certificate
from clasess.CertificateProperties import CertificateProperties
from clasess.Csr import Csr

SOFTWARE_NAME = 'OpenSSL Certificate Creator'
SOFTWARE_VERSION = '1.0.0'
current_path = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser(description='Create openSSL config files, certificates and keys with one command')

    parser.add_argument('--create-config', '-c', dest='create_config_file', action='store_true',
                        help='creates openSSL config file at current folder')

    parser.add_argument('--create-csr', '-s', dest='create_csr', action='store_true',
                        help='creates private key and certificate signing request')

    parser.add_argument('-p', '--path', default=current_path, required=False,
                        help='enter path to store file either current path will be used')

    parser.add_argument('-f', '--file', default=None, required=False,
                        help='enter path to openSSL config file')

    parser.add_argument('-v', '--version', action='version', version=SOFTWARE_VERSION)

    args = parser.parse_args()
    destination_folder_path = args.path
    config_file_path = args.file

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

        openssl_config_file.create_config_file(destination_folder_path, certificate_properties, SOFTWARE_NAME, SOFTWARE_VERSION)
    # TODO: file path configuration
    if args.create_csr:
        figlet = Figlet(font='slant')
        print(figlet.renderText(SOFTWARE_NAME))
        try:
            if config_file_path is None:
                config_file_path = input('Warning file path to config file not present.\nEnter config file path: ')

            config_file_dir = os.path.dirname(config_file_path)
            csr_creator = Csr.from_config_file(config_file_path)
            print(f"Config file loaded successfully")
            print(config_file_dir)
            csr_creator.create_csr(config_file_dir)

        except KeyError:
            print("Error while loading file please verify path and file name ")


if __name__ == "__main__":
    main()
