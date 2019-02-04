# -*- coding: utf-8 -*-
try:
    from types import SimpleNamespace  # New in version 3.3
except ImportError:
    class SimpleNamespace(object):
        def __init__(self, **kwds):
            self.__dict__.update(kwds)

        def __repr__(self):
            keys = sorted(self.__dict__)
            items = ('{0}={1!r}'.format(k, self.__dict__[k]) for k in keys)
            return '{0}({1})'.format(type(self).__name__, ', '.join(items))

        def __eq__(self, other):
            return self.__dict__ == other.__dict__


class MagicNamespace(SimpleNamespace):
    """Return a subclass of MagicNamespace that supports special names.

    This class works like types.SimpleNamespace but also supports
    special names (i.e., magic methods and attributes).

    Magic methods and attributes must be provided as keyword arguments
    during instantiation---they cannot be added later. Functions that
    are assigned to magic methods will be bound to the class instance
    and should accept a *self* argument.
    """
    def __new__(cls, subclassname, **kwds):
        special_names, normal_names = cls._partition_kwds(kwds)
        subcls = type(subclassname, (cls,), special_names)
        return super(MagicNamespace, subcls).__new__(subcls, **normal_names)

    def __init__(self, name, **kwds):
        special_names, normal_names = self._partition_kwds(kwds)
        self._special_names = special_names
        super(MagicNamespace, self).__init__(**normal_names)

    @staticmethod
    def _partition_kwds(kwds):
        """Take a dictionary of names and objects and returns two
        dictionaries---one with special (dunder) names and one with
        normal names.
        """
        special_names = dict()
        normal_names = dict()

        for name, obj in kwds.items():
            if name.startswith('__') and name.endswith('__'):
                special_names[name] = obj
            else:
                normal_names[name] = obj

        return special_names, normal_names

    def __setattr__(self, name, value):
        if name.startswith('__') and name.endswith('__'):
            msg = ('cannot assign special names after instantiation '
                   '(they must be provided during object creation)')
            raise ValueError(msg)
        super(MagicNamespace, self).__setattr__(name, value)

    def __repr__(self):
        attr_dict = dict(self.__dict__)
        attr_dict.pop('_special_names')
        attr_dict.update(self._special_names)

        attr_items = sorted(attr_dict.items())
        formatted = ('{0}={1!r}'.format(k, v) for k, v in attr_items)
        return '{0}({1})'.format(type(self).__name__, ', '.join(formatted))
