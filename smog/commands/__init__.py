# import pkgutil

# pkgutil.walk_packages(__path__)

# commands = []

# for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
#     if module_name == "base":
#         continue
    
#     commands.append(
#         loader.find_module(module_name, __path__)
#         .load_module(module_name)
#         .Command(manager)
#     )
