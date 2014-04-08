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

import ipy_alerts
import os
import pytest

class TestIPyAlerts(object):

    def teardown_method(self, method):
        os.unsetenv('IPY_ALERTS_FROM_PASSWORD') # for test_setting_env_var

    def test_setting_env_var(self):
        ipy_alerts_class = ipy_alerts.AlertsMagic()
        test_from_password = 'test_password'

        os.environ['IPY_ALERTS_FROM_PASSWORD'] = test_from_password

        from_password = (
            ipy_alerts_class._gather_email_requirements('from_password'))

        assert from_password == test_from_password

    def test_config_file(self, tmpdir):
        ipy_alerts_class = ipy_alerts.AlertsMagic()
        test_from_password = 'test_password'

        f = tmpdir.mkdir("subdir").join("ipy_alerts.cfg")

        f.write("[ipy_alerts]\nfrom_password:{}".format(test_from_password))

        test_file = os.path.join(tmpdir.strpath, 'subdir', 'ipy_alerts.cfg')

        from_password = (
            ipy_alerts_class._gather_email_requirements('from_password',
                                                        test_file))

        assert from_password == test_from_password

    def test_ipython_config(self):
        # need to add testing for this, not sure how to get IPython obj
        # in the test
        pass

    def test_none_variable(self):
        """Throw an error if a variable isn't set after attempting to
        set everything."""
        ipy_alerts_class = ipy_alerts.AlertsMagic()

        test_line = "-e thauck@zulily.com"

        with pytest.raises(ValueError):
            ipy_alerts_class.ipy_alerts(test_line, "")

    def test_order_of_operations(self, tmpdir):
        """Make sure that if the config file is set, as well as the env var,
        that the config file isn't blown out."""

        config_password = 'config_password'
        env_password = 'env_password'
        expected_password = 'config_password'

        ipy_alerts_class = ipy_alerts.AlertsMagic()
        f = tmpdir.mkdir("subdir").join("ipy_alerts.cfg")
        f.write("[ipy_alerts]\nfrom_password:{}".format(config_password))
        test_file = os.path.join(tmpdir.strpath, 'subdir', 'ipy_alerts.cfg')

        os.environ['IPY_ALERTS_FROM_PASSWORD'] = env_password

        from_password = (
            ipy_alerts_class._gather_email_requirements('from_password',
                                                        test_file))
