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

import numpy as np

from src.models.storage.batch import FrameBatch
from src.models.storage.frame import Frame
from src.executor.pp_executor import PPExecutor
from ..executor.utils import DummyExecutor


class PPScanExecutorTest(unittest.TestCase):

    def test_should_return_only_frames_satisfy_predicate(self):
        frame_1 = Frame(1, np.ones((1, 1)), None)
        frame_2 = Frame(1, 2 * np.ones((1, 1)), None)
        frame_3 = Frame(1, 3 * np.ones((1, 1)), None)
        batch = FrameBatch(frames=[
            frame_1,
            frame_2,
            frame_3,
        ], info=None)
        expression = type("AbstractExpression", (), {"evaluate": lambda x: [
            False, False, True]})

        plan = type("PPScanPlan", (), {"predicate": expression})
        predicate_executor = PPExecutor(plan)
        predicate_executor.append_child(DummyExecutor([batch]))

        expected = FrameBatch(frames=[frame_3], info=None)
        filtered = list(predicate_executor.exec())[0]
        self.assertEqual(expected, filtered)
