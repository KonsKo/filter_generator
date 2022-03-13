"""Filter module for table Letter."""
######################################
# This file has been auto generated. #
######################################

from datetime import datetime
from typing import Any, List, Optional

from db.schema import Letter
from pydantic import BaseModel

OFFSET_DEFAULT = 0
LIMIT_DEFAULT = 50


class BaseFilter(BaseModel):
    """Base filter."""

    offset: int = OFFSET_DEFAULT
    limit: int = LIMIT_DEFAULT


class FilterFieldTsFrom(BaseModel):
    """Filter field class."""

    name: str = 'ts_from'
    datatype: Any = datetime
    op: str = 'from'
    field_names: Optional[List] = None
    field_value: Any


class FilterFieldT(BaseModel):
    """Filter field class."""

    name: str = 'T'
    datatype: Any = str
    op: str = 'T'
    field_names: Optional[List] = ['sender', 'to', 'subject']
    field_value: Any


class FilterFieldWtf(BaseModel):
    """Filter field class."""

    name: str = 'wtf'
    datatype: Any = str
    op: str = 'custom'
    field_names: Optional[List] = None
    field_value: Any


class FilterFieldSender(BaseModel):
    """Filter field class."""

    name: str = 'sender'
    datatype: Any = str
    op: str = '='
    field_names: Optional[List] = None
    field_value: Any


class FilterFieldSenderIn(BaseModel):
    """Filter field class."""

    name: str = 'sender_in'
    datatype: Any = str
    op: str = 'in'
    field_names: Optional[List] = None
    field_value: Any


class FilterFieldUser(BaseModel):
    """Filter field class."""

    name: str = 'user'
    datatype: Any = int
    op: str = 'eq'
    field_names: Optional[List] = None
    field_value: Any


class FilterFieldTsTo(BaseModel):
    """Filter field class."""

    name: str = 'ts_to'
    datatype: Any = datetime
    op: str = 'to'
    field_names: Optional[List] = None
    field_value: Any


class LetterFilter(BaseFilter):
    """Filter class."""

    name: str = 'LetterFilter'
    model: str = Letter
    order_by: Optional[list] = ['ts desc', 'id']
    ff_ts_from = FilterFieldTsFrom()
    ff_t = FilterFieldT()
    ff_wtf = FilterFieldWtf()
    ff_sender = FilterFieldSender()
    ff_sender_in = FilterFieldSenderIn()
    ff_user = FilterFieldUser()
    ff_ts_to = FilterFieldTsTo()


######################################
# This file has been auto generated. #
######################################
