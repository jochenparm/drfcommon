#!/usr/bin/env python
import logging
from drfcommon.choices import ComCodeChoice

LOG_PRINT_FUNC = {
    ComCodeChoice.OK: logging.debug,
    ComCodeChoice.BAD: logging.warning,
    ComCodeChoice.UNAUTHORIZED_ERR: logging.warning,
    ComCodeChoice.FORBIDDEN_ERR: logging.warning,
    ComCodeChoice.API_NOT_FUND: logging.error,
    ComCodeChoice.HTTP_405_METHOD_NOT_ALLOWED: logging.error,
    ComCodeChoice.API_ERR: logging.error,
    ComCodeChoice.DB_ERR: logging.error,
}
