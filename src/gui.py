################################################################################
# Modules
################################################################################
import math
import xml.etree.ElementTree as ET
import tkinter as tk
import tkinter.filedialog as tkfd

import utils
import logger as lo
import filedialogger as fd

################################################################################
# GUI parameters
################################################################################
LOGS_TEXT_WIDTH = 80

################################################################################
# GUI classes
################################################################################
class GUILogger(lo.Logger):
    """Class for the GUI logger. Inherit from Logger.

    A logger that can display logs through a Text widget.

    Attributes
    ----------
        _text (getter/setter): text widget to display logs
        _linescolumn (getter/setter): text widget to display logs lines numbers
        _paragraph_counter: logs lines numbers counter

    Methods
    -------
        log(str, int) -> void: stack a log from a given message and a given log
                               type and display log in a text widget
    """

    SUCCESS_COLOR = 'green'
    ERROR_COLOR = 'red'
    WARNING_COLOR = 'yellow'

    #---------------------------------------------------------------------------
    def __init__(self):
        lo.Logger.__init__(self)

        self._text = None
        self._linescolumn = None
        self._paragraph_counter = 1
    
    #---------------------------------------------------------------------------
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, p_text):
        assert isinstance(p_text, tk.Text), 'Passed widget must be instance of tkinter Text'
        
        self._text = p_text
    
    @property
    def linescolumn(self):
        return self._linescolumn
    
    @linescolumn.setter
    def linescolumn(self, p_linescolumn):
        assert isinstance(p_linescolumn, tk.Text), 'Passed widget must be instance of tkinter Text'
        
        self._linescolumn = p_linescolumn

    #---------------------------------------------------------------------------
    def log(self, p_msg, p_type=lo.LogType.DEFAULT):
        """Overriding of Logger class log method. Stack a log from a given
        message and a given log type and display it in a text widget.
        """

        # stack log first
        log = lo.Log(p_msg, p_type)
        lo.Logger.stack(self, log)

        # handle displaying then
        if self._text and self._linescolumn:
            # insert log message
            log_line = str(log) + '\n'
            self._text.config(state='normal')
            if (p_type == lo.LogType.SUCCESS):
                self._text.insert('end', log_line, 'success')
            elif (p_type == lo.LogType.ERROR):
                self._text.insert('end', log_line, 'error')
            elif (p_type == lo.LogType.WARNING):
                self._text.insert('end', log_line, 'warning')
            elif (p_type == lo.LogType.ADD):
                self._text.insert('end', log_line, 'add')
            else:
                self._text.insert('end', log_line)
            self._text.config(state='disabled')
            self._text.see('end')
            
            # parse nb of chars of current line to get the nb of lines
            idx = self._text.index(str(self._paragraph_counter) + '.end')
            nbchars = int(idx.split('.')[1])
            nblines = math.ceil(nbchars / LOGS_TEXT_WIDTH)
            
            # insert log line number
            log_number = str(self._paragraph_counter) + '\n' * nblines
            self._linescolumn.config(state='normal')
            self._linescolumn.insert('end', log_number)
            self._linescolumn.config(state='disabled')
            self._linescolumn.see('end')

            self._paragraph_counter += 1

