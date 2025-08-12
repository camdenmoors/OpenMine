from pkgutil import iter_modules
import os
from importlib import import_module

globals()['modules'] = {}

package_dir = os.path.dirname(os.path.abspath(__file__))

for (_, module_name, _) in iter_modules([package_dir]):
    globals()['modules'][module_name] = getattr(import_module(f"{__name__}.{module_name}"), 'getModule')