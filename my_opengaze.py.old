from opengaze import OpenGazeTracker

class MyOpenGazeTracker(OpenGazeTracker, object):
    def __init__(self,
                 samplerHandler,
                 *args,
                 **kwargs):
        self._log_sample = samplerHandler
        super(MyOpenGazeTracker, self).__init__(*args, **kwargs)    
