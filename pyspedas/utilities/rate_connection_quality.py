def rate_connection_quality(transfer_time: float, transfer_size:float, transfer_rate:float) -> str:
    """
    Rate the connection quality in terms of the transfer size, transfer time, and transfer rate

    Parameters
    ----------
    transfer_time: float
        Elapsed time for the download, seconds
    transfer_size: float
        Amount of data transferred, megabytes
    transfer_rate: float
         Speed of the transfer, megabytes/sec

    Returns
    -------
    string
    "transfer_slow" if the connection seems slower than expected, "transfer_normal" otherwise

    """
    # We may want to add more quality tiers, but this will serve as a proof of concept
    # Don't bother rating small or very fast transfers
    if transfer_time < 2.0:
        return 'transfer_normal'
    elif transfer_rate < 1.0:
        return 'transfer_slow'
    else:
        return 'transfer_normal'