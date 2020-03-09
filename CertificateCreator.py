import argparse

from pyfiglet import Figlet

from clasess.Certificate import Certificate
from clasess.CertificateProperties import CertificateProperties
from clasess.Csr import Csr

SOFTWARE_NAME = 'OpenSSL Certificate Creator'
SOFTWARE_VERSION = '1.0.0'


def main():
    parser = argparse.ArgumentParser(prog='cc',
                                     description='Create openSSL config files, certificates and keys with one command')

    parser.add_argument('--create-config', dest='create_config_file', action='store_true',
                        help='creates openSSL config file')

    parser.add_argument('--create-csr', dest='create_csr', action='store_true',
                        help='creates private key and certificate signing request')

    parser.add_argument('-v', '--version', action='version', version=SOFTWARE_VERSION)

    args = parser.parse_args()
    dest_folder = 'C:\\Users\\ppuczka\\Desktop\\workshop\\py_cli\\'

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
    # TODO: file path configuration
    if args.create_csr:
        figlet = Figlet(font='slant')
        print(figlet.renderText(SOFTWARE_NAME))
        file_name = 'file1.conf'
        file_path = dest_folder + file_name
        try:
            csr_creator = Csr.from_config_file(file_path)
            csr_creator.create_csr(dest_folder)
            print(f"Config file loaded successfully")
        except KeyError:
            print("Error while loading file please verify path and file name ")


if __name__ == "__main__":
    main()
