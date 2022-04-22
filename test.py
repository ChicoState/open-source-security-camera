import environ as Environ

if '__name__' == '__main__':
    envirionment = Environ.Env()
    Environ.Env.read_env()
    key = envirionment('EMAIL')
