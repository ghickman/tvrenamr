class AlreadyNamedException(Exception):
    """
    Raised when the format of the file being passed in is the same as the output format
    """
    def __init__(self,fn):
        msg = "Already in correct naming format: "+fn
        print msg
    
class UnexpectedFormatException(Exception):
    """
    """
    def __init__(self,fn):
        msg = "The file was in an unexpected format: "+fn
        print msg
    
class EpisodeNotFoundException(Exception):
    """
    """
    def __init__(self,fn):
        msg = "Episode could not be found: "+fn
        print msg
    
class EpisodeAlreadyExistsInFolderException(Exception):
    """
    """
    def __init__(self,fn,new_fn):
        msg = "An episode called \'"+fn+"\' already exists in the current folder"
        print msg
    
class ShowNotFoundException(Exception):
    """
    """
    def __init__(self,show):
        msg = show+" could not be found"
        print msg
    
class EpisodeNotFoundException(Exception):
    """
    """
    def __init__(self,episode):
        msg = episode+" could not be found"
        print msg