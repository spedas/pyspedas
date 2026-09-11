import logging
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)


def das2ascii(
    url="",
    server="server",
    dataset="",
    start_time="",
    end_time="",
    interval=None,
    params=None,
    extra="ascii=true",
):
    """
    Request ASCII-formatted data from a DAS2 server.

    Parameters
    ----------
    url : str, optional
        DAS2 server URL.
        For example: "https://jupiter.physics.uiowa.edu/das/server".
    server : str, optional
        DAS2 'server' identifier.
    dataset : str, optional
        DAS2 'dataset' identifier to request.
    start_time : str, optional
        Start time passed to the DAS2 'start_time' query parameter.
        Recommended format: YYYY-MM-DDTHH:MM:SS.sss
    end_time : str, optional
        End time passed to the DAS2 'end_time' query parameter.
        Recommended format: YYYY-MM-DDTHH:MM:SS.sss
    interval : int, optional
        DAS2 sampling interval passed to the 'interval' query parameter.
    params : str, optional
        Additional variables to include in the request.
    extra : str, optional
        Extra query parameters to include in the request.
        Default is an ASCII format parameter.

    Returns
    -------
    str
        Response text from the DAS2 server when the request succeeds, otherwise
        an empty string.
    """

    return_str = ""

    if not url:
        logger.error("Error: No DAS2 URL provided.")
        return return_str

    if not url.startswith("https://"):
        logger.error("Error: Invalid DAS2 URL provided. It should start with https://")
        return return_str

    def format_das2_time(time_in):
        # Fix times to DAS2 server recommended time format: YYYY-MM-DDTHH:MM:SS.sss
        if isinstance(time_in, datetime):
            time_dt = time_in
            if time_dt.tzinfo is None:
                time_dt = time_dt.replace(tzinfo=timezone.utc)
        else:
            time_text = str(time_in).strip()
            time_text = time_text.removesuffix("Z")
            time_text = time_text.replace("T", " ")
            if "." in time_text:
                time_text = time_text.split(".", 1)[0]
            if len(time_text) == 10:
                time_text = time_text + " 00:00:00"
            time_dt = datetime.strptime(time_text + "+0000", "%Y-%m-%d %H:%M:%S%z")
        return time_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    if start_time:
        start_time_str = format_das2_time(start_time)
    if end_time:
        end_time_str = format_das2_time(end_time)

    dasurl = f"{url}"
    if server:
        dasurl += f"?server={server}"
    if dataset:
        dasurl += f"&dataset={dataset}"
    if start_time:
        dasurl += f"&start_time={start_time_str}"
    if end_time:
        dasurl += f"&end_time={end_time_str}"
    if interval:
        dasurl += f"&interval={interval}"
    if params:
        dasurl += f"&params={params}"
    if extra:
        dasurl += f"&{extra}"

    try:
        logger.info(f"Requesting DAS2 data from: {dasurl}")
        response = requests.get(dasurl)
        if response.status_code == 200 and isinstance(response.text, str):
            return_str = response.text
    except requests.RequestException as e:
        logger.error(f"Error occurred while making the request: {e}")

    return return_str


if __name__ == "__main__":
    # Example usage of the das2ascii function
    # https://jupiter.physics.uiowa.edu/das/server?server=dataset&dataset=Juno%2FEphemeris%2FJovicentric&ascii=true&end_time=2020-01-01T03:00:00&interval=300&params=JLAT%20CLAT%20JULT&start_time=2020-01-01T02:00:00
    url = "https://jupiter.physics.uiowa.edu/das/server"
    dataset = "Juno/Ephemeris/Jovicentric"
    t1 = "2020-01-01 02:00:00"
    t2 = "2020-01-01 03:00:00"

    data = das2ascii(
        url=url,
        server="dataset",
        dataset=dataset,
        start_time=t1,
        end_time=t2,
        interval=300,
        params="JLAT CLAT JULT",
    )

    print(data)
