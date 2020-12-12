#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  import_.py
#
#  Copyright 2020 iwoithe <iwoithe@just42.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import openpyxl
import pandas as pd

from Pretzel.core.database.items import add_items


def import_excel(file: str, columns_dict: dict, database: str = "data/databases/data.db"):
    """ Imports items from a Microsoft Excel (Excel) file into Pretzel's database

     :param file: The file path of the Excel file
     :type file: str
     :param columns_dict: The column indexes
     :type columns_dict: dict
     :param database: The database to import the items to
     :type database: str """

    columns = {}
    for c in columns_dict:
        if columns_dict[c] > 0:
            columns[c] = (columns_dict[c] - 1)

    # Sort the columns
    sorted_columns = {}
    sorted_keys = sorted(columns, key=columns.get)
    for w in sorted_keys:
        sorted_columns[w] = columns[w]

    columns = sorted_columns

    # Load the data
    columns_list = list(columns.values())

    wb = openpyxl.load_workbook(file)
    for sheet_name in wb.sheetnames:
        df = pd.read_excel(file, sheet_name, usecols=columns_list)

    # Redo the indexes
    index = 0
    for c in columns:
        columns[c] = index
        index += 1

    items = []
    for row in df.iloc:
        item = []

        # Name
        try:
            item.append(row.iloc[columns["Name"]])
        except KeyError:
            items.append("")

        # Chemical Formula
        try:
            item.append(row.iloc[columns["Chemical Formula"]])
        except KeyError:
            item.append("")

        # Warning Label
        try:
            item.append(str(row.iloc[columns["Warning Label"]]).title())
        except KeyError:
            item.append("None")

        # Danger Level
        try:
            item.append(str(row.iloc[columns["Danger Level"]]).title())
        except KeyError:
            item.append("None")

        # Notes
        try:
            item.append(row.iloc[columns["Notes"]])
        except KeyError:
            item.append("")

        # Pictograms
        item.append("")

        # Add the item to the items list
        items.append(item)

    add_items(items=items)


def import_ods(file: str, database: str = "data/databases/data.db"):
    """ Imports items from an Open Document Spreadsheet (ODS) into Pretzel's database

     :param file: The file path of the ODS file
     :type file: str
     :param database: The database to import the items to
     :type database: str """

    pass


def import_csv(file: str, database: str = "data/databases/data.db"):
    """ Imports items from a comma separated values (CSV) file into Pretzel's database

     :param file: The file path of the CSV file
     :type file: str
     :param database: The database to import the items to
     :type database: str """

    pass