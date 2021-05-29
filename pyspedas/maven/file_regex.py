import re

# kp pattern
kp_pattern = (r'^mvn_(?P<{0}>kp)_'
              '(?P<{1}>insitu|iuvs)'
              '(?P<{2}>|_[a-zA-Z0-9\-]+)_'
              '(?P<{3}>[0-9]{{4}})'
              '(?P<{4}>[0-9]{{2}})'
              '(?P<{5}>[0-9]{{2}})'
              '(?P<{6}>|[t|T][0-9]{{6}})_'
              'v(?P<{7}>[0-9]+)_r(?P<{8}>[0-9]+)\.'
              '(?P<{9}>tab)'
              '(?P<{10}>\.gz)*').format('instrument',
                                        'level',
                                        'description',
                                        'year',
                                        'month',
                                        'day',
                                        'time',
                                        'version',
                                        'revision',
                                        'extension',
                                        'gz')

kp_regex = re.compile(kp_pattern)

l2_pattern = (r'^mvn_(?P<{0}>[a-zA-Z0-9]+)_'
              '(?P<{1}>l[a-zA-Z0-9]+)'
              '(?P<{2}>|_[a-zA-Z0-9\-]+)_'
              '(?P<{3}>[0-9]{{4}})'
              '(?P<{4}>[0-9]{{2}})'
              '(?P<{5}>[0-9]{{2}})'
              '(?P<{6}>|T[0-9]{{6}}|t[0-9]{{6}})_'
              'v(?P<{7}>[0-9]+)_'
              'r(?P<{8}>[0-9]+)\.'
              '(?P<{9}>cdf|xml|sts|md5)'
              '(?P<{10}>\.gz)*').format('instrument',
                                        'level',
                                        'description',
                                        'year',
                                        'month',
                                        'day',
                                        'time',
                                        'version',
                                        'revision',
                                        'extension',
                                        'gz')
l2_regex = re.compile(l2_pattern)