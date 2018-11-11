'''
Created on 07.12.2016

@author: rudnikp
'''
import imp
import os
import pkgutil
MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')

def package_contents(package_name):
    file, pathname, description = imp.find_module(package_name)
    if file:
        raise ImportError('Not a package: %r', package_name)
    # Use a set because some may be both source and compiled.
    #return set([os.path.splitext(module)[0]
    #return set([module for module in os.listdir(pathname) if module.endswith(MODULE_EXTENSIONS)])
    return set([module for module in os.listdir(pathname) if module.endswith(MODULE_EXTENSIONS)])
    #return [name for _, name, _ in pkgutil.iter_modules([package_name])]


def print_package_content(package_name): 
    for module in package_contents(package_name):
        print("{p}.{m}".format(p=package_name, m=module))
    
    
if __name__ == "__main__":
    print_package_content("Carbon")
         