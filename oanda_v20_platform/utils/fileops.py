from pathlib import Path


def get_abs_path(pathlist=['oanda_v20_platform', 'data', 'marketdata.db']):
    """To solve the problem of finding files with relative
    paths on windows/linux/mac etc. esp when a module has been 
    imported into a different working directory
    This finds the current working directory cuts it back
    to oanda_v20_platform_public then adds the components of pathlist
    Args:
        pathlist list of str, folder and filenames required
        after oanda_v20_platform
    Returns:
         a pathlib object with the absolute path
        
    """
    p = Path()
    # get the current working dir
    cwd = p.cwd()
    # get the dir tree
    l = list(cwd.parts)
    # shorten it to the oanda_v20_platform root
    l = l[:l.index('oanda_v20_platform_public')+1]
    for x in pathlist:
        l.append(x)
    newpath = Path(*l)

    return newpath.absolute()