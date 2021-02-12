#!/bin/sh -e
# Copyright 2021 UT-Battelle, LLC
# See the top-level LICENSE file for details.
# SPDX-License-Identifier: Apache-2.0

if [ -z "$1" ]; then
  echo "usage: $0 project-cmake-dir" >&2
  exit 2
fi

if [ ! -d "$1" ]; then
  echo "$1: not a directory" >&2
  exit 2
fi

SRC="$(dirname "$0")/CgvFindVersion.cmake"
DST="$1/CgvFindVersion.cmake"
cp "$SRC" "$DST"
echo "-- Copied script to $DST" >&2

GITATTR="$1/.gitattributes"
if [ ! -e "$GITATTR" ] \
  || ! grep "^/CgvFindVersion.cmake" "$GITATTR" >/dev/null
then
  cat >>"$GITATTR" <<EOF
/.gitattributes export-ignore
/CgvFindVersion.cmake export-subst
EOF
  echo "-- Updated $GITATTR" >&2
fi
