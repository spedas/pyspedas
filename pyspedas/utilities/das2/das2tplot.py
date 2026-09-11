import html
import re

from pyspedas import options, store_data


def _autoplot_text(text):
    """Convert common Autoplot codes to readable plain text.

    Subscripts use underscores and superscripts use carets; font size and
    cursor positioning are not reproduced. Unknown codes remain unchanged.
    Both upper- and lowercase codes are accepted.
    """

    replacements = {
        "b": "_",
        "d": "_",  # Subscript, optionally with a smaller font.
        "a": "^",
        "e": "^",
        "u": "^",  # Superscript variants.
        "n": "",  # Return to the normal baseline.
        "c": "\n",  # Start a new line.
        "s": "",
        "r": "",  # Ignore saved/restored drawing positions.
        "!": "!",  # An escaped exclamation mark is literal text.
    }
    # Decode entities such as &alpha; and process each code once so that
    # an escaped exclamation mark cannot start another formatting command.
    return re.sub(
        r"!([abdeuncsr!])",
        lambda match: replacements[match.group(1).lower()],
        html.unescape(text),
        flags=re.IGNORECASE,
    )


def das2parse(datastr):
    """
    Parse DAS2 ASCII response text into metadata and data arrays.

    Parameters
    ----------
    datastr : str
        DAS2 ASCII response text containing stream metadata, packet variable
        definitions, and data rows.

    Returns
    -------
    tuple
        Five-element tuple containing:

        "general_dict" : dict
            Stream-level attributes and properties.
        "timearr" : list of str
            Time stamps parsed from DAS2 data rows.
        "varlist" : list of str
            Variable names parsed from packet "<y>" definitions.
        "vardict" : dict
            Variable metadata keyed by variable name.
        "vararray" : list of list of float
            Numeric data values for each variable in "varlist" order.

    """
    general_dict = {}
    timearr = []
    varlist = []
    vardict = {}
    vararray = []

    def clean_text(text):
        # Decode XML entities and remove escaping used in copied DAS2 text.
        text = html.unescape(text)
        text = text.replace("\\<", "<").replace("\\>", ">")
        text = text.replace("\\/", "/").replace("\\_", "_")
        return text

    def parse_attrs(text):
        # Extract key-value pairs from an XML element's attribute string.
        attrs = {}
        for key, value in re.findall(r'([A-Za-z_][A-Za-z0-9_:\-.]*)\s*=\s*"([^"]*)"', text):
            attrs[key.split(":")[-1]] = value
        for key in ("xLabel", "yLabel", "zLabel", "units"):
            if key in attrs:
                attrs[key] = _autoplot_text(attrs[key])
        return attrs

    def parse_properties(text):
        # Extract key-value pairs from a DAS2 <properties> element's text content.
        properties = {}
        # Merge attributes from nested properties elements into one mapping.
        for prop_match in re.finditer(r"<properties\b([^>]*)/?>", text, re.DOTALL):
            properties.update(parse_attrs(prop_match.group(1)))
        return properties

    datastr = clean_text(datastr)

    # DOTALL permits descriptors to span lines. Stream properties are shared
    # by every variable, while packet properties describe individual columns.
    stream_match = re.search(r"<stream\b([^>]*)>(.*?)</stream>", datastr, re.DOTALL)
    if stream_match is not None:
        general_dict.update(parse_attrs(stream_match.group(1)))
        general_dict.update(parse_properties(stream_match.group(2)))

    packet_match = re.search(r"<packet\b[^>]*>(.*?)</packet>", datastr, re.DOTALL)
    if packet_match is not None:
        packet_text = packet_match.group(1)
        for var_match in re.finditer(r"<y\b([^>]*)>(.*?)</y>", packet_text, re.DOTALL):
            attrs = parse_attrs(var_match.group(1))
            name = attrs.get("name", "")
            if name == "":
                continue

            attrs.update(parse_properties(var_match.group(2)))
            # Preserve descriptor order to align numeric columns with names.
            varlist.append(name)
            vardict[name] = attrs

    vararray = [[] for _ in varlist]
    # Accept :NN: packet records with calendar or day-of-year UTC timestamps.
    data_line_re = re.compile(r"^:\d{2}:\s*(\d{4}-(?:\d{2}-\d{2}|\d{3})T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)\s*(.*)$")
    # Numeric fields may include signs, decimal fractions, and exponents.
    number_re = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")

    for line in datastr.splitlines():
        line = line.strip()
        data_match = data_line_re.match(line)
        if data_match is None:
            continue

        timearr.append(data_match.group(1))
        values = [float(value) for value in number_re.findall(data_match.group(2))]
        for index in range(len(varlist)):
            if index < len(values):
                vararray[index].append(values[index])
            else:
                # Pad absent fields so all columns stay aligned with timearr.
                vararray[index].append(float("nan"))

    return general_dict, timearr, varlist, vardict, vararray


