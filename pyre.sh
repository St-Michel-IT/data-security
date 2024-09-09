#!/usr/bin/bash
pyre init-pysa
pyre analyze --no-verify --save-results-to ./pysa-runs
sapp --database-name sapp.db analyze ./pysa-runs/taint-output.json
sapp --database-name sapp.db server --source-directory=./