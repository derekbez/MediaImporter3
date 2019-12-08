import argparse
from mediaimporter import UserChoices
from mediaimporter import MediaImporter
#from mediaimporter import Messages
from mediaimporter import Config
import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown 
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.progressbar import ProgressBar



class console():
    
    def __init__(self, sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None):
        
        self._sourceFolder = sourceFolder
        self._targetFolder = targetFolder
        self._folderStyle = folderStyle
        self._fileStyle = fileStyle
        self._yearStyle = yearStyle
        self._projectName = projectName
        
        config = Config()
        userChoices = UserChoices()
        userChoices.sourceFolder = 'x:'
        mediaImporter = MediaImporter(userChoices, sourceFolder=self._sourceFolder
                                                    , targetFolder=self._targetFolder
                                                    , folderStyle=self._folderStyle
                                                    , fileStyle=self._fileStyle
                                                    , yearStyle=self._yearStyle
                                                    , projectName=self._projectName)
        userChoices.sourceFolder = 'D:\\Dev\\MediaImporter3\\test\\tempsource'
        
        mediaTypes = config.getMediaTypes()
        print(mediaTypes)
        print(config.getFolderStyles())
        print('Source Folder %s - %s' %(userChoices.sourceFolder , mediaImporter.sourceFolder))
        print('Target Folder %s - %s' %(userChoices.targetFolder, mediaImporter.targetFolder))
        print('Folder Style %s' %userChoices.folderStyle)
        print('File Style %s' %userChoices.fileStyle)
        print('Year Style %s' %userChoices.yearStyle)
        print('Project Name %s' %userChoices.projectName)
        print('Sample path %s' %mediaImporter.getSampleTargetPath())
        
        #mediaImporter = MediaImporter(yearStyle=False)
        print(mediaImporter.getCountsOfFilesInSource())
        mediaImporter.start()
        print(mediaImporter.getFoldersProcessed())



class MainMediaImporterScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainMediaImporterScreen, self).__init__(**kwargs)
        
        config = Config()
        userChoices = UserChoices()
        mediaImporter = MediaImporter(userChoices, sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)
        
        self.cols = 2
        self.add_widget(Label(text='Source Folder'))
        # https://kivy.org/doc/stable/api-kivy.uix.filechooser.html
        self.sourceFolder = TextInput(multiline=False)
        self.add_widget(self.sourceFolder)
        self.add_widget(Label(text='Target Folder'))
        self.targetFolder = TextInput(multiline=False)
        self.add_widget(self.targetFolder)
        
        self.add_widget(Label(text='Folder Style'))
        #print(mediaImporter.folderStyle, list(config.getFolderStyles()))
        self.folderStyle = Spinner(text=mediaImporter.folderStyle, values=list(config.getFolderStyles()))
        self.add_widget(self.folderStyle)
        self.add_widget(Label(text='File Style'))
        self.fileStyle = Spinner(text=mediaImporter.fileStyle, values=list(config.getFileStyles()))
        self.add_widget(self.fileStyle)
        self.add_widget(Label(text='Separate Year Folder'))
        self.yearStyle = CheckBox(active=mediaImporter.yearStyle)
        self.add_widget(self.yearStyle)
        
        #TODO: convert projectName default from None to empty string
        if mediaImporter.projectName is None:
            mediaImporter.projectName = ''
        self.add_widget(Label(text='Project Name'))
        self.projectName = TextInput(text=mediaImporter.projectName, multiline=False)
        self.add_widget(self.projectName)
        
        startButton = Button(text='Start Import')
        self.add_widget(startButton)
        stopButton = Button(text='Abort')
        self.add_widget(stopButton)
        
        #https://kivy.org/doc/stable/api-kivy.uix.progressbar.html
        progressBar = ProgressBar(max=100)
        self.add_widget(progressBar)
        
        self.outputText = TextInput(multiline=True)
        self.add_widget(self.outputText)
        

class MIApp(App):
    def build(self):
        return MainMediaImporterScreen()





def parserCommandLine():
    """ The argument parser of the command-line version """
    parser = argparse.ArgumentParser(description=('Import media files (photos, video, etc) from a Source (SD card) to a Target (hard drive), and rename.'))
    parser.add_argument('--console', action='store_true'
                        ,help="Force the console app")
    parser.add_argument('--defaults', '-D', action='store_true'
                        ,help="Use Defaults from mediaimporterconfig.ini file.")   
    parser.add_argument('--source', '-S'
                        ,help="Source drive and folder")
    parser.add_argument('--target', '-T'
                        ,help="Target drive and folder")
    #todo: add other options for folder and file styles
    #parser.print_help()
    return parser

def commandLine(args):
    """ Run the command line version """
    if args.source is None:
        print("Source not defined")
    if args.target is None:
        print("Target not defined")
    if (args.source is not None and args.target is not None) and args.defaults.lower() is None:
        #print("do something here....")
        cp = console(sourceFolder=args.source, targetFolder=Noargs.targetne, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)
    if args.defaults == True:
        print("do it with mediaimporterconfig.ini defaults....")
        #cp = console(sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)


def main():
    config = Config()
    
    parser = parserCommandLine()
    args = parser.parse_args()
    print(args)
    if config.useCON or args.console:
        if args.source or args.defaults:
            commandLine(args)

    
    
    if config.useGUI:
        

        MIApp().run()
        #pass
    
if __name__ == '__main__':
    main()
    
    
    
    
    

    
"""
https://kivy.org/doc/stable/installation/installation-windows.html
python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
python -m pip install kivy_deps.gstreamer==0.1.*
python -m pip install kivy_deps.angle==0.1.*
python -m pip install kivy==1.11.1
https://kivy.org/doc/stable/api-kivy.html

D:\Dev\MediaImporter3\share\kivy-examples\demo\kivycatalog
"""    