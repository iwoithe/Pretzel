from enum import Enum


# Add Items Dialog type
class AddItemsDialogType(Enum):
    """ The types for the AddItemsDialog """
    Item = 1
    Stock = 2


# Stock Type type

class StockType(Enum):
    """ The types for loading stock """
    Default = 1
    Edit = 2