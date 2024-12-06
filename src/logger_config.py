"""
Module for setting up logging configuration based on the environment.

This module provides the `setup_logging` function, which configures logging settings
by loading the appropriate configuration from a logging configuration file. The
environment (such as 'dev' or 'prod') can be specified to customize the logging
output, such as log levels and handlers, based on the desired environment.

The logging configuration is read from the 'logging_config.ini' file, with the option
to set the environment dynamically, either through a provided argument or by reading
the value from an environment variable (`LOGGER_CONFIG` in the `.env` file).
"""

import logging.config
import os


def setup_logging(environment='prod'):
    """
    Configures the logging settings based on the provided environment.

    This function loads the logging configuration from a file (`logging_config.ini`) 
    and sets up logging accordingly. The configuration is customized for the 
    specified environment (e.g., 'dev' or 'prod'). The default environment is 'prod'.
    It also checks if the environment variable `LOGGER_CONFIG` is set in the `.env` file,
    and uses it if available.

    Args:
        environment (str): The environment for the logging configuration (default is 'dev').

    Returns:
        logging.Logger: The logger instance configured for the specified environment.
    """

    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    value: str = os.getenv('LOGGER_CONFIG')
    if value is not None:
        environment = value

    logging.config.fileConfig('logging_config.ini',
                              defaults={'env': environment})

    return logging.getLogger(environment)
