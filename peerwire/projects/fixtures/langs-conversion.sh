#!/bin/bash

cat langs | awk '{print "- model: projects.lang\n  pk: "FNR"\n  fields:\n    name: "$0}' > initial_data.yaml