def parse_general_dict(general_dict):
    """
    Return the stream title with property placeholders substituted.

    Parameters
    ----------
    general_dict : dict or str
        Stream-level attributes and properties returned by das2parse, or
        DAS2 stream XML text.

    Returns
    -------
    str
        Title with references such as '%{xCacheResolution}' replaced by
        their property values. Unknown references are left unchanged.
        Returns an empty string if the input cannot be parsed or has no
        valid string title.
    """

    try:
        if isinstance(general_dict, str):
            general_dict, _, _, _, _ = das2parse(general_dict)
        if not isinstance(general_dict, dict):
            return ""

        # Accept typed keys as well as the names already normalized by das2parse.
        properties = {
            key.split(":")[-1]: value for key, value in general_dict.items() if isinstance(key, str) and value is not None
        }
        title = properties.get("title", "")
        if not isinstance(title, str):
            return ""
        # Resolve references from this stream, retaining unknown placeholders.
        title = re.sub(
            r"%\{([^}]+)\}",
            lambda match: str(properties.get(match.group(1), match.group(0))),
            title,
        )
        # Also normalize titles supplied directly as dictionaries and any
        # formatting codes introduced by the substituted property values.
        return _autoplot_text(title)
    except (TypeError, ValueError):
        # Optional descriptive metadata must not prevent data from loading.
        return ""


def das2tplot(
    datastr="",
    varnames=None,
    prefix="",
    suffix="",
):
    """
    Convert DAS2 ASCII response text to tplot variables.

    Parameters
    ----------
    datastr : str, optional
        DAS2 ASCII response text to parse.
    varnames : str or list of str, optional
        Variable name or list of variable names to store. By default, all
        parsed variables are stored. "*" and "" also select all
        variables.
    prefix : str, optional
        Prefix to add to each output tplot variable name.
    suffix : str, optional
        Suffix to add to each output tplot variable name.

    Returns
    -------
    list of str
        Names of the tplot variables created from the DAS2 data.

    Notes
    -----
    Each variable stores the resolved stream title and its variable attributes
    under the metadata key "DAS2", as "STREAM_TITLE" and "VATT".
    """
    vars_out = []

    if len(datastr) < 20:
        return vars_out

    # Normalize a single selector to a list; an empty list selects everything.
    if varnames is None:
        varnames = []
    elif not isinstance(varnames, list):
        varnames = [varnames]

    for var in varnames:
        # These two explicit selectors also request every available variable.
        if var == "*" or var == "":
            varnames = []
            break

    # Parse datastr and fill tplot variables
    general_dict, timearr, varlist, vardict, vararray = das2parse(datastr)

    stream_properties = parse_general_dict(general_dict)

    for idx, var in enumerate(varlist):
        if varnames is None or len(varnames) == 0 or var in varnames:
            var_name = prefix + var.lower() + suffix
            var_attrs = vardict.get(var, {})
            var_data = vararray[idx]
            ytitle = var_attrs.get("yLabel", "")
            units = var_attrs.get("units", "")

            # Keep shared stream information and per-variable attributes in
            # metadata; these entries do not appear on the plot by default.
            attr_dict = {
                "DAS2": {
                    "STREAM_TITLE": stream_properties,
                    "VATT": var_attrs,
                }
            }

            sdres = store_data(var_name, data={"x": timearr, "y": var_data}, attr_dict=attr_dict)
            if sdres:
                options(var_name, "ytitle", ytitle)
                # Display units separately from the descriptive axis label.
                options(var_name, "ysubtitle", units)
                vars_out.append(var_name)

    return vars_out


if __name__ == "__main__":
    # Example usage of the das2tplot function
    from pyspedas import get_data, tplot
    from pyspedas.utilities.das2.das2ascii import das2ascii

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

    vars_out = das2tplot(datastr=data, prefix="jovicentric_")
    print(vars_out)

    c = get_data("jovicentric_clat")
    print(c)

    tplot(vars_out)
