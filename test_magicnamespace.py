#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from magicnamespace import MagicNamespace

try:
    unittest.TestCase.assertRegex  # New in version 3.2
except AttributeError:
    try:
        _oldname = unittest.TestCase.assertRegexpMatches  # New in version 3.1
        unittest.TestCase.assertRegex = _oldname
    except AttributeError:
        from re import compile

        def assertRegex(self, text, expected_regexp, msg=None):
            if isinstance(expected_regexp, str):
                expected_regexp = compile(expected_regexp)
            if not expected_regexp.search(text):
                msg = msg or "Regexp didn't match"
                msg = '%s: %r not found in %r' % (msg, expected_regexp.pattern, text)
                raise self.failureException(msg)

        unittest.TestCase.assertRegex = assertRegex


class TestMagicNamespace(unittest.TestCase):
    def test_empty_namespace(self):
        ns = MagicNamespace('MyNamespace')
        self.assertEqual(ns.__class__.__name__, 'MyNamespace')

    def test_subclass_behavior(self):
        """Should return subclass instances (not class instances)."""
        ns = MagicNamespace('MyNamespace')
        cls = ns.__class__

        self.assertIsNot(cls, MagicNamespace)
        self.assertTrue(issubclass(cls, MagicNamespace))

    def test_normal_names(self):
        """Should work like types.SimpleNamespace with normal names."""
        def func():
            return 'Hello World!'

        ns = MagicNamespace(
            'MyNamespace',
            func=func,
            attr=123,
        )
        self.assertEqual(ns.func(), 'Hello World!')
        self.assertEqual(ns.attr, 123)

    def test_special_names(self):
        """Allow magic methods and attributes during instantiation."""
        def func(self):  # <- Must accept *self*, will be bound to instance.
            return 'Hello World!'

        ns = MagicNamespace(
            'CallableNamespace',
            __call__=func,  # <- Assigned as magic method!
        )
        self.assertEqual(ns(), 'Hello World!')

    def test_assign_after_creation(self):
        ns = MagicNamespace('MyNamespace')

        # Normal names should work without issue.
        func = lambda: 'Hello World!'
        ns.func = func
        self.assertEqual(ns.func(), 'Hello World!')

        # Special names should fail.
        func = lambda self: 'Hello World!'
        msg = 'should not allow special method assignment after instantiation'
        with self.assertRaises(ValueError):
            ns.__call__ = func

    def test_repr(self):
        ns = MagicNamespace('MyNamespace')
        self.assertRegex(repr(ns), r'MyNamespace\(\)')

        ns.attr=1
        self.assertRegex(repr(ns), r'MyNamespace\(attr=1\)')

        ns = MagicNamespace('MyNamespace', attr=1, __call__=lambda self: True)
        regex = r'MyNamespace\(__call__=<[^,]+lambda[^,]+>, attr=1\)'
        self.assertRegex(repr(ns), regex)


if __name__ == '__main__':
    unittest.main()
