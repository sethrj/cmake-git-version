#!/bin/sh -ex
# Copyright 2021 UT-Battelle, LLC
# See the top-level LICENSE file for details.
# SPDX-License-Identifier: Apache-2.0

if [ -z "$1" ]; then
  echo "usage: $0 project-cmake-dir" > &2
  exit 2
fi

exit 1
