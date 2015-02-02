import os
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

projects = ['pysf']
data_extensions = set()


class PackageFinder:
    '''Python package finder'''
    def __init__(self, projects, data_extension):
        self.projects = projects
        self.data_extension = data_extension

    def find_belong(self, path):
        head = path
        while head.replace(os.sep, '.') not in self.packages:
            head, _ = os.path.split(head)
        return head.replace(os.sep, '.')

    def search(self):
        '''Search for packages'''
        self.packages = []
        self.package_data = {}
        for dir in self.projects:
            for item in os.walk(dir):
                if '__init__.py' in item[2]:
                    self.packages.append(item[0].replace(os.sep, '.'))
                for filename in item[2]:
                    _, ext = os.path.splitext(filename)
                    if ext in self.data_extension:
                        key = self.find_belong(item[0])
                        if key not in self.package_data:
                            self.package_data[key] = []
                        self.package_data[key].append(
                            os.path.join(item[0], filename).replace(
                                key.replace('.', os.sep), ''
                            ).lstrip(os.sep)
                        )

finder = PackageFinder(projects, data_extensions)
finder.search()

setup(
    name='Engel',
    version='0.0.1',
    description='Python script connecting to Hub via SF',
    packages=finder.packages,
    package_data=finder.package_data
)
