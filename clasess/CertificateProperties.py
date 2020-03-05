from __future__ import print_function, unicode_literals

import configparser

from PyInquirer import prompt
from examples import custom_style_2


class CertificateProperties:

    def __init__(self, default_bits, prompt_type, default_md, req_extensions, distinguished_name):
        self.default_bits = default_bits
        self.prompt = prompt_type
        self.default_md = default_md
        self.req_extensions = req_extensions
        self.distinguished_name = distinguished_name

    @classmethod
    def from_default_properties(cls):
        default_bits = '1024'
        prompt_type = 'no'
        default_md = 'SHA256'
        req_extensions = 'req_ext'
        distinguished_name = 'dn'

        return cls(default_bits, prompt_type, default_md, req_extensions, distinguished_name)

    @classmethod
    def from_user_input(cls):
        questions = [
            {
                'type': 'list',
                'name': 'bits',
                'message': 'Set bits, default = 2048',
                'choices': ['512', '1024', '2048', '4096']
            },
            {
                'type': 'list',
                'name': 'prompt',
                'message': 'Set prompt, default = No',
                'choices': ['Yes', 'No'],
            },
            {
                'type': 'list',
                'name': 'message digest',
                'message': 'Set message digest, default = SHA256',
                'choices': ['SHA', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512', 'Other']
            }
        ]

        user_config = prompt(questions, style=custom_style_2)

        default_bits = user_config.get('bits')
        prompt_type = user_config.get('prompt')
        default_md = user_config.get('message digest')
        req_extensions = 'req_ext'
        distinguished_name = 'dn'

        return cls(default_bits, prompt_type, default_md, req_extensions, distinguished_name)

    @classmethod
    def from_config_file(cls, conf_file_path):
        config_file_reader = configparser.ConfigParser()
        config_file_reader.read(conf_file_path)

        default_bits = config_file_reader['crt']['default_bits']
        prompt_type = config_file_reader['crt']['prompt']
        default_md = config_file_reader['crt']['default_md']
        req_extensions = config_file_reader['crt']['req_extensions']
        distinguished_name = config_file_reader['crt']['distinguished_name']

        return cls(default_bits, prompt_type, default_md, req_extensions, distinguished_name)

    def __str__(self):
        return 'Entered values:\n' + ', '.join(['{key} = {value}'.
                                               format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])
