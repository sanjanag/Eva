# coding=utf-8
# Copyright 2018-2020 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from src.parser.table_ref import TableInfo
from src.catalog.catalog_manager import CatalogManager
from typing import List

from src.expression.abstract_expression import AbstractExpression
from src.expression.tuple_value_expression import ExpressionType

from src.parser.create_statement import ColumnDefinition

from src.utils.logging_manager import LoggingLevel
from src.utils.logging_manager import LoggingManager


def bind_table_ref(video_info: TableInfo) -> int:
    """Grab the metadata id from the catalog for
    input video

    Arguments:
        video_info {TableInfo} -- [input parsed video info]
    Return:
        catalog_entry for input table
    """

    catalog = CatalogManager()
    catalog_entry_id, _ = catalog.get_table_bindings(video_info.database_name,
                                                     video_info.table_name,
                                                     None)
    return catalog_entry_id


def bind_columns_expr(target_columns: List[AbstractExpression]):
    if target_columns is None:
        return

    for column_exp in target_columns:
        child_count = column_exp.get_children_count()
        for i in range(child_count):
            bind_columns_expr([column_exp.get_child(i)])

        if column_exp.etype == ExpressionType.TUPLE_VALUE:
            bind_tuple_value_expr(column_exp)


def bind_tuple_value_expr(expr: AbstractExpression):
    catalog = CatalogManager()
    table_id, column_ids = catalog.get_table_bindings(None,
                                                      expr.table_name,
                                                      [expr.col_name])
    expr.table_metadata_id = table_id
    if not isinstance(column_ids, list) or len(column_ids) == 0:
        LoggingManager().log(
            "Optimizer Utils:: bind_tuple_expr: \
            Cannot bind column name provided", LoggingLevel.ERROR)

    expr.col_metadata_id = column_ids.pop()


def bind_predicate_expr(predicate: AbstractExpression):
    # This function will be expanded as we add support for
    # complex predicate expressions and sub select predicates

    child_count = predicate.get_children_count()
    for i in range(child_count):
        bind_predicate_expr(predicate.get_child(i))

    if predicate.etype == ExpressionType.TUPLE_VALE:
        bind_tuple_value_expr(predicate)


def create_column_metadata(col_list: List[ColumnDefinition]):
    """Create column metadata for the input parsed column list. This function
    will not commit the provided column into catalog table. 
    Will only return in memory list of ColumnDataframe objects

    Arguments:
        col_list {List[ColumnDefinition]} -- parsed col list to be created
    """
    if isinstance(col_list, ColumnDefinition):
        col_list = [col_list]

    result_list = []
    for col in col_list:
        if col is None:
            LoggingManager().log(
                "Empty column while creating column metadata",
                LoggingLevel.ERROR)
            result_list.append(col)
        result_list.append(
            CatalogManager().create_column_metadata(
                col.name, col.type, col.dimension))

    return result_list
