#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os.path import abspath
from os.path import dirname as d
from pathlib import Path

# Load in root dir to system path for easy access
ROOT_DIR = d(d(abspath(__file__)))
sys.path.append(ROOT_DIR)

if ROOT_DIR.endswith("tests"):
    TEST_DIR = str(ROOT_DIR)
else:
    TEST_DIR = str(Path(ROOT_DIR + "/tests"))


def test_place_holder():
    pass
