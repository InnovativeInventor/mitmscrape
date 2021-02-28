from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import pprint

"""
Credit: modified from mitmdump docs
"""

with open("results", "rb") as logfile:
    freader = io.FlowReader(logfile)
    pp = pprint.PrettyPrinter(indent=4)
    try:
        for f in freader.stream():
            print(f.request.pretty_url)
    except FlowReadException as e:
        print(f"Flow file corrupted: {e}")
