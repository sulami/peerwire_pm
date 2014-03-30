#!/bin/bash

cat skills | awk '{print "- model: projects.skill\n  pk: "FNR"\n  fields:\n    name: "$0}' > skills.yaml
