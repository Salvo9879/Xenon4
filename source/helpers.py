""" Basic functions which help other internal packages.
Should be imported like this:

```python
import source.helpers as helpers
``` """

# Import standard packages
import datetime

def get_current_datetime() -> datetime.datetime:
    """ Returns a `datetime.datetime` object of the current datetime. """
    return datetime.datetime.now()

def convert_to_iso(datetime_: datetime.datetime) -> str:
    """ Converts a `datetime.datetime` object to ISO 8601 format.
     
    Params:
        - datetime_ (datetime.datetime) - The `datetime.datetime` object wanted to be converted. """
    return datetime_.isoformat()