# ipy_alerts

> An IPython extension that implements a cell magic which will send
an email when the cell has finished running.

### Installation

_(from within IPython)_

```
%install_ext https://raw.github.com/zulily/ipy_alerts/master/ipy_alerts.py
```

### Usage

```
%load_ext ipy_alerts
%%ipy_alerts -e to@example.com -s "hey there" -b "email body!" -f from@example.com -p pa$$w0rd

import time
time.sleep(1)
```

An email will be sent after the cell has completed, here after a 1 second pause.

### Parameters

* `--to_email`, `-e`: the email recipient
* `--subject`, `-s`: the email subject
* `--body`, `-b`: the email body
* `--from_email`, `-f`: the email sender
* `--from_password`, `-p`: the password of the email sender account
* `--email_config`, `-c`: the location of a config file to check for the above
parameters

All parameters (except `email_config`) must be eventually set in order for the email to be sent.
The __Configuration__ section below describes the various options for configuring ipy_alerts without
explicitly passing the values at execution time.

### Configuration

Instead of passing all required parameters at execution time, ipy_alerts has 3 different methods
for configuring parameters.  If desired, a combination of methods can be used, and ipy_alerts will
use the following precedence order to determine the configuration parameters:

  * parameters passed at execution time **(highest precedence)**
  * explicit config file
  * environment variables
  * IPython config **(lowest precedence)**

At this time, the email client is assumed to be gmail and cannot be modified via parameters.  Modifying the code
to use a different email client should be straightforward.

#### 1. Explicit Config File

As mentioned above, it's possible to setup a config file which contains some/all of
the config parameters.  This file should be readable by `ConfigParser` and have a section
titled `ipy_alerts`.

Example:

```
[ipy_alerts]
from_password:mypass
from_email:alerts@example.com
subject:Your model just finished.
to_email:example@example.com
```

This file path can be specified with the `--email_config`, `-c` option, and defaults to
`~/.ipy_alerts.ini`

Example execution: `%ipy_alerts -b "Model XYZ just finished" -c ~/.ipy_alerts.ini`.

#### 2. Environment Variables

ipy_alerts will look for environment variables using the naming convention
`IPY_ALERTS_<PARAMETER>`.

Example: `export IPY_ALERTS_FROM_EMAIL=from@example.com`

#### 3. IPython Config

ipy_alerts will look in your current IPython config, in a section called `ipy_alerts` for config
parameters.

Example:

```
c.ipy_alerts = {'from_password': 'mypassword', 'from_email': 'alerts@example.com'}
```
