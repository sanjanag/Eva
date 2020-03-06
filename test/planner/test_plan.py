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
import unittest
from src.parser.table_ref import TableRef, TableInfo
from src.catalog.models.df_column import DataFrameColumn
from src.catalog.column_type import ColumnType

from src.planner.create_plan import CreatePlan
from src.planner.insert_plan import InsertPlan
from src.planner.types import PlanNodeType


class PlanNodeTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_create_plan(self):
        dummy_info = TableInfo('dummy')
        dummy_table = TableRef(dummy_info)

        columns = [DataFrameColumn('id', ColumnType.INTEGER),
                   DataFrameColumn('name', ColumnType.TEXT,
                                   array_dimensions=50)]
        dummy_plan_node = CreatePlan(dummy_table, columns, False)
        self.assertEqual(dummy_plan_node.node_type, PlanNodeType.CREATE)
        self.assertEqual(dummy_plan_node.if_not_exists, False)
        self.assertEqual(dummy_plan_node.video_ref.table_info.table_name,
                         "dummy")
        self.assertEqual(dummy_plan_node.column_list[0].name, "id")
        self.assertEqual(dummy_plan_node.column_list[1].name, "name")

    def test_insert_plan(self):
        video_id = 0
        column_ids = [0, 1]
        expression = type("AbstractExpression", (), {"evaluate": lambda: 1})
        values = [expression, expression]
        dummy_plan_node = InsertPlan(video_id, column_ids, values)
        self.assertEqual(dummy_plan_node.node_type, PlanNodeType.INSERT)


if __name__ == '__main__':
    unittest.main()
