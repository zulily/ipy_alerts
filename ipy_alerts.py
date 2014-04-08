"""
IPython extension to alert the user via email when a cell has finished.
"""

"""
Copyright (C) 2014 zulily, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from os.path import expanduser, expandvars
import smtplib
import ConfigParser
import re

import IPython
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.core.magic import Magics, magics_class, cell_magic


@magics_class
class AlertsMagic(Magics):

    def __init__(self, *args, **kwargs):
        super(AlertsMagic, self).__init__(*args, **kwargs)

    def _send_email(self, **kwargs):
        """Send the email."""
        from_password = kwargs.pop('from_password')

        message = self._format_message(**kwargs)

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.login(kwargs['from_email'], from_password)

        session.sendmail(kwargs['from_email'], kwargs['to_email'], message)


    def _format_message(self, **kwargs):
        """Format the email according to the kwargs."""

        header = "\r\n".join(["from: {from_email}",
                              "subject: {subject}",
                              "to: {to_email}",
                              "mime-version: 1.0",
                              "content-type: text/html"]).format(**kwargs)

        return "{header} \r\n\r\n {body}".format(header=header,
                                                  body=kwargs['body'])

    def _gather_email_requirements(self, find_value, file_location=None):
        """Gets necessary information to send an email.

        Notes
        -----
        Sending an email requires:
            1. email sender account
            2. email sender password

        If these values are None, we'll work through a list of locations in an attempt to find
        suitable values:
            * explicit config file (highest precedence)
            * environment variables
            * IPython config(lowest precedence)

        See README for more details
        """

        # we'll actually update in reverse order to observe the described precedence
        value = None

        # try current IPython config
        if IPython.release.version < '1.0.0':
            ip = IPython.core.ipapi.get()
        else:
            ip = IPython.core.getipython.get_ipython()

        try:
            config = ip.config.get('ipy_alerts')
            if config:
                value = config.get(find_value)
        except:
            pass

        # try environment variables
        value = os.getenv("IPY_ALERTS_{}".format(find_value.upper()), value)

        # last chance
        file_location = expandvars(expanduser(file_location))
        if os.path.exists(file_location):
            config = ConfigParser.ConfigParser()
            config.readfp(open(file_location))
            value = config.get('ipy_alerts', find_value, value)

        return value

    def _sanitize_inputs(self, value):
        """Clean the inputs, if a multiple word parameter is passed
        then remove the leading and trailing quotes.
        """
        return re.sub(r'^"|^\'|"$|\'$', '', value)

    @magic_arguments()
    @argument('--to_email', '-e', default=None)
    @argument('--subject', '-s', default=None)
    @argument('--body', '-b', default=None)
    @argument('--from_email', '-f', default=None)
    @argument('--from_password', '-p', default=None)
    @argument('--email_config', '-c', default='~/.ipy_alerts.ini')
    @cell_magic
    def ipy_alerts(self, line, cell):
        """Implements the cell magic.

        See the README.md for examples on parameterizing the cell magic.
        """
        args = parse_argstring(self.ipy_alerts, line)
        args_dict = args.__dict__

        config_location = args_dict.pop('email_config')

        for arg_key, arg_value in args_dict.iteritems():
            if not arg_value:
                args_dict[arg_key] = self._gather_email_requirements(arg_key,
                                                                config_location)

            if not args_dict[arg_key]:
                raise ValueError("{} is None, no email will be sent."
                                 .format(arg_key))

            args_dict[arg_key] = self._sanitize_inputs(args_dict[arg_key])

        self.shell.run_cell(cell)

        self._send_email(**args_dict)


def load_ipython_extension(ipython):
    """Load the extension."""
    ipython.register_magics(AlertsMagic)

def unload_ipython_extension(ipython):
    """Unload the extension... mainly not to throw the warning when
    its unloaded.
    """
    pass
