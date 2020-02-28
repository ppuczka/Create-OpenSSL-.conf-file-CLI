from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2


class Certificate:

    def __init__(self, default_bits='2048', prompt='no', default_md='sha256',
                 req_extensions='req_ext', distinguished_name='dn'):

        self.default_bits = default_bits
        self.prompt = prompt
        self.default_md = default_md
        self.req_extensions = req_extensions
        self.distinguished_name = distinguished_name

    def __str__(self):
        return 'Entered values:\n' + ', '.join(['{key} = {value}'.
                                                format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

    questions = [
        {
            'type': 'list',
            'name': 'bits',
            'message': 'Choose default bits',
            'choices': ['512', '1024', '2048', '4096']
        },
        {
            'type': 'list',
            'name': 'prompt',
            'message': 'Set prompt',
            'choices': ['Yes', 'No'],
        },
        {
            'type': 'list',
            'name': 'message digest',
            'message': 'Set message digest',
            'choices': ['', '']
        },
        {
            'type': 'list',
            'name': 'message digest',
            'message': 'Set message digest',
            'choices': ['', '']
        },
    ]

    answers = prompt(questions, style=custom_style_2)
    pprint(answers)




