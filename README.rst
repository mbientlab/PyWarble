PyWarble
########
PyWarble provides Python classes that wrap around the exported functions of the `Warble <https://github.com/mbientlab/Warble>`_ 
C library.  

Install
#######
Use ``pip`` to install the warble package.  

.. code-block:: bash

    pip install warble
    
As this project requires compiling the ``warble`` C library, you will need to configure your target machine to have the 
appropriate build environment before running ``pip`` as described in warble's 
`README <https://github.com/mbientlab/Warble/blob/master/README.md#build>`_.  

Windows
=======
The setup script will build the dll with ``MSBuild``.  Make sure your ``Path`` system variable has an entry pointing to the 
``MSBuild`` executable and that you have the necessary 
`Windows 10 SDK <https://github.com/mbientlab/Warble/blob/master/README.md#windows-10>`_ installed.  

Linux
=====
Install the required tools and packages detailed in the `Linux <https://github.com/mbientlab/Warble/blob/master/README.md#linux>`_ 
build section.

Usage
#####
See the Python scripts in the `examples <https://github.com/mbientlab/PyWarble/blob/master/examples>`_ folder.  
