class AlreadyNamedException(Exception):
    """
    """
    def __init__(self, fn):
        msg = "Already in correct naming format: "+fn
        
        print msg
    
class UnexpectedFormatException(Exception):
    """
    """
    def __init__(self, fn):
        msg = "The file was in an unexpected format: "+fn
        print msg
    
class EpisodeNotFoundException(Exception):
    """
    """
    def __init__(self, fn):
        msg = "Episode could not be found: "+fn
        print msg
