import logging
from pyspedas.mms.mms_config import CONFIG


# the following decorator prints the loaded tplot variables after each load routine call
def print_vars(func):
    def wrapper(*args, **kwargs):
        variables = func(*args, **kwargs)
        if variables is None:
            return None
        if kwargs.get('available') or CONFIG['download_only']:
            logging.info('Available files:')
        else:
            logging.info('Loaded variables:')
        for var in variables:
            logging.info(var)
        return variables
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
