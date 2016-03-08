Title: Object oriented Python
Date: 2016-01-06
Category: Python
Tags: python
Author: TDB
Status: draft
Summary: All about object oriented python.

# 0. Old style vs new style class



Up to Python 2.1, old-style classes were the only flavour available to the user. The concept of (old-style) class is unrelated to the concept of type: if x is an instance of an old-style class, then x.__class__ designates the class of x, but type(x) is always <type 'instance'>. This reflects the fact that all old-style instances, independently of their class, are implemented with a single built-in type, called instance.

For old-style classes (the only flavour of classes up to Python 2.1), have the following property :
If x is an instance of the class, then `x.__class__` designates the class of x.
However, `type(x)` will always return `instance`.

New-style classes, introduced in Python 2.2, unify the concepts of class and type. Calling `type(x)` or `x.__class__` will return the same thing (unless you override it). 

The major motivation for introducing new-style classes is to provide a unified object model with a full meta-model. It also has a number of immediate benefits, like the ability to subclass most built-in types, or the introduction of "descriptors", which enable computed properties.

In Python 2.7, classes are still old-style by default. New-style classes are created by inheriting from a new-style class or from `object`.

New-style classes introduce a couple of important changes : the `super()` function (more later), descriptors, or the order in which functions are looked-up in case of multiple inheritance.

In short, you get :

```python
class NewStyleClass(object):
    pass

class AnotherNewStyleClass(NewStyleClass):
    pass
Old-style classes don't.

class OldStyleClass():
    pass
```

Python 3 only has new-style classes, whether you subclass from `object` or not.

# 1. Overloading

It is possible to overload common operators, like + in this case by redefining the relevant function (__add__() in this case).

```python
class TestOverloading():

def __init__(self, a):
	self._val = a

def __add__(self, b):
	return self._val * b._val
```

	> a = TestOverloading(2)
	> b = TestOverloading(3)
	> print a+b
	> 6

# 2. Inheritance

```python
class Base(object):
	def __init__(self):
		print "1"

class Child(Base):
	def __init__(self):
		super(Child, self).__init__()
```

Super indicates that we use the inherited `__init__` method
N.B. The base class needs to inherit from object

# 3. Overriding Base class functions

```python

class Base():
	def _method():
		# do things

class Child(Base):

	def _method():
		# do other things
		# this overrides the base class _method
```


# 4. Abstract Base Classes

A class is an abstract base class (ABC) if its only purpose is to serve as a base class through inheritance.
An ABC cannot be instantiated.

from abc import ABCMeta, abstractmethod
# need these definitions


# 5. Using super

*N.B.* `super` only works with new style classes.

This part relies heavily on this [stack thred](http://stackoverflow.com/questions/222877/how-to-use-super-in-python/33469090#33469090).

In a class hierarchy with single inheritance, super can be used to refer to parent classes without naming them explicitly, thus making the code more maintainable. 

Let's give an example :

```python
class ChildA(Base):
    def __init__(self):
        Base.__init__(self)

class ChildB(Base):
    def __init__(self):
        super(ChildB, self).__init__()
```

In the case of simple inheritance, these two chunks of codes achieve the same thing (i.e. showing the `ChildA` and `ChildB` explicitly inherit the `__init__` method from `Base`). However, were we to change the name of `Base`, we would have to change it everywhere it was used to specify inheritance.

The second use case is to support cooperative multiple inheritance. Once again, let's use an example to illustrate. 

```python
class SomeBaseClass(object):
    def __init__(self):
        print('SomeBaseClass.__init__(self) called')

class Child(SomeBaseClass):
    def __init__(self):
        print('Child.__init__(self) called')
        SomeBaseClass.__init__(self)

class SuperChild(SomeBaseClass):
    def __init__(self):
        print('SuperChild.__init__(self) called')
        super(SuperChild, self).__init__()

class InjectMe(SomeBaseClass):
    def __init__(self):
        print('InjectMe.__init__(self) called')
        super(InjectMe, self).__init__()

class UnsuperInjector(Child, InjectMe): pass

class SuperInjector(SuperChild, InjectMe): pass
```

Let's look at the results :

	>>> o = UnsuperInjector()
	Child.__init__(self) called
	SomeBaseClass.__init__(self) called

	>>> o2 = SuperInjector()
	SuperChild.__init__(self) called
	InjectMe.__init__(self) called
	SomeBaseClass.__init__(self) called

So we see that the dependency on InjectMe is only taken into account through the use of `super`.
Using `super`, we can inject a class (`InjectMe`) between two other classes (`Child` and `SomeBaseClass`). This gives you a way of influencing the behaviour of the `SuperInjector` class without modifying the code of the base class.