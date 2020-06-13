from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Type, Generic, List
import inspect
import operator
import random

from logger import logger
from common_utils.check_utils import check_type_from_list, check_type

T = TypeVar('T')
H = TypeVar('H')

class BasicObject(Generic[T]):
    @abstractmethod
    def __str__(self) -> str:
        ''' To override '''
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()
    
    def __key(self) -> tuple:
        return tuple([self.__class__.__name__] + list(self.__dict__.values()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    @classmethod
    def get_constructor_params(cls) -> list:
        return [param for param in list(inspect.signature(cls.__init__).parameters.keys()) if param != 'self']

    def to_constructor_dict(self) -> dict:
        constructor_dict = {}
        for key, val in self.__dict__.items():
            if key in self.get_constructor_params():
                constructor_dict[key] = val
        return constructor_dict

    @classmethod
    def buffer(cls: T, obj) -> T:
        return obj

    def copy(self: T) -> T:
        obj = type(self)(*self.to_constructor_dict().values())
        obj.__dict__ = self.__dict__
        return obj

class BasicObjectList:
    def __init__(self: H, obj_type: type, obj_list: List[T]=None):
        check_type(obj_type, valid_type_list=[type])
        self.obj_type = obj_type
        if obj_list is not None:
            check_type_from_list(obj_list, valid_type_list=[obj_type])
        self.obj_list = obj_list if obj_list is not None else []

    def __key(self) -> tuple:
        return tuple([self.__class__] + list(self.__dict__.values()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self: H):
        return f'{self.__class__.__name__}({[obj for obj in self]})'

    def __repr__(self: H):
        return self.__str__()

    def __len__(self: H) -> int:
        return len(self.obj_list)

    def __getitem__(self: H, idx: int) -> T:
        if type(idx) is int:
            if len(self.obj_list) == 0:
                logger.error(f"{type(self).__name__} is empty.")
                raise IndexError
            elif idx < 0 or idx >= len(self.obj_list):
                logger.error(f"Index out of range: {idx}")
                raise IndexError
            else:
                return self.obj_list[idx]
        elif type(idx) is slice:
            return self.obj_list[idx.start:idx.stop:idx.step]
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __setitem__(self: H, idx: int, value: T):
        check_type(value, valid_type_list=[self.obj_type])
        if type(idx) is int:
            self.obj_list[idx] = value
        elif type(idx) is slice:
            self.obj_list[idx.start:idx.stop:idx.step] = value
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __delitem__(self: H, idx: int):
        if type(idx) is int:
            if len(self.obj_list) == 0:
                logger.error(f"{type(self).__name__} is empty.")
                raise IndexError
            elif idx < 0 or idx >= len(self.obj_list):
                logger.error(f"Index out of range: {idx}")
                raise IndexError
            else:
                del self.obj_list[idx]
        elif type(idx) is slice:
            del self.obj_list[idx.start:idx.stop:idx.step]
        else:
            logger.error(f'Expected int or slice. Got type(idx)={type(idx)}')
            raise TypeError

    def __iter__(self: H) -> H:
        self.n = 0
        return self

    def __next__(self: H) -> T:
        if self.n < len(self.obj_list):
            result = self.obj_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def copy(self: H) -> H:
        return type(self)(self.obj_list.copy())

    def append(self: H, item: T):
        check_type(item, valid_type_list=[self.obj_type])
        self.obj_list.append(item)

    def sort(self: H, attr_name: str, reverse: bool=False):
        if len(self) > 0:
            attr_list = list(self.obj_list[0].__dict__.keys())    
            if attr_name not in attr_list:
                logger.error(f"{self.obj_type.__name__} class has not attribute: '{attr_name}'")
                logger.error(f'Possible attribute names:')
                for name in attr_list:
                    logger.error(f'\t{name}')
                raise Exception

            self.obj_list.sort(key=operator.attrgetter(attr_name), reverse=reverse)
        else:
            logger.error(f"Cannot sort. {type(self).__name__} is empty.")
            raise Exception

    def shuffle(self: H):
        random.shuffle(self.obj_list)