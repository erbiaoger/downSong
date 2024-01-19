import os
import sys

class Spec:
    def __init__(self, path):
        self.path = path
        self.spec = self.read_spec()
    
    def read_spec(self):

        with open(self.path, 'r') as f:
            spec = f.read()
        return spec