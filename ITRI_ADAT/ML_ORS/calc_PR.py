#!/usr/bin/env python3

from julia.api import Julia

julia_file = 'calc_PR.jl'

jl = Julia(compiled_modules=False)

jl.eval('include("' + julia_file +  '")')



