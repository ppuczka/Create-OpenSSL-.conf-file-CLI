import argparse
import logging
import os

from PyInquirer import prompt
from examples import custom_style_2
from pyfiglet import Figlet

from clasess.CaRestClient import CaRestClient
from clasess.Certificate import Certificate
from clasess.CertificateProperties import CertificateProperties
from clasess.Csr import Csr

SOFTWARE_NAME = 'OpenSSL Certificate Creator'
SOFTWARE_VERSION = '1.0.0'
current_path = os.path.dirname(os.path.abspath(__file__))


def user_input_parser():
    questions = [
        {
            'type': 'list',
            'name': 'user_choice',
            'message': 'What do You want to create',
            'choices': ['Create private and public key pair', 'Create private key and CSR', 'Send sign key by CA'],
        },

    ]
    answers = prompt(questions, style=custom_style_2)
    user_choice = answers.get('user_choice')
    return user_choice


def print_welcome_screen():
    figlet = Figlet(font='slant')
    print(figlet.renderText(SOFTWARE_NAME))


def main():
    parser = argparse.ArgumentParser(description='Create openSSL config files, certificates and keys with one command')

    parser.add_argument('--create-config', '-c', dest='create_config_file', action='store_true',
                        help='creates openSSL config file at current folder')

    parser.add_argument('--create', '-r', dest='create', action='store_true',
                        help='creates private key and certificate signing request')

    # parser.add_argument('--create-key-pair', dest='key_pair', action='store_true',
    #                     help='creates public and private key')

    parser.add_argument('--sign', '-s', dest='sign', action='store_true',
                        help='sign csr in provided CA')

    parser.add_argument('-p', '--path', default=current_path, required=False,
                        help='enter path to store file either current path will be used')

    parser.add_argument('-f', '--file', default=None, required=False,
                        help='enter path to openSSL config file')

    parser.add_argument('-v', '--version', action='version', version=SOFTWARE_VERSION)

    args = parser.parse_args()
    destination_folder_path = args.path
    config_file_path = args.file

    if args.create_config_file:
        print_welcome_screen()
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

        openssl_config_file.create_config_file(destination_folder_path, certificate_properties,
                                               SOFTWARE_NAME, SOFTWARE_VERSION)
    if args.create:
        print_welcome_screen()
        user_choice = user_input_parser()
        if config_file_path is None:
            config_file_path = input('Warning file path to config file not present.\nEnter config file path: ')

        config_file_dir = os.path.dirname(config_file_path)
        creator = Csr.from_config_file(config_file_path)
        print(f"Config file loaded successfully")

        try:
            if user_choice == 'Create private and public key pair':
                creator.create_key_pair(config_file_dir)
            else:
                creator.create_csr(config_file_dir)
        except KeyError:
            logging.error("Error while loading file please verify path and file name ")

    if args.sign:
        print_welcome_screen()
        pub_key_path = input('Please provide public key path: ')
        ca_server_url = input('Please provide CA server url: ')

        ca_rest_client = CaRestClient(ca_server_url)
        response = ca_rest_client.test_connection()
        print(response)


if __name__ == "__main__":
    main()

