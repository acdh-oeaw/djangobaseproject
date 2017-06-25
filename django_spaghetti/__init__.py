__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 0,
    'releaselevel': 'final',
    'serial': 0
}


def get_version(release_level=True):
    """
    Return the formatted version information
    """
    version = ["%(major)i.%(minor)i.%(micro)i" % __version_info__]
    if release_level and __version_info__['releaselevel'] != 'final':
        version.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(version)

__version__ = get_version()
