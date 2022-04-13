from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

globals()['modules'] = {}

package_dir = Path(__file__).resolve()
for (_, module_name, _) in iter_modules(['./fingerprints']):
    globals()['modules'][module_name] = getattr(import_module(f"{__name__}.{module_name}"), 'getModule')