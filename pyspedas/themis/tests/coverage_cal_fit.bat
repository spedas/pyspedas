@echo off
cd C:/work/Codes/SPEDAS/pycharm/
coverage run --source=C:\work\Codes\SPEDAS\pycharm\pyspedas\themis\ -m unittest C:/work/Codes/SPEDAS/pycharm/pyspedas/themis/tests/tests_cal_fit.py
coverage report -m
cd C:/work/Codes/SPEDAS/pycharm/pyspedas/themis/tests/