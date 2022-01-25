################################################################################
# Modules
################################################################################
import os
import subprocess
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
from tkinter import scrolledtext

import utils
import logger as lo
import gui
import parserinjector

################################################################################
# Application class
################################################################################

# TODO: rework Application class
# TODO: add a common binding for y scrolling on text-logs and text-logs-lines widgets

class Application(tk.Tk):
    """Class of the application. Inherit from Tk.
    
    Attributes
    ----------

    Methods
    -------
    """

    def __init__(self):
        tk.Tk.__init__(self)

        self._logger = gui.GUILogger()
        self._fd = gui.GUIFileDialogger(self._logger)
        self._parser = parserinjector.ParserInjector(self._logger)

        self._indigo_exe_path = ''
        self._halt = 1
        self._activemodelid = None
        self._activematerialid = None
        self._activecameraid = None

        self._init_window()
        self._init_widgets()
        self._set_bindings()
        
    #---------------------------------------------------------------------------
    def _init_window(self):
        """Initialize the main frame of the application which contains widgets.
        """

        self._win = tk.Frame(self)
        self._win.grid(padx=5, pady=5)
        self._win.grid_rowconfigure(0, weight=0)
        self._win.grid_rowconfigure(1, weight=0)
        self._win.grid_rowconfigure(2, weight=0)
        self._win.grid_rowconfigure(3, weight=0)
        self._win.grid_rowconfigure(4, weight=0)
        self._win.grid_rowconfigure(5, weight=1)
        self._win.grid_rowconfigure(6, weight=0)
        self._win.grid_rowconfigure(7, weight=0)
        self._win.grid_rowconfigure(8, weight=0)
        self._win.grid_rowconfigure(9, weight=0)
        self._win.grid_rowconfigure(10, weight=1)
        self._win.grid_rowconfigure(11, weight=0)
        self._win.grid_columnconfigure(0, weight=0)
        self._win.grid_columnconfigure(1, weight=1)

    def _init_widgets(self):
        """Initialize all of the application widgets.
        """
        
        # widgets creation
        self._widgets = {
            'button-open-materialsdir': tk.Button(self._win),
            'button-open-object': tk.Button(self._win),
            'button-open-scene': tk.Button(self._win),
            'button-open-camerasdir': tk.Button(self._win),
            'button-set-packshotdir': tk.Button(self._win),
            'button-set-exe': tk.Button(self._win),
            'frame-logs': tk.Frame(self._win),
            'sep-middle': ttk.Separator(self._win),
            'button-active-model': tk.Button(self._win),
            'button-active-material': tk.Button(self._win),
            'button-assign-material': tk.Button(self._win),
            'button-assign-camera': tk.Button(self._win),
            'frame-render': tk.Frame(self._win),
            'frame-items': tk.Frame(self._win),
        }
        self._widgets['text-logs-lines'] = tk.Text(self._widgets['frame-logs'])
        self._widgets['text-logs'] = scrolledtext.ScrolledText(self._widgets['frame-logs'])

        self._widgets['label-halt'] = tk.Label(self._widgets['frame-render'])
        self._widgets['entry-halt'] = tk.Entry(self._widgets['frame-render'])
        self._widgets['button-render'] = tk.Button(self._widgets['frame-render'])

        self._widgets['frame-models'] = tk.Frame(self._widgets['frame-items'])
        self._widgets['label-models'] = tk.Label(self._widgets['frame-models'])
        self._widgets['listbox-models'] = gui.CustomListbox(self._widgets['frame-models'])
        self._widgets['scrollbar-models'] = tk.Scrollbar(self._widgets['frame-models'])

        self._widgets['frame-materials'] = tk.Frame(self._widgets['frame-items'])
        self._widgets['label-materials'] = tk.Label(self._widgets['frame-materials'])
        self._widgets['listbox-materials'] = gui.CustomListbox(self._widgets['frame-materials'])
        self._widgets['scrollbar-materials'] = tk.Scrollbar(self._widgets['frame-materials'])

        self._widgets['frame-cameras'] = tk.Frame(self._widgets['frame-items'])
        self._widgets['label-cameras'] = tk.Label(self._widgets['frame-cameras'])
        self._widgets['listbox-cameras'] = gui.CustomListbox(self._widgets['frame-cameras'])
        self._widgets['scrollbar-cameras'] = tk.Scrollbar(self._widgets['frame-cameras'])

        # widgets configuration
        self._widgets['button-open-materialsdir'].config(
            text='Open Materials Directory',
            command=self._command_open_materialsdir
        )

        self._widgets['button-open-camerasdir'].config(
            text='Open Cameras Directory',
            command=self._command_open_camerasdir
        )

        self._widgets['button-open-object'].config(
            text='Open Object File',
            command=self._command_open_object
        )

        self._widgets['button-open-scene'].config(
            text='Open Scene File',
            command=self._command_open_scene
        )

        self._widgets['button-set-packshotdir'].config(
            text='Set Packshot Directory',
            command=self._command_set_packshotdir
        )

        self._widgets['button-set-exe'].config(
            text='Set Console Executable',
            command=self._command_set_executable
        )

        self._widgets['text-logs-lines'].config(
            width=3,
            state='disabled'
        )
        
        self._logger.linescolumn = self._widgets['text-logs-lines']

        self._widgets['text-logs'].config(
            width=gui.LOGS_TEXT_WIDTH,
            state='disabled'
        )
        self._widgets['text-logs'].tag_config('success', foreground=gui.GUILogger.SUCCESS_COLOR)
        self._widgets['text-logs'].tag_config('error', foreground=gui.GUILogger.ERROR_COLOR)
        self._widgets['text-logs'].tag_config('warning', foreground=gui.GUILogger.WARNING_COLOR)
        self._widgets['text-logs'].tag_config('add', foreground=gui.GUILogger.SUCCESS_COLOR)
        
        self._logger.text = self._widgets['text-logs']

        self._widgets['sep-middle'].config(orient='horizontal')
        
        self._widgets['button-active-model'].config(
            text='Set Active Model',
            command=self._command_active_model
        )

        self._widgets['button-active-material'].config(
            text='Set Active Material',
            command=self._command_active_material
        )

        self._widgets['button-assign-material'].config(
            text='Assign Material to Model',
            command=self._command_assign_material
        )

        self._widgets['button-assign-camera'].config(
            text='Assign Camera to Scene',
            command=self._command_assign_camera
        )

        self._widgets['label-halt'].config(text='Halt (sec):')

        self._widgets['entry-halt'].config(
            width=4,
            validate='key',
            vcmd=(self.register(self._command_validate_halt), '%P')
        )
        self._widgets['entry-halt'].insert(0, str(self._halt))

        self._widgets['button-render'].config(
            text='Render Packshot',
            command=self._command_render
        )

        self._widgets['label-models'].config(text='Models:')

        self._widgets['listbox-models'].config(
            yscrollcommand=self._widgets['scrollbar-models'].set
        )
        self._parser.listbox_models = self._widgets['listbox-models']

        self._widgets['scrollbar-models'].config(
            command=self._widgets['listbox-models'].yview
        )

        self._widgets['label-materials'].config(text='Materials:')

        self._widgets['listbox-materials'].config(
            yscrollcommand=self._widgets['scrollbar-materials'].set
        )
        self._parser.listbox_materials = self._widgets['listbox-materials']

        self._widgets['scrollbar-materials'].config(
            command=self._widgets['listbox-materials'].yview
        )

        self._widgets['label-cameras'].config(text='Cameras:')

        self._widgets['listbox-cameras'].config(
            yscrollcommand=self._widgets['scrollbar-cameras'].set
        )
        self._parser.listbox_cameras = self._widgets['listbox-cameras']

        self._widgets['scrollbar-cameras'].config(
            command=self._widgets['listbox-cameras'].yview
        )

        # widgets placement
        self._widgets['button-open-materialsdir'].grid(
            row=0, column=0,
            padx=(5, 6), pady=(5, 5),
            sticky='n'
        )

        self._widgets['button-open-camerasdir'].grid(
            row=1, column=0,
            padx=(5, 10), pady=(0, 5),
            sticky='n'
        )

        self._widgets['button-open-object'].grid(
            row=2, column=0,
            padx=(5, 10), pady=(0, 5),
            sticky='n'
        )

        self._widgets['button-open-scene'].grid(
            row=3, column=0,
            padx=(5, 10), pady=(0, 5),
            sticky='n'
        )

        self._widgets['button-set-packshotdir'].grid(
            row=4, column=0,
            padx=(5, 10), pady=(0, 5),
            sticky='n'
        )

        self._widgets['button-set-exe'].grid(
            row=5, column=0,
            padx=(5, 10),
            sticky='n'
        )

        self._widgets['frame-logs'].grid(
            row=0, column=1,
            rowspan=6,
            padx=(0, 5), pady=(5, 5),
            sticky='nsew'
        )
        self._widgets['frame-logs'].grid_columnconfigure(0, weight=0)
        self._widgets['frame-logs'].grid_columnconfigure(1, weight=1)

        self._widgets['text-logs-lines'].grid(
            row=0, column=0,
            sticky='ns'
        )

        self._widgets['text-logs'].grid(
            row=0, column=1,
            sticky='nsew'
        )

        self._widgets['sep-middle'].grid(
            row=6, column=0,
            columnspan=2,
            padx=5, pady=(0, 5),
            sticky='nsew'
        )
        
        self._widgets['button-active-model'].grid(
            row=7, column=0,
            padx=(5, 10), pady=(0, 5) ,
            sticky='n'
        )

        self._widgets['button-active-material'].grid(
            row=8, column=0,
            padx=(5, 10), pady=(0, 5) ,
            sticky='n'
        )

        self._widgets['button-assign-material'].grid(
            row=9, column=0,
            padx=(5, 10), pady=(0, 5) ,
            sticky='n'
        )

        self._widgets['button-assign-camera'].grid(
            row=10, column=0,
            padx=(5, 10), pady=(0, 5),
            sticky='n'
        )

        self._widgets['frame-render'].grid(
            row=11, column=0,
            padx=(5, 10), pady=(0, 5),
            sticky='nsew'
        )
        
        self._widgets['label-halt'].grid(
            row=0, column=0
        )

        self._widgets['entry-halt'].grid(
            row=1, column=0,
            padx=(0, 5)
        )

        self._widgets['button-render'].grid(
            row=1, column=1,
        )

        self._widgets['frame-items'].grid(
            row=7, column=1,
            rowspan=6, columnspan=2,
            padx=(0, 5), pady=(0, 5),
            sticky='nsew'
        )
        self._widgets['frame-items'].grid_columnconfigure(0, weight=1)
        self._widgets['frame-items'].grid_columnconfigure(1, weight=1)
        self._widgets['frame-items'].grid_columnconfigure(2, weight=1)

        self._widgets['frame-models'].grid(
            row=0, column=0,
            sticky='nsew'
        )
        self._widgets['frame-models'].grid_columnconfigure(0, weight=1)
        self._widgets['frame-models'].grid_columnconfigure(1, weight=0)

        self._widgets['label-models'].grid(
            row=0, column=0,
            sticky='w'
        )

        self._widgets['listbox-models'].grid(
            row=1, column=0,
            sticky='nsew'
        )

        self._widgets['scrollbar-models'].grid(
            row=1, column=1,
            padx=(0, 5),
            sticky='ns'
        )

        self._widgets['frame-materials'].grid(
            row=0, column=1,
            sticky='nsew'
        )
        self._widgets['frame-materials'].grid_columnconfigure(0, weight=1)
        self._widgets['frame-materials'].grid_columnconfigure(1, weight=0)

        self._widgets['label-materials'].grid(
            row=0, column=0,
            sticky='w'
        )

        self._widgets['listbox-materials'].grid(
            row=1, column=0,
            sticky='nsew'
        )

        self._widgets['scrollbar-materials'].grid(
            row=1, column=1,
            padx=(0, 5),
            sticky='ns'
        )

        self._widgets['frame-cameras'].grid(
            row=0, column=2,
            sticky='nsew'
        )
        self._widgets['frame-cameras'].grid_columnconfigure(0, weight=1)
        self._widgets['frame-cameras'].grid_columnconfigure(1, weight=0)

        self._widgets['label-cameras'].grid(
            row=0, column=0,
            sticky='w'
        )

        self._widgets['listbox-cameras'].grid(
            row=1, column=0,
            sticky='nsew'
        )

        self._widgets['scrollbar-cameras'].grid(
            row=1, column=1,
            sticky='ns'
        )
    
    def _set_bindings(self):
        """Set all bindings in the application.
        """

        self.protocol('WM_DELETE_WINDOW', self._on_closing)

        #self._widgets['text-logs-lines'].bind('<MouseWheel>', self._on_mousewheel)
        #self._widgets['text-logs'].bind('<MouseWheel>', self._on_mousewheel)

    #---------------------------------------------------------------------------
    # Buttons commands
    #---------------------------------------------------------------------------
    def _command_open_materialsdir(self):
        """"""

        matfnames = self._fd.open_materialsdir()

        if matfnames:
            # delete existing materials
            self._parser.empty_materials()

            for fname in matfnames:
                self._parser.parse_material(fname)

            # add in listbox if it exists
            if self._parser.listbox_materials:
                for mat in self._parser.materials:
                    self._parser.listbox_materials.additem(mat)
    
    def _command_open_camerasdir(self):
        """"""

        camfnames = self._fd.open_camerasdir()

        if camfnames:
            # delete existing cameras
            self._parser.empty_cameras()

            for fname in camfnames:
                self._parser.parse_camera(fname)
            
            # add in listbox if it exists
            if self._parser.listbox_cameras:
                for cam in self._parser.cameras:
                    self._parser.listbox_cameras.additem(cam)

    def _command_open_object(self):
        """"""

        fname = self._fd.open_object()

        if fname:
            # delete existing models
            self._parser.empty_models()

            self._parser.parse_models(fname)

            # add in listbox if it exists
            if self._parser.listbox_models:
                for model in self._parser.models:
                    self._parser.listbox_models.additem(model)
    
    def _command_open_scene(self):
        """"""

        fname = self._fd.open_scene()

        if fname:
            # delete existing scene
            self._parser.scene = None

            self._parser.parse_scene(fname)
    
    def _command_set_packshotdir(self):
        """"""

        dirname = tkfd.askdirectory(mustexist=True)
        
        if dirname:
            correct_dirname = utils.inject_separator(dirname)

            # add new log for valid operation
            log_msg = ('Packshot destination is successfuly set at "' +
                       correct_dirname + '"')
            self._logger.log(log_msg, lo.LogType.SUCCESS)

            self._parser.packshotdest = correct_dirname
    
    def _command_set_executable(self):
        """"""

        fname = tkfd.askopenfilename()

        if fname:
            if self._fd.isofextension(fname, 'exe'):
                self._indigo_exe_path = r'"' + utils.inject_separator(fname) + r'"'

                log_msg = 'Indigo Renderer Console executable is successfuly set'
                self._logger.log(log_msg, lo.LogType.SUCCESS)

    def _command_active_model(self):
        """"""

        itemid = self._widgets['listbox-models'].curselection()

        # check in order to differentiate listboxes selections 
        if itemid:
            # unset previous active model if it exists
            if self._activemodelid != None:
                self._widgets['listbox-models'].setunactive(self._activemodelid)

            # set active current model
            self._activemodelid = itemid[0]
            self._widgets['listbox-models'].setactive(itemid[0])
            
            # add new log for valid operation
            activemodel = self._widgets['listbox-models'].dataitems[itemid[0]]
            log_msg = ('Set active model "' +
                       activemodel.getname() + '"')
            self._logger.log(log_msg, lo.LogType.SUCCESS)
            
    def _command_active_material(self):
        """"""

        itemid = self._widgets['listbox-materials'].curselection()

        # check in order to differentiate listboxes selections 
        if itemid:
            # unset previous active material if it exists
            if self._activematerialid != None:
                self._widgets['listbox-materials'].setunactive(self._activematerialid)

            # set active current material
            self._activematerialid = itemid[0]
            self._widgets['listbox-materials'].setactive(itemid[0])

            # add new log for valid operation
            activematerial = self._widgets['listbox-materials'].dataitems[itemid[0]]
            log_msg = ('Set active material "' +
                       activematerial.getname() + '"')
            self._logger.log(log_msg, lo.LogType.SUCCESS)

    def _command_assign_material(self):
        """"""

        if self._activemodelid != None and self._activematerialid != None:
            # assign active material to active model
            activemodel = self._widgets['listbox-models'].dataitems[self._activemodelid]
            activematerial = self._widgets['listbox-materials'].dataitems[self._activematerialid]
            activemodel.material = activematerial
            newitemtext = (activemodel.getname() + ' [' +
                           activematerial.getname() + ']')
            self._widgets['listbox-models'].setitemcontent(self._activemodelid,
                                                           newitemtext)

            # reset active current active model
            self._widgets['listbox-models'].setactive(self._activemodelid)

            # add new log for valid operation
            log_msg = ('Assigned material "' + activematerial.getname() +
                       '" to model "' + activemodel.getname() + '"')
            self._logger.log(log_msg, lo.LogType.SUCCESS)
    
    def _command_assign_camera(self):
        """"""

        itemid = self._widgets['listbox-cameras'].curselection()

        # check in order to differentiate listboxes selections
        # and if there is a scene set
        if itemid and self._parser.scene:
            camera = self._widgets['listbox-cameras'].dataitems[itemid[0]]
            self._parser.scene.camera = camera

            # unset previous active camera if it exists
            if self._activecameraid != None:
                prevcam = self._widgets['listbox-cameras'].dataitems[self._activecameraid]
                self._widgets['listbox-cameras'].setitemcontent(self._activecameraid,
                                                                prevcam.getname())

            # set active current camera
            self._activecameraid = itemid[0]
            newitemtext = camera.getname() + ' [Scene]'
            self._widgets['listbox-cameras'].setitemcontent(itemid[0],
                                                            newitemtext)

            # add new log for valid operation
            log_msg = 'Assigned camera "' + camera.getname() + '" to scene'
            self._logger.log(log_msg, lo.LogType.SUCCESS)

    def _command_validate_halt(self, P):
        """"""
    
        if len(P) > 4:
            return False
        elif len(P) >= 1 and not P.isdigit():
            return False
        elif len(P) == 4 and int(P) == 0:
            return False
    
        return True

    def _command_render(self):
        """"""

        materials_detected = True
        cameras_detected = True
        models_assigned = True
        scene_assigned = True
        packshotdest_set = True
        executable_set = True
        halt_valid = True
        
        # control if materials are detected
        if not self._parser.materials:
            log_msg = 'No materials detected'
            self._logger.log(log_msg, lo.LogType.ERROR)

            materials_detected = False
        
        # control if cameras are detected
        if not self._parser.cameras:
            log_msg = 'No cameras detected'
            self._logger.log(log_msg, lo.LogType.ERROR)

            cameras_detected = False

        # control if models are detected
        if self._parser.models:
            # control if all models are assigned with a material
            for model in self._parser.models:
                if not model.material:
                    log_msg = 'All models must be assigned with a material'
                    self._logger.log(log_msg, lo.LogType.ERROR)

                    models_assigned = False

                    break
        else:
            log_msg = 'No models detected'
            self._logger.log(log_msg, lo.LogType.ERROR)

            models_assigned = False

        # control if scene is detected
        if self._parser.scene:
            # control if a scene is assigned with a camera
            if not self._parser.scene.camera:
                log_msg = 'A camera must be assigned to the scene'
                self._logger.log(log_msg, lo.LogType.ERROR)

                scene_assigned = False
        else:
            log_msg = 'No scene detected'
            self._logger.log(log_msg, lo.LogType.ERROR)
            
            scene_assigned = False
        
        # control if a destination for packshot is set
        if not self._parser.packshotdest:
            log_msg = 'No packshot destination set'
            self._logger.log(log_msg, lo.LogType.ERROR)

            packshotdest_set = False
        
        if not self._indigo_exe_path:
            log_msg = 'No Indigo Renderer Console executable set'
            self._logger.log(log_msg, lo.LogType.ERROR)

            packshotdest_set = False

            executable_set = False
        
        # control if halt value is valid
        if not self._widgets['entry-halt'].get():
            log_msg = 'No halt set for rendering'
            self._logger.log(log_msg, lo.LogType.ERROR)
        
            halt_valid = False

        if (materials_detected and
            cameras_detected and
            models_assigned and
            scene_assigned and
            packshotdest_set and
            executable_set and
            halt_valid):

            # remove existing material tags in object file
            objbasetree = self._parser.models[0].basetree
            objroot = objbasetree.getroot()
            for nei in objroot.findall('material'):
                objroot.remove(nei)
                
            self._parser.inject_materials()

            # remove existing include tags in scene file
            for nei in self._parser.scene.tree.iter('include'):
                self._parser.scene.tree.remove(nei)

            self._parser.inject_camera()
            self._parser.inject_object()

            scenefname = self._parser.write_treesfiles()

            if scenefname:
                log_msg = 'Materials were successfuly injected'
                self._logger.log(log_msg, lo.LogType.SUCCESS)

                self._render_image(scenefname)
    
    def _render_image(self, p_scenefname):
        """"""
        
        now = datetime.now()
        strnow = now.strftime('%Y%d%m%H%M%S')
        imgdest = self._parser.packshotdest + os.sep + 'output_' + strnow

        cmd = (self._indigo_exe_path + ' -halt ' +
               self._widgets['entry-halt'].get() + ' -o ' + imgdest + '.png ' +
               p_scenefname)

        self._logger.log('Render start with halt at ' +
                         self._widgets['entry-halt'].get() + ' seconds')

        p = subprocess.Popen(cmd)

        # TODO: write a end message lol

    #---------------------------------------------------------------------------
    # Bindings methods
    #---------------------------------------------------------------------------
    def _on_mousewheel(self, p_event):
        """"""

        # TODO: don't work

        self._widgets['text-logs-lines'].yview_scroll(-1 * (p_event.delta/120), 'units')
        self._widgets['text-logs'].yview_scroll(-1 * (p_event.delta/120), 'units')

    def _on_closing(self):
        """Event function when closing the application. Write logs in a file
        before exiting application.
        """

        self._logger.write()
        self.destroy()

################################################################################
# Main
################################################################################
app = Application()
app.title('Indigo Packshoter')
app.resizable(False, False)
app.grab_set()

app.mainloop()