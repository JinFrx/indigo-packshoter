################################################################################
# Modules
################################################################################
import os
import xml.etree.ElementTree as ET

import utils
import logger as lo

################################################################################
# FileDialogger class
################################################################################
class FileDialogger:
    """Class for filedialogger. A filedialogger is in charge of dialogging with
    the file system.
    
    Attributes
    ----------
        _logger (getter/setter): attached logger to handle exceptions
    
    Methods
    -------
        isofextension(str, str) -> bool: identify if a file has the correct
                                         extension
        any_isofextension(list of str, str) -> bool: identify if any of given
                                                     files has the correct
                                                     extension
        isvalidxml(str) -> bool: identify if a file can be parsed as a XML file
        open_dir(str, bool) -> list of str: give all subfiles of a given
                                            directory
    """
    
    #---------------------------------------------------------------------------
    def __init__(self, p_logger=None):
        self._logger = p_logger
    
    #---------------------------------------------------------------------------
    @property
    def logger(self):
        return self._logger
    
    @logger.setter
    def logger(self, p_logger):
        # as a base class, this setter is useless
        self._logger = p_logger

    #---------------------------------------------------------------------------
    def isofextension(self, p_fname, p_ext):
        """Given a filename, return True if the file has the correct extension.
        Return False otherwise.
        """

        if not p_fname.endswith(p_ext):
            # handle exception if an attached logger exists
            if self._logger:
                log_msg = ('File "' + p_fname + '" not in valid format "' +
                           p_ext + '"')
                self._logger.log(log_msg, lo.LogType.ERROR)

            return False
        
        return True
    
    def any_isofextension(self, p_fnames, p_ext):
        """Given multiple filenames, return True if there is at least one file
        that has the correct extension. Return False otherwise.
        """

        for fname in p_fnames:
            if fname.endswith(p_ext):
                return True

        # handle exception if an attached logger exists
        if self._logger:
            log_msg = 'No files were found with valid format "' + p_ext + '"'
            self._logger.log(log_msg, lo.LogType.ERROR)

        return False
    
    def isvalidxml(self, p_fname):
        """Return True if a file can be parsed as a XML file. Return False
        otherwise.
        """

        try:
            ET.parse(p_fname)
        except Exception as e:
            # handle exception if an attached logger exists
            if self._logger:
                e_msg = utils.parse_exception(e).capitalize()
                log_msg = 'From file "' + p_fname + '": ' + e_msg
                self._logger.log(log_msg, lo.LogType.ERROR)
            
            return False
        
        return True
    
    def open_dir(self, p_dirname, p_notempty=False):
        """Read a directory and return a list of existing subfilesnames. Return
        an empty list otherwise.

        Parameters
        ----------
        bool p_notempty: ensure that the directory must not be empty
        """
        
        if not os.path.isdir(p_dirname):
            # handle exception if an attached logger exists
            if self._logger:
                log_msg = '"' + p_dirname + '" is not a directory'
                self._logger.log(log_msg, lo.LogType.ERROR)

            return []
        
        subfnames = os.listdir(p_dirname)

        if p_notempty and not subfnames:
            # handle exception if an attached logger exists
            if self._logger:
                log_msg = 'Directory "' + p_dirname + '" is empty'
                self._logger.log(log_msg, lo.LogType.ERROR)

            return []
        
        # return complete files names
        return [utils.inject_separator(os.path.join(p_dirname, fname)) for fname
                in subfnames]
    
################################################################################
# Main and tests
################################################################################
if __name__ == '__main__':
    pass