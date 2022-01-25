################################################################################
# Modules
################################################################################
import os
import re

################################################################################
# Utilities functions
################################################################################
def parse_exception(p_exception):
    """Parse exception message from passed exception. Return the message.
    """

    return str(p_exception).split('] ')[-1]

def inject_separator(p_string):
    """Inject in a string the os separator. Return the updated filename.
    """

    splitstr = re.split(r'\\|/', p_string)
    splitstr[0] += os.sep

    return os.path.join(*splitstr)

def get_parent_directory(p_filename):
    """Parse and return the parent directory of a given file.
    """

    splitfname = p_filename.split(os.sep)[:-1]
    splitfname[0] += os.sep

    return os.path.join(*splitfname)

################################################################################
# Main and tests
################################################################################
if __name__ == '__main__':
    pass