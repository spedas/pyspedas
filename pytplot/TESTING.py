import pydivide
pydivide.download_files(start_date='2015-12-25',end_date='2015-12-27')
pydivide.download_files(start_date='2015-12-25',end_date='2015-12-27',iuvs=True)
insitu,iuvs = pydivide.read('2015-12-26')

insitu2 = pydivide.insitu_search(insitu, 'inbound')