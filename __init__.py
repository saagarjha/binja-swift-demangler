import binaryninja
import subprocess

def demangle_swift(bv):
	swift_functions = []
	for function in bv.functions:
		if function.name.startswith("_$s"):
			swift_functions.append(function)
	results = subprocess.check_output(["xcrun", "swift-demangle", "--compact", "--simplified"], input="\n".join(map(lambda f: f.name, swift_functions)).encode()).decode().strip().split("\n")
	assert len(swift_functions) == len(results)
	for (function, name) in zip(swift_functions, results):
		if function.comment:
			function.comment = f"{function.comment} ({function.name})"
		else:
			function.comment = function.name
		function.name = name

binaryninja.PluginCommand.register("Swift Demangler", "Demangles Swift", demangle_swift)