class GUIFileDialogger(fd.FileDialogger):
    """Class for the GUI filedialogger. Inherit from FileDialogger.
    
    A filedialogger that can handle and ask user for files related to Indigo
    Renderer.

    Methods
    -------
        ismaterial(str) -> bool: identify if a given file is a Indigo material
        iscamera(str) -> bool: identify if a given file is a Indigo camera
        isobject(str) -> bool: identify if a given file is a Indigo object
        isscene(str) -> bool: identify if a given file is a Indigo scene
        open_materialsdir() -> list of str: ask to user a directory that
                                            contains Indigo materials
        open_camerasdir() -> list of str: ask to user a directory that
                                          contains Indigo cameras
        open_object() -> str: ask to user a Indigo object file
        open_scene() -> str: ask to user a Indigo scene file
    """

    def __init__(self, p_logger=None):
        assert isinstance(p_logger, GUILogger), 'Passed logger is not an instance of GUILogger'
        
        fd.FileDialogger.__init__(self, p_logger)
    
    #---------------------------------------------------------------------------
    @property
    def logger(self):
        return self._logger
    
    @logger.setter
    def logger(self, p_logger):
        assert isinstance(p_logger, GUILogger), 'Rval is not an instance of GUILogger'

        self._logger = p_logger

    #---------------------------------------------------------------------------
    def ismaterial(self, p_fname):
        """Given a filename, return True if the file is a Indigo material.
        Return False otherwise.
        """

        if not self.isvalidxml(p_fname):
            return False
        
        root = ET.parse(p_fname).getroot()
        
        if not root.tag == 'scenedata' or not root.find('material'):
            # handle exception if an attached logger exists
            if self._logger:
                log_msg = 'File "' + p_fname + '" is not a material file'
                self._logger.log(log_msg, lo.LogType.ERROR)

            return False
        
        return True
    
    def iscamera(self, p_fname):
        """Given a filename, return True if the file is a Indigo camera.
        Return False otherwise.
        """
        
        # TODO: multiple occurences of camera tag is not allowed

        if not self.isvalidxml(p_fname):
            return False
        
        root = ET.parse(p_fname).getroot()
        
        if not root.tag == 'scenedata' or not root.find('camera'):
            # handle exception if an attached logger exists
            if self._logger:
                log_msg = 'File "' + p_fname + '" is not a camera file'
                self._logger.log(log_msg, lo.LogType.ERROR)

            return False
        
        return True
    
    def isobject(self, p_fname):
        """Given a filename, return True if the file is a Indigo object.
        Return False otherwise.
        """

        if not self.isvalidxml(p_fname):
            return False
        
        root = ET.parse(p_fname).getroot()

        if not root.tag == 'scenedata' or not root.find('model2'):
            # handle exception if an attached logger exists
            if self._logger:
                log_msg = 'File "' + p_fname + '" is not an object file'
                self._logger.log(log_msg, lo.LogType.ERROR)

            return False
        
        return True
    
    def isscene(self, p_fname):
        """Given a filename, return True if the file is a Indigo scene.
        Return False otherwise.
        """

        if not self.isvalidxml(p_fname):
            return False
        
        root = ET.parse(p_fname).getroot()

        if not root.tag == 'scene':
            # handle exception if an attached logger exists
            if self._logger:
                log_msg = 'File "' + p_fname + '" is not a scene file'
                self._logger.log(log_msg, lo.LogType.ERROR)

            return False
        
        return True

    def open_materialsdir(self):
        """Ask to user a directory and return a list of existing Indigo
        materials filenames. Return an empty list otherwise.
        """

        matfnames = []
        
        dirname = tkfd.askdirectory()

        if dirname:
            subfnames = self.open_dir(dirname, True)

            if subfnames and self.any_isofextension(subfnames, 'igm'):
                goodfnames = [fname for fname in subfnames
                              if fname.endswith('igm')]

                for fname in goodfnames:
                    if self.ismaterial(fname):
                        matfnames.append(fname)
        
        return matfnames
    
    def open_camerasdir(self):
        """Ask to user a directory and return a list of existing Indigo
        cameras filenames. Return an empty list otherwise.
        """

        camfnames = []
        
        dirname = tkfd.askdirectory()

        if dirname:
            subfnames = self.open_dir(dirname, True)

            if subfnames and self.any_isofextension(subfnames, 'igs'):
                goodfnames = [fname for fname in subfnames
                              if fname.endswith('igs')]

                for fname in goodfnames:
                    if self.iscamera(fname):
                        camfnames.append(fname)
        
        return camfnames

    def open_object(self):
        """Ask to user a Indigo object and return the filename. Return an empty
        string otherwise.
        """

        fname = tkfd.askopenfilename()

        if fname:
            if self.isofextension(fname, 'igs'):
                if self.isobject(fname):
                    return utils.inject_separator(fname)
        
        return ''

    def open_scene(self):
        """Ask to user a Indigo scene and return the filename. Return an empty
        string otherwise.
        """

        fname = tkfd.askopenfilename()

        if fname:
            if self.isofextension(fname, 'igs'):
                if self.isscene(fname):
                    return utils.inject_separator(fname)
        
        return ''

class CustomListbox(tk.Listbox):
    """Class for custom listbox. Inherit from Listbox.
    
    Attributes
    ----------
        _idcounter: count the insertions of items
        _dataitems (readonly): dictionnary that contains data items as materials,
                               models or cameras

    Methods
    -------
        additem(object) -> void: add a data item to the dictionnary and to the
                                 listbox
        setitemcontent(int, str) -> void: set content of a listbox item
        setactive(int) -> void: set active a listbox item
        setunactive(int) -> void: set unactive a listbox item
        clear() -> void: delete all items in the dictionnary and in the listbox
    """

    def __init__(self, master=None, **options):
        tk.Listbox.__init__(self, master, options)

        self._idcounter = 0
        self._dataitems = {}
    
    #---------------------------------------------------------------------------
    @property
    def dataitems(self):
        return self._dataitems

    #---------------------------------------------------------------------------
    def additem(self, p_item):
        """Add a data item to the dictionnary and insert the name of the item
        in the listbox.
        """

        self._dataitems[self._idcounter] = p_item
        self.insert('end', p_item.getname())
        self._idcounter += 1
    
    def setitemcontent(self, p_itemid, p_content):
        """Set content of a listbox item.
        """

        self.delete(p_itemid)
        self.insert(p_itemid, p_content)

    def setactive(self, p_itemid):
        """Set active a listbox item.
        """

        self.itemconfig(p_itemid, {'bg': 'green', 'fg': 'white'})
    
    def setunactive(self, p_itemid):
        """Set unactive a listbox item.
        """

        self.itemconfig(p_itemid, {'bg': '', 'fg': 'black'})

    def clear(self):
        """Delete all items in the dictionnary and all items in the listbox.
        """
        
        self._dataitems = {}
        self.delete('0', 'end')
        self._idcounter = 0

################################################################################
# Main and tests
################################################################################
if __name__ == '__main__':
    pass