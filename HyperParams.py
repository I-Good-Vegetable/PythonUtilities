import collections
import pickle
from pathlib import Path


class HyperParams(object):
    hyperParams: dict

    def __init__(self, hyperParams=None, srcHyperParams=None):
        self.hyperParams = dict()
        if hyperParams is not None:
            self.hyperParams = hyperParams
        if srcHyperParams is not None:
            self.hyperParams = srcHyperParams.hyperParams

    def add(self, param):
        if isinstance(param, tuple):
            key, value = param
            self.hyperParams[key] = value
        elif isinstance(param, dict):
            self.hyperParams = {**self.hyperParams, **param}
        elif isinstance(param, HyperParams):
            self.hyperParams = {**self.hyperParams, **param.hyperParams}
        return self

    def __add__(self, another):
        newHyperParams = HyperParams(srcHyperParams=self)
        newHyperParams.add(another)
        return newHyperParams

    def toStr(self):
        orderedDict = collections.OrderedDict(sorted(self.hyperParams.items()))
        return '_'.join([f'{key}={value}' for key, value in orderedDict.items()])

    def toPkl(self, folder=None, filepath=None):
        if filepath is None and folder is not None:
            filepath = Path(folder) / Path(self.toStr() + '.dict')
        if filepath is not None:
            with open(filepath, 'wb') as pklFile:
                pickle.dump(self.hyperParams, pklFile)

    def loadPkl(self, filepath):
        with open(filepath, 'rb') as pklFile:
            data = pickle.load(pklFile)
            if isinstance(data, dict):
                self.hyperParams = data
            else:
                print('Not a dictionary')

    def __str__(self):
        return self.toStr()

    def __getattr__(self, item):
        return self.hyperParams[item]
