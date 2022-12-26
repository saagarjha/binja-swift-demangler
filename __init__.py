import binaryninja
import subprocess

def run_demanger(symbols):
	return subprocess.check_output(["swift", "demangle", "--compact", "--simplified"], input="\n".join(symbols).encode()).decode().strip().split("\n")

def demangle_swift(bv):
	swift_functions = []
	for function in bv.functions:
		if function.name.startswith("_$s"):
			swift_functions.append(function)
	results = run_demanger(map(lambda f: f.name, swift_functions))
	assert len(swift_functions) == len(results)
	for (function, name) in zip(swift_functions, results):
		if function.comment:
			function.comment = f"{function.comment} ({function.name})"
		else:
			function.comment = function.name
		function.name = name

	variables = bv.data_vars
	swift_variables = []
	for variable in variables:
		try:
			variable = variables[variable]
			if variable.name.startswith("_$s"):
				swift_variables.append(variable)
		except:
			pass
	results = run_demanger(map(lambda v: v.name, swift_variables))
	assert len(swift_variables) == len(results)
	for (variable, name) in zip(swift_variables, results):
		variable.name = name

binaryninja.PluginCommand.register("Swift Demangler", "Demangles Swift", demangle_swift)
