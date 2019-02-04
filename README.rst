
MagicNamespace
==============

Implements a ``MagicNamespace`` class that works like
``types.SimpleNamespace`` but also supports special names
(i.e., magic methods and attributes).

I'm not sure how useful this code is since it's perfectly
reasonable to subclass ``types.SimpleNamespace`` directly
and add methods as needed. As it turned out, writing this
code was ultimately an exercise in basic metaprogramming.
