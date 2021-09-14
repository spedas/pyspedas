
Time Conversions
====================================

Convert from unix time to a string
------------------------------------

.. autofunction:: pyspedas.time_string

Example
^^^^^^^^^

.. code-block:: python

   from pyspedas import time_string
   time_string(1444953600.0)

.. code-block:: python

   '2015-10-16 00:00:00.000000'


Convert from a string to unix time
------------------------------------

.. autofunction:: pyspedas.time_double

Example
^^^^^^^^^

.. code-block:: python

   from pyspedas import time_double
   time_double('2015-10-16/14:00')

.. code-block:: python

   1445004000.0


Convert from a string or unix time to a datetime object
----------------------------------------------------------

.. autofunction:: pyspedas.time_datetime

Example
^^^^^^^^^

.. code-block:: python

   from pyspedas import time_datetime
   time_datetime('2015-10-16/14:00')


.. code-block:: python

   datetime.datetime(2015, 10, 16, 14, 0, tzinfo=datetime.timezone.utc)