import cdflib
from pytplot import get_data
import logging

def get_gatt_ror(downloadonly, loaded_data):
    """Get global attributes from a downloaded CDF file or loaded tplot variable, in order to print rules of the road"""
    try:
        if isinstance(loaded_data, list):
            if downloadonly:
                cdf_file = cdflib.CDF(loaded_data[-1])
                gatt = cdf_file.globalattsget()
            else:
                md = get_data(loaded_data[-1], metadata=True)
                if type(md) is not dict:
                    # If the last variable doesn't work, try the first variable
                    md = get_data(loaded_data[0], metadata=True)
                gatt = md['CDF']['GATT']
        elif isinstance(loaded_data, dict):
            gatt = loaded_data[list(loaded_data.keys())[-1]]['CDF']['GATT']
        return gatt
    except:
        logging.warning('Retrieving PI info and rules of the road failed')
        # Return a dictionary containing all the fields the various load routines are looking for
        return {'PI_name':'Error_retrieving',
                "PI_NAME":"Error_retrieving",
                'PI_affiliation':'Error_retrieving',
                "PI_AFFILIATION":"Error_retrieving",
                'LINK':'Error_retrieving',
                "TEXT":["Error_retrieving"],
                "LINK_TEXT":"Error_retriving",
                "HTTP_LINK":"Error_retrieving",
                "Rules_of_use":"Error_retrieving",
                "Logical_source_description":"Error_retrieving",
                "LOGICAL_SOURCE_DESCRIPTION":"Error_retrieving",
                "Station_code":"Error_retrieving"
                }
