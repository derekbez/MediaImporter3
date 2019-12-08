import argparse
from mediaimporter import UserChoices
from mediaimporter import MediaImporter
#from mediaimporter import Messages
from mediaimporter import Config
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog



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



class MainMediaImporterScreen():
    def __init__(self, frame,  **kwargs):
        
        self.frame = frame
        self.config = Config()
        self.userChoices = UserChoices()
        self.mediaImporter = MediaImporter(self.userChoices, sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)

        
        self.sourceFolder = tk.StringVar()
        self.sourceFolder.set(self.userChoices.sourceFolder)
        self.sourceFolderLabel = ttk.Label(self.frame, text='Source Folder')
        self.sourceFolderLabel.pack()
        self.sourceFolderEntry = ttk.Entry(self.frame, width=60, textvariable=self.sourceFolder)
        self.sourceFolderEntry.pack()
        self.sourceFolderButton = ttk.Button(self.frame, text='Browse', command=self.sourceFolderCallback)
        self.sourceFolderButton.pack()
        
        
        self.targetFolder = tk.StringVar()
        self.targetFolder.set(self.userChoices.targetFolder)
        self.targetFolderLabel = ttk.Label(self.frame, text='Target Folder')
        self.targetFolderLabel.pack()
        self.targetFolderEntry = ttk.Entry(self.frame, width=60, textvariable=self.targetFolder)
        self.targetFolderEntry.pack()
        self.targetFolderButton = ttk.Button(self.frame, text='Browse', command=self.targetFolderCallback)
        self.targetFolderButton.pack()

        self.folderStyles = list(self.config.getFolderStyles())
        self.folderStyleLabel = ttk.Label(self.frame, text='Folder Style')
        self.folderStyleLabel.pack()
        self.folderStyle = ttk.Combobox(self.frame, width=30, values=self.folderStyles)
        self.folderStyle.set(self.userChoices.folderStyle)
        self.folderStyle.pack()
        self.folderStyle.bind('<<ComboboxSelected>>')
        
        self.fileStyles = list(self.config.getFileStyles())
        self.fileStyleLabel = ttk.Label(self.frame, text='File Style')
        self.fileStyleLabel.pack()
        self.fileStyle = ttk.Combobox(self.frame, width=30, values=self.fileStyles)
        self.fileStyle.set(self.userChoices.fileStyle)
        self.fileStyle.pack()
        
        self.yearStyle = ttk.Checkbutton(self.frame, text='Use Year in Folder Structure?', variable=self.userChoices.yearStyle, onvalue=True, offvalue=False)
        self.yearStyle.pack()
        
        self.startButton = ttk.Button(self.frame, text='Start', command=self.start())
        self.startButton.pack()
        
        self.abortButton = ttk.Button(self.frame, text='Abort', command=self.abort())
        #self.abortButton.state(['disabled'])
        self.abortButton.pack()

    def sourceFolderCallback(self):
        folder = filedialog.askdirectory(title='Please select a directory')
        #print('folder -%s- %d' %folder %len(folder))
        #if len(folder) > 1:
        #    self.sourceFolder.set(folder)

    def targetFolderCallback(self):
        folder = filedialog.askdirectory(parent=self.frame, initialdir=self.targetFolder, title='Please select a directory')
        print('folder -%s- %d' %folder %len(folder))
        #if len(folder) > 1:
        #    self.targetFolder.set(folder)

    def start(self):
        #self.abortButton.state(['enabled'])
        self.mediaImporter.start()
        #self.abortButton.state(['disabled'])
        
    def abort(self):
        self.mediaImporter.abort()
        #self.abortButton.state(['disabled'])

class MIApp():
    def __init__(self, master):
        master.title = 'MediaImporter'
        frame = tk.Frame(master)
        frame.pack(side="top", fill="both", expand = True)
 
        MainMediaImporterScreen(frame)




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
        print("do something here....")
        #cp = console(sourceFolder=args.source, targetFolder=Noargs.targetne, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)
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
            #commandLine(args)
            pass
    
    
    if config.useGUI:
        root = tk.Tk()
        app = MIApp(root)   #.pack(side="top", fill="both", expand=True)
        root.mainloop()
        #pass
    
if __name__ == '__main__':
    main()
    
    
    
    
    

    