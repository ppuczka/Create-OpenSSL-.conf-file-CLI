import argparse
import configparser
import sys

class FileParameters:

    def __init__(self, ) 

def create_config_file():
    file_creator = configparser.ConfigParser()
    file_creator.add_section('crt')
    file_creator.set('crt', 'default_bits', '2048')
    file_creator.set('crt', 'prompt', 'no')
    file_creator.set('crt', 'default_md', 'sha256')
    file_creator.set('crt', 'req_extensions', 'req_ext')
    file_creator.set('crt', 'distinguished_name', 'dn')
    file_creator.add_section('dn')
    file_creator.set('dn', 'C', )
    file_creator.set('dn', 'ST', )
    file_creator.set('dn', 'L', )
    file_creator.set('dn', 'O', )
    file_creator.set('dn', 'OU', )
    file_creator.set('dn', 'emailAddress', 'replace with email')
    file_creator.set('dn', 'CN', )
    file_creator.add_section('req_ext')
    file_creator.set('req_ext', 'subjectAltName', '@alt_names')
    file_creator.add_section('alt_names')
    file_creator.set('alt_names', 'DNS.1', 'replace_this')
    file_creator.set('alt_names', 'DNS.2', 'replace_this')
    file_creator.set('alt_names', 'IP.1', 'replace_this')
    file_creator.write(sys.stdout)

    with open("file2.conf", "w") as conf:
        file_creator.write(conf)


parser = argparse.ArgumentParser(description='Create openSSL config files with one command')
parser.add_argument('-v', '--version', action = 'version', version = '1.0.0')
parser.add_argument('-c', '--create', dest = 'create_file', action = 'store_true', help = "creates openSSL config file")
args = parser.parse_args()

if args.create_file:

