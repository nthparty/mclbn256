mclbn256
========

Python library that serves as an API for the BN254/256 pairing-friendly
curve implemented in `MCl <https://github.com/herumi/mcl>`__
in C.

.. image:: https://badge.fury.io/py/mclbn256.svg
    :target: https://badge.fury.io/py/mclbn256
    :alt: PyPI version and link.

Package Installation and Usage
------------------------------

The package is available on
`PyPI <https://pypi.org/project/mclbn254/>`__:

.. highlight:: shell

::

   pip install mclbn256

The library can be imported in the usual ways:

.. highlight:: python

::

   import mclbn256  # Abstracted 'dumb' API over the scalar and point groups
   from mclbn256 import mclbn256  # Extended attributes, internals, classes, test methods

Examples
~~~~~~~~

This library supports concise construction of elliptic curve points
(groups G1 and G2) and scalars (group Fr):

::

   from mclbn256 import G1, G2, Fr
   >>> p = G1().hash("some row")
   >>> q = G2().hash("another row")
   >>> p.valid()
   True
   >>> q.valid()
   True
   >>> s = Fr(6)
   >>> t = Fr(857462736753)
   >>> ((p * s) @ (q * t)) == (p @ (q * s * t))
   True
   >>> ((p * s * ~t) @ (q * t)) == (p @ (q * s))
   True
   >>> ((p * s) @ q) == ((p * ~t) @ (q * s * t))
   True

Data structures for the relevant curve subgroups and finite fields are
included as well:

::

   >>> len(Fr().randomize().serialize())
   32
   >>> len(G1().randomize().serialize())
   32
   >>> len(G2().randomize().serialize())
   64
   >>> len((G1().randomize() @ G2().randomize()).serialize()) <= 384
   True
   
The representation of BN254 points and scalars in this library is compatible with the pure-Python `bn254 <https://pypi.org/project/bn254/>`__ implementation thanks to :code:`ECp_to_G1` and the other similarly-named helpers.  We may also convert points in that library's representation to the minimal-size MCl `serial <https://github.com/herumi/mcl/blob/0489e76cfae425ab9d3ec93952e9ae928ef86017/include/mcl/op.hpp#L78-L103>`__ format using :code:`ECp_serialize`.

::

    >>> Q = G1.random(); G1().deserialize(ECp_serialize(G1_to_ECp(Q))) == Q and Q.serialize() == ECp_serialize(G1_to_ECp(Q))
    True

Please see the package
`oblivious <https://pypi.org/project/oblivious/>`__ (which extends this
package) for more examples of how to use the BN254 curve.

Contributions
-------------

In order to contribute to the source code, open an issue or submit a
pull request on the `GitHub page <mclbn256.py>`__ for this library.

Versioning
----------

Beginning with version 0.1.0, the version number format for this library
and the changes to the library associated with version number increments
conform with `Semantic Versioning
2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Naming Notes
------------

BN-256 was an old name for the Barreto–Naehrig(2,254) Weierstrass curve,
when it was though to have close to 256 bits of security. It has since
been estimated to have at least 90 bits of security (compared to
symmetric ciphers) and is now more commonly refered to by BN254, after
the number of bits in its prime modulus. Specifically, :code:`mclbn256` is the
`name <https://github.com/herumi/mcl/blob/master/Makefile#L49>`__ of the subset of the MCl library containing the support for this
curve.
