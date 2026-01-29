import importlib
import inspect

from core import config
from models import plugin_base



# Scan all the plugins in the plugins folder, and register them to the config.py.
def register_scanned_plugins():
    plugin_name_list = []
    for p in config.PLUGINS_DIR.iterdir():
        if p.suffix == ".py" and p.name != "__init__.py":
            plugin_name_list.append(p.stem)
    plugin_name_list.sort()

    plugins_dict = {}
    for i in range(0, len(plugin_name_list)):
        plugins_dict[i+1] = plugin_name_list[i]

    config.PLUGINS_DICT = plugins_dict



# Import plugin module by its id.
def load_plugin_module(plugin_id:int):
    plugin_name = config.PLUGINS_DICT[plugin_id]
    module_path = f"plugins.{plugin_name}"
    return importlib.import_module(module_path)




# Register the plugin instance to config.py.
def register_plugin_instance(plugin_id:int):
    plugin_module = load_plugin_module(plugin_id)

    # Find a Plugin's subclass.
    plugin_cls = None
    for name, obj in inspect.getmembers(plugin_module, inspect.isclass):
        # Make sure the object is AnalysisPlugin's subclass，and is not base-class itself.
        if issubclass(obj, plugin_base.AnalysisPlugin) and obj is not plugin_base.AnalysisPlugin:
            plugin_cls = obj
            break
    
    if plugin_cls is None:
        raise RuntimeError(f"Can't find a Plugin's subclass in the plugin {config.PLUGINS_DICT[plugin_id]}.")
    
    plugin_instance = plugin_cls()
    config.PLUGIN_INSTANCE = plugin_instance

