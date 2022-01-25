################################################################################
# Modules
################################################################################
from datetime import datetime
import enum

################################################################################
# Logger classes
################################################################################
class LogType(enum.Enum):
    """Enumerator for log type.
    
    According to the type, logs might be handled or displayed in a different
    way. See Log class for more information.
    """

    DEFAULT = 1
    SUCCESS = 2
    ERROR = 3
    WARNING = 4
    ADD = 5

class Log:
    """Class for logs. A log store a message and its type.

    Attributes
    ----------
        _msg (readonly): the log message
        _type (readonly): the type of the log (see LogType class).
    """

    _DEFAULT_TAG = ''
    _SUCCESS_TAG = '[OK] '
    _WARNING_TAG = '[!] '
    _ERROR_TAG = '[Error] '
    _ADD_TAG = '[+] '

    #---------------------------------------------------------------------------
    def __init__(self, p_msg, p_type=LogType.DEFAULT):
        self._msg = p_msg
        self._type = p_type

    def __str__(self):
        if self._type == LogType.SUCCESS:
            return (Log._SUCCESS_TAG + self._msg)
        elif self._type == LogType.ERROR:
            return (Log._ERROR_TAG + self._msg)
        elif self._type == LogType.WARNING:
            return (Log._WARNING_TAG + self._msg)
        elif self._type == LogType.ADD:
            return (Log._ADD_TAG + self._msg)
        return (Log._DEFAULT_TAG + self._msg)
    
    #---------------------------------------------------------------------------
    @property
    def msg(self):
        return self._msg
    
    @property
    def type(self):
        return self._type

class Logger:
    """Class for loggers. A logger stores logs in a stack.

    Attributes
    ----------
        _stack: a stack of logs
    
    Methods
    -------
        log(str, int) -> void: stack a log from a given message and a given log
                               type
        stack(Log) -> void: stack a given log
        unstack() -> Log: unstack and return last log
        unstack_all() -> list of Log: unstack entirely the stack
        write() -> void: write the entire stack in a file
    """

    def __init__(self):
        self._stack = []
    
    #---------------------------------------------------------------------------
    def log(self, p_msg, p_type=LogType.DEFAULT):
        """Store at the head of the stack a log from a given message and a given
        log type.
        """
        
        self._stack.append(Log(p_msg, p_type))

    def stack(self, p_log):
        """Store at the head of the stack a given log.
        """
        
        self._stack.append(p_log)

    def unstack(self):
        """Pop a log from the head of the stack and return it.
        """

        log = None

        try:
            log = self._stack.pop()
        except IndexError: pass
        
        return log
    
    def unstack_all(self):
        """Pop all logs from the stack from the head and return a list that
        contain all the logs.
        """

        logs = []
        unstoppopable = True

        while unstoppopable:
            try:
                logs.append(self._stack.pop())
            except IndexError:
                unstoppopable = False
        
        return logs
    
    def write(self, p_filename='logs.txt'):
        """Write in a file all logs that are contained in the stack.
        """

        if self._stack:
            with open(p_filename, 'a') as f:
                # write banner with current date and time
                now = datetime.now()
                strnow = now.strftime('%Y/%d/%m %H:%M')
                f.write('---- ' + strnow + ' ----\n')

                # write logs
                for log in self._stack:
                    f.write(log.msg + '\n')
                
                f.write('\n')

################################################################################
# Main and tests
################################################################################
if __name__ == '__main__':
    pass