Arase (ERG) Analysis Tools
===========================

Coordinate transformations
---------------------------

The ERG mission defines coordinate systems SGA, SGI, and DSI.  The J2000 system
serves as a bridge between the ERG systems and the geophysical systems handled
by pyspedas.cotrans().

The top-level routine for converting between SGA, SGI, DSI, and J2000 is erg_cotrans.

.. autofunction:: pyspedas.projects.erg.erg_cotrans

.. autofunction:: pyspedas.projects.erg.dsi2j2000

.. autofunction:: pyspedas.projects.erg.sga2sgi

.. autofunction:: pyspedas.projects.erg.sgi2dsi


Particle Tools
--------------

.. autofunction:: pyspedas.projects.erg.erg_hep_part_products

.. autofunction:: pyspedas.projects.erg.erg_lep_part_products

.. autofunction:: pyspedas.projects.erg.erg_mep_part_products




Example
^^^^^^^

.. code-block:: python

        import pytplot
        import pyspedas
        from pyspedas.projects.erg import erg_mep_part_products
        from pyspedas import timespan, tplot
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa80-100')
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa0-10')

        ## Decorate the obtained spectrum variables
        pytplot.options('erg_mepe_l2_3dflux_FEDU_energy_mag_pa80-100', 'ytitle', 'MEP-e flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_mepe_l2_3dflux_FEDU_energy_mag_pa0-10', 'ytitle', 'MEP-e flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_mepe_l2_3dflux_FEDU_energy_mag_pa80-100', 'erg_mepe_l2_3dflux_FEDU_energy_mag_pa0-10'], save_png='erg_mep_en_pa_limit.png')

.. image:: _static/erg_mep_en_pa_limit.png
   :align: center
   :class: imgborder

.. autofunction:: pyspedas.projects.erg.erg_xep_part_products