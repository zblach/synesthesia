__author__ = 'zblach'


def enum(*sequential, **named):
    return type('Enum', (), dict(zip(sequential, range(len(sequential))), **named))

