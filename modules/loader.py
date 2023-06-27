import os

class Loader():
    
    resources = {}
    def __init__(self, folders = []):
        self.folders = folders
        self.__list_resources()

    def __list_resources(self):
        for folder in self.folders:
            for path in os.listdir(folder):
                if os.path.isfile( os.path.join( folder, path )):
                    self.resources[ path ] = f'{os.path.join( folder, path )}'

    def get(self, resource):
        if resource in self.resources:
            return self.resources[resource]
        else:
            raise Exception(f'resource not found "{resource}"')
