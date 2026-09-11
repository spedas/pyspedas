from pyspedas.utilities.das2.das2ascii import das2ascii


def das2info(
    url="",
    server="",
    dataset="",
):
    """
    Request information from a DAS2 server.

    Parameters
    ----------
    url : str, optional
        DAS2 URL.
    server : str, optional
        DAS2 "server" parameter.
        Possible values:
            "list" (list available datasets),
            "peers" (list available peers),
            "dsdf" (also needs dataset, return the Data Source Definition File for a dataset)
    dataset : str, optional
        DAS2 dataset identifier to request information for.

    Returns
    -------
    str
        Response text from the DAS2 server when the request succeeds, otherwise
        an empty string.
    """
    res = ""

    if server not in ["list", "peers", "dsdf"]:
        print("Invalid server parameter. Please use one of the following: list, peers, dsdf, discover")
        return res
    if server == "dsdf" and not dataset:
        print("Dataset parameter is required when using 'dsdf' server.")
        return res

    res = das2ascii(url=url, server=server, dataset=dataset, extra="")

    return res


if __name__ == "__main__":
    # Test the das2info function.
    # https://jupiter.physics.uiowa.edu/das/server?server=dsdf&dataset=Juno/Ephemeris/Jovicentric
    url = "https://jupiter.physics.uiowa.edu/das/server"
    dataset = "Juno/Ephemeris/Jovicentric"
    info = das2info(url=url, server="dsdf", dataset=dataset)
    print(info)
