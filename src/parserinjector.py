################################################################################
# Modules
################################################################################
import copy
import xml.etree.ElementTree as ET

import utils
import logger as lo
import data
import gui

################################################################################
# ParserInjector class
################################################################################

# TODO: rework ParserInjector class

class ParserInjector:
    """Class of the parser/injector.

    Attributes
    ----------

    Methods
    -------
    """
    
    _matuid = 50

    #---------------------------------------------------------------------------
    def __init__(self, p_logger=None):
        if p_logger:
            assert isinstance(p_logger, gui.GUILogger), 'Passed logger is not an instance of GUILogger'
            self._logger = p_logger
        else:
            self._logger = None

        self._materials = []
        self._cameras = []
        self._models = []

        self._listbox_models = None
        self._listbox_materials = None
        self._listbox_cameras = None

        self.scene = None
        self.packshotdest = ''
    
    #---------------------------------------------------------------------------
    @property
    def logger(self):
        return self._logger
    
    @logger.setter
    def logger(self, p_logger):
        assert isinstance(p_logger, gui.GUILogger), 'Rval is not an instance of GUILogger'
        self._logger = p_logger

    @property
    def materials(self):
        return self._materials
    
    @property
    def cameras(self):
        return self._cameras
    
    @property
    def models(self):
        return self._models

    @property
    def listbox_models(self):
        return self._listbox_models
    
    @listbox_models.setter
    def listbox_models(self, p_listbox_models):
        assert isinstance(p_listbox_models, gui.CustomListbox), 'Rval is not an instance of tkinter CustomListbox'
        self._listbox_models = p_listbox_models
    
    @property
    def listbox_materials(self):
        return self._listbox_materials
    
    @listbox_materials.setter
    def listbox_materials(self, p_listbox_materials):
        assert isinstance(p_listbox_materials, gui.CustomListbox), 'Rval is not an instance of tkinter CustomListbox'
        self._listbox_materials = p_listbox_materials
    
    @property
    def listbox_cameras(self):
        return self._listbox_cameras
    
    @listbox_cameras.setter
    def listbox_cameras(self, p_listbox_cameras):
        assert isinstance(p_listbox_cameras, gui.CustomListbox), 'Rval is not an instance of tkinter CustomListbox'
        self._listbox_cameras = p_listbox_cameras

    #---------------------------------------------------------------------------
    def parse_material(self, p_fname):
        """"""

        # TODO: parse complex materials

        tree = ET.parse(p_fname)
        root = tree.getroot()

        material = data.Material(root.find('material'), tree, p_fname)
        self._materials.append(material)

        # handle valid operation if an attached logger exists
        if self._logger:
            log_msg = ('Material "' + material.getname() +
                       '" is successfully added')
            self._logger.log(log_msg, lo.LogType.ADD)

    def parse_camera(self, p_fname):
        """"""

        tree = ET.parse(p_fname)
        root = tree.getroot()

        camera = data.Camera(root.find('camera'), tree, p_fname)
        self._cameras.append(camera)

        # handle valid operation if an attached logger exists
        if self._logger:
            log_msg = ('Camera "' + camera.getname() +
                       '" is successfully added')
            self._logger.log(log_msg, lo.LogType.ADD)

    def parse_models(self, p_fname):
        """"""

        tree = ET.parse(p_fname)
        root = tree.getroot()

        for nei in root.iter('model2'):
            model = data.Model(nei, tree, p_fname)
            self._models.append(model)

            # handle valid operation if an attached logger exists
            if self._logger:
                log_msg = ('Model "' + model.getname() +
                           '" is successfully added')
                self._logger.log(log_msg, lo.LogType.ADD)

    def parse_scene(self, p_fname):
        """"""

        tree = ET.parse(p_fname)
        root = tree.getroot()

        self.scene = data.Scene(root, tree, p_fname)

        # handle valid operation if an attached logger exists
        if self._logger:
            log_msg = ('Scene "' + self.scene.getname() +
                       '" is successfully added')
            self._logger.log(log_msg, lo.LogType.ADD)
    
    def empty_materials(self):
        """"""
        
        self._materials = []

        if self._listbox_materials:
            self._listbox_materials.clear()

    def empty_cameras(self):
        """"""
        
        self._cameras = []

        if self._listbox_cameras:
            self._listbox_cameras.clear()

    def empty_models(self):
        """"""
        
        self._models = []

        if self._listbox_models:
            self._listbox_models.clear()
    
    def inject_materials(self):
        """"""

        objbasetree = self._models[0].basetree
        root = objbasetree.getroot()
        
        # inject assigned materials
        for model in self._models:
            # insert uid tag in material
            new_uid_tag = ET.Element('uid')
            new_uid_tag.text = str(ParserInjector._matuid)
            dup_mattree = copy.deepcopy(model.material.tree)
            dup_mattree.insert(0, new_uid_tag)

            # insert material in object tree
            root.insert(0, dup_mattree)

            # update model material uid
            model_matuid_tag = model.tree.find('materials').find('uid')
            model_matuid_tag.text = str(ParserInjector._matuid)
            ParserInjector._matuid += 1

    def inject_camera(self):
        """"""

        include_tag = ET.Element('include')
        pathname_tag = ET.SubElement(include_tag, 'pathname')
        pathname_tag.text = self.scene.camera.fname
        self.scene.tree.insert(0, include_tag)
    
    def inject_object(self):
        """"""

        objfname = self._models[0].fname
        include_tag = ET.Element('include')
        pathname_tag = ET.SubElement(include_tag, 'pathname')
        pathname_tag.text = objfname[:-4] + '_new.igs'
        self.scene.tree.insert(1, include_tag)
    
    def write_treesfiles(self):
        """"""

        objfname = self._models[0].fname
        objbasetree = self._models[0].basetree
        scenefname = self.scene.fname
        scenebasetree = self.scene.basetree

        out_objfname = objfname[:-4] + '_new.igs'
        out_scenefname = scenefname[:-4] + '_new.igs'

        try:
            objbasetree.write(out_objfname)
            scenebasetree.write(out_scenefname)
        except Exception as e:
            # handle exception if there is an existing logger
            if self._logger:
                log_msg = utils.parse_exception(e)
                self._logger.log(log_msg, lo.LogType.ERROR)
            
            return ''
        
        return out_scenefname

################################################################################
# Main and tests
################################################################################
if __name__ == '__main__':
    pass