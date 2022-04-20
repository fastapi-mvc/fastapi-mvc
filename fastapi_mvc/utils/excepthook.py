import logging
import sys
import platform
from traceback import format_exception

from fastapi_mvc.exceptions import RootException
from fastapi_mvc import __version__


log = logging.getLogger("GlobalExceptHook")
template = """Help improve fastapi-mvc :)

It does not have to be a defect immediately. But if you think this should not 
happen or it would make a nice feature, feel free to create an issue: 
{issues}

I've formated copy-paste markdown with details for you to make things easier.
However, add/edit whatever you see fit.

-----------------------------------------------------------------------------

**Describe the bug**
<!-- A clear and concise description of what the bug is. -->
```shell
{details}
```

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->

**To Reproduce**
<!-- Steps to reproduce the behavior. -->
```shell
fastapi-mvc {argv}
```

**Environment**
* Python version: `{py_ver}`
* Operating System: `{os_info}`
* fastapi-mvc version: `{version}`

**Additional context**
<!-- Add any other context about the problem here. -->

"""


def global_except_hook(exctype, value, traceback):
    if issubclass(exctype, RootException):
        if log.isEnabledFor(logging.DEBUG):
            log.exception(
                "Reason exception occurred:",
                exc_info=(exctype, value, traceback),
            )
        sys.exit(exctype.code)
    else:
        log.exception(
            "Unhandled exception occurred during RunTime.",
            exc_info=(exctype, value, traceback),
        )
        msg = template.format(
            issues="https://github.com/rszamszur/fastapi-mvc/issues/new",
            details="".join(format_exception(exctype, value, traceback)),
            argv=" ".join(sys.argv[1:]),
            py_ver=platform.python_version(),
            os_info=platform.platform(),
            version=__version__,
        )
        log.info(msg)
