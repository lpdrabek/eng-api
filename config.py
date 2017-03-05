db_user = ''
db_pass = ''
db_host = ''
db_name = ''

SECRET_KEY = ''
SQLALCHEMY_DATABASE_URI='mysql://{usr}:{pwd}@{host}/{db}'.format(usr=db_user,
                                                                 pwd=db_pass,
                                                                 host=db_host,
                                                                 db=db_name)
