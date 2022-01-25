################################################################################
# Modules
################################################################################
import xml.etree.ElementTree as ET

################################################################################
# Data classes
################################################################################

# TODO: add NamedTree class, with Material, Camera and Scene inherit from it
#       Scene has to override getname() method though

class XMLTree:
    """Class for XML trees. Store a parsed XML tree and its filename.
    
    Attributes
    ----------
        _tree (readonly): a parsed XML tree
        _basetree (readonly): the base tree of a parsed XML file
        _fname (readonly): the corresponding filename of the XML file
    """

    def __init__(self, p_tree, p_basetree, p_fname):
        assert isinstance(p_tree, ET.Element), 'Passed tree is not an instance of Element'
        self._tree = p_tree
        self._basetree = p_basetree

        self._fname = p_fname
    
    #---------------------------------------------------------------------------
    @property
    def tree(self):
        return self._tree
    
    @property
    def basetree(self):
        return self._basetree
    
    @property
    def fname(self):
        return self._fname

class Material(XMLTree):
    """Class for materials. Inherit from XMLTree.
    
    Methods
    -------
        getname() -> str: gives the name of the material in the tree
    """

    def __init__(self, p_tree, p_basetree, p_fname):
        XMLTree.__init__(self, p_tree, p_basetree, p_fname)
        assert p_tree.tag == 'material', 'Passed tree is not a material'
    
    #---------------------------------------------------------------------------
    def getname(self):
        """Find and return the name of the material in the tree. Return an empty
        string otherwise.
        """

        return self._tree.findtext('name', '')

class Camera(XMLTree):
    """Class for cameras. Inherit from XMLTree.
    
    Methods
    -------
        getname() -> str: gives the name of the camera in the tree
    """

    def __init__(self, p_tree, p_basetree, p_fname):
        XMLTree.__init__(self, p_tree, p_basetree, p_fname)
        assert p_tree.tag == 'camera', 'Passed tree is not a camera'
    
    #---------------------------------------------------------------------------
    def getname(self):
        """Find and return the name of the camera in the tree. Return an empty
        string otherwise.
        """
        
        return self._tree.findtext('name', '')

class Model(XMLTree):
    """Class for models. Inherit from XMLTree.
    
    Attributes
    ----------
        _material (getter/setter): the associated material
        
    Methods
    -------
        getname() -> str: gives the name of the model in the tree
    """

    def __init__(self, p_tree, p_basetree, p_fname):
        XMLTree.__init__(self, p_tree, p_basetree, p_fname)
        assert p_tree.tag == 'model2', 'Passed tree is not a model'

        self._material = None

    #---------------------------------------------------------------------------
    @property
    def material(self):
        return self._material
    
    @material.setter
    def material(self, p_material):
        assert isinstance(p_material, Material), 'Rval is not an instance of Material'
        self._material = p_material

    #---------------------------------------------------------------------------
    def getname(self):
        """Find and return the name of the model in the tree. Return an empty
        string otherwise.
        """
        
        return self._tree.findtext('name', '')

class Scene(XMLTree):
    """Class for scenes. Inherit from XMLTree.
    
    Attributes
    ----------
        _camera (getter/setter): the associated camera

    Methods
    -------
        getname() -> str: gives the name of the scene in the tree
    """

    def __init__(self, p_tree, p_basetree, p_fname):
        XMLTree.__init__(self, p_tree, p_basetree, p_fname)
        assert p_tree.tag == 'scene', 'Passed tree is not a scene'

        self._camera = None
    
    #---------------------------------------------------------------------------
    @property
    def camera(self):
        return self._camera
    
    @camera.setter
    def camera(self, p_camera):
        assert isinstance(p_camera, Camera), 'Rval is not an instance of Camera'
        self._camera = p_camera

    #---------------------------------------------------------------------------
    def getname(self):
        """Find and return the name of the scene in the tree. Return an empty
        string otherwise.
        """

        return self._tree.find('metadata').findtext('scene_name', '')

################################################################################
# Main and tests
################################################################################
if __name__ == '__main__':
    pass