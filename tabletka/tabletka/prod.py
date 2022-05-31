import dj_database_url

DATABASES = {'default': dj_database_url.config(
    default='postgres://cyigdohhawhjdg:a463caf6f526cb07e22505e3b531b3bfcc3ffb3b20b91624eec25ad277313261@ec2-52-18-116-67.eu-west-1.compute.amazonaws.com:5432/delac70srfmee6')}
