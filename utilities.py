import traceback

def loadFingerprintModules(module):
    targetHostnames = []
    fingerprintModules = {}
    for fingerprintName, fingerprintModule in module.modules.items():
        try:
            module = fingerprintModule()
            fingerprintModules[module['hostname']] = module
            targetHostnames.append(module['hostname'])
            if('hostname' not in module or type(module['hostname']) != str):
                raise Exception("Module has no hostname")
            if('name' not in module or type(module['hostname']) != str):
                raise Exception("Module has no name")
            if 'fingerprints' not in module or type(module['fingerprints']) != dict:
                raise Exception("Module has invalid fingerprints")
            if 'minMatches' not in module or type(module['minMatches']) != int:
                raise Exception("Module has invalid minimum fingerprint count")
            print(f"Loaded fingerprint module {fingerprintName} - Hostname: {module['hostname']} - Minimum Matches: {module['minMatches']}")
        except Exception as e:
            print(f"Failed to load fingerprint module {fingerprintName}:")
            print(traceback.format_exc())

    return [targetHostnames, fingerprintModules]

def loadDatastoreModules(module, datastoreHost):
    dataStoreModules = []
    for moduleName, fingerprintModule in module.modules.items():
        try:
            module = fingerprintModule(datastoreHost)
            if('name' not in module or type(module['name']) != str):
                raise Exception("Module has no name")
            if 'handleData' not in module:
                raise Exception("Module has invalid handleData method")
            print(f"Loaded datastore module {module['name']} - Server Host: {module['host']}")
            dataStoreModules.append(module)
        except Exception as e:
            print(f"Failed to load datastore module {moduleName}:")
            print(traceback.format_exc())

    return dataStoreModules