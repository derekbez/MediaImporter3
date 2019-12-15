import argparse
import time
from mediaimporter import UserChoices
from mediaimporter import MediaImporter
#from mediaimporter import Messages
from mediaimporter import Config
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.scrolledtext as tkscrolled
import threading
from pubsub import pub


class MICosole():
    
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
        #wrap with threading
        mediaImporter.startImport()
        ######
        print(mediaImporter.getFoldersProcessed())



class MIGUI():
    def __init__(self, master, **kwargs):
        
        self.master = master
        self.config = Config()
        self.userChoices = UserChoices()
       
        self.mediaImporter = MediaImporter(self.userChoices, sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)
        
        self.screenLayout()
        
    def screenLayout(self):    
        self.sourceFolder = tk.StringVar()
        self.sourceFolderLabel = ttk.Label(self.master, text='Source Folder')
        self.sourceFolderLabel.pack()
        self.sourceFolderEntry = ttk.Entry(self.master, width=60, textvariable=self.sourceFolder)
        self.sourceFolder.set(self.userChoices.sourceFolder)
        self.sourceFolderEntry.pack()
        self.sourceFolderButton = ttk.Button(self.master, text='Browse', command=self.sourceFolderButtonCallback)
        self.sourceFolderButton.pack()
        self.sourceFolder.trace('w', self.sourceFolderVarCallback)
        
        
        self.targetFolder = tk.StringVar()
        self.targetFolderLabel = ttk.Label(self.master, text='Target Folder')
        self.targetFolderLabel.pack()
        self.targetFolderEntry = ttk.Entry(self.master, width=60, textvariable=self.targetFolder)
        self.targetFolder.set(self.userChoices.targetFolder)
        self.targetFolderEntry.pack()
        self.targetFolderButton = ttk.Button(self.master, text='Browse', command=self.targetFolderButtonCallback)
        self.targetFolderButton.pack()
        self.targetFolder.trace('w', self.targetFolderVarCallback)

        self.folderStyles = list(self.config.getFolderStyles())
        self.folderStyleLabel = ttk.Label(self.master, text='Folder Style')
        self.folderStyleLabel.pack()
        self.folderStyle = ttk.Combobox(self.master, width=30, values=self.folderStyles)
        self.folderStyle.set(self.userChoices.folderStyle)
        self.folderStyle.pack()
        self.folderStyle.bind('<<ComboboxSelected>>', self.folderStyleCallback)
        
        self.fileStyles = list(self.config.getFileStyles())
        self.fileStyleLabel = ttk.Label(self.master, text='File Style')
        self.fileStyleLabel.pack()
        self.fileStyle = ttk.Combobox(self.master, width=30, values=self.fileStyles)
        self.fileStyle.set(self.userChoices.fileStyle)
        self.fileStyle.pack()
        self.fileStyle.bind('<<ComboboxSelected>>', self.fileStyleCallback)
        
        self.yearStyleCheck = tk.BooleanVar()
        self.yearStyle = ttk.Checkbutton(self.master, text='Use Year in Folder Structure?', variable=self.yearStyleCheck, onvalue=True, offvalue=False, command=self.yearStyleCallback)
        self.yearStyleCheck.set(self.userChoices.yearStyle)
        self.yearStyle.pack()
        
        self.projectName = tk.StringVar()
        self.projectNameLabel = ttk.Label(self.master, text='Project Name')
        self.projectNameLabel.pack()
        self.projectNameEntry = ttk.Entry(self.master, width=60, textvariable=self.projectName)
        self.projectName.set(self.userChoices.projectName)
        self.projectNameEntry.pack()
        self.projectName.trace('w', self.projectNameVarCallback)
        
        self.startButton = ttk.Button(self.master, text='Start', command=self.startCallback)
        self.startButton.pack()
        
        self.abortButton = ttk.Button(self.master, text='Abort', command=self.abortCallback)
        self.abortButton.state(['disabled'])
        self.abortButton.pack()
        
        self.sampleLabel = ttk.Label(self.master, text='Sample')
        self.sampleLabel.pack()
        self.sampleText = ttk.Label(self.master, text=self.mediaImporter.getSampleTargetPath())
        self.sampleText.pack()
        
        self.progress = ttk.Progressbar(self.master, length=500)
        self.progress.pack()
        
        self.outputBox = tkscrolled.ScrolledText(self.master, height=15, width=80, wrap='word')
        self.outputBox.pack()
        
        pub.subscribe(self.statusListener, 'STATUS')
        pub.subscribe(self.progressListener, 'PROGRESS')
        pub.subscribe(self.actionsListener, 'ACTIONS')
          
        self.displayCountOfFilesinSource()
        self.updateCountOfFilesinSource()
        


        
    def statusListener(self, status, value):
        if self.config.useDebug:
            self.updateOutputBox('MIGUI -> %s - %s' %(status , value))
        if status == 'copying' and (value == 'finished' or value == 'ABORTED'):
            self.updateOutputBox('Folders processed:')
            for folder in self.mediaImporter.getFoldersProcessed():
                self.updateOutputBox(folder)
            self.startButton.state(['!disabled'])
            self.abortButton.state(['disabled'])
            
            
            
    def progressListener(self, value):
        if self.config.useDebug:
            self.updateOutputBox('Progress %d' % value)
        self.progress['maximum'] = 100
        self.progress['value'] = value
        
    def actionsListener(self, source, target, action):
        self.updateOutputBox('%s -> %s - %s' %(source, target, action))
        
   

    def sourceFolderButtonCallback(self):
        folder = filedialog.askdirectory(initialdir=self.sourceFolder.get(), title='Please select the Source Folder')
        if self.config.useDebug:
            self.updateOutputBox('folder -%s- %3d' %(folder, len(folder)))
        if len(folder) > 1:
            self.sourceFolder.set(folder)
            self.updateCountOfFilesinSource()
            
    def sourceFolderVarCallback(self, v, l, o):  #https://stackoverflow.com/questions/29690463/what-are-the-arguments-to-tkinter-variable-trace-method-callbacks
        self.userChoices.sourceFolder = self.sourceFolder.get()
        self.updateCountOfFilesinSource()

    def targetFolderButtonCallback(self):
        folder = filedialog.askdirectory(initialdir=self.targetFolder.get(), title='Please select the Target Folder')
        self.updateOutputBox('folder -%s- %3d' %(folder, len(folder)))
        if len(folder) > 1:
            self.targetFolder.set(folder)
            
    def targetFolderVarCallback(self, v, l ,o):
        self.userChoices.targetFolder = self.targetFolder.get()        
    
    def folderStyleCallback(self, event):
        self.userChoices.folderStyle = self.folderStyle.get()
        self.sampleText.config(text = self.mediaImporter.getSampleTargetPath())
            
    def fileStyleCallback(self, event):
        self.userChoices.fileStyle = self.fileStyle.get()
        self.sampleText.config(text = self.mediaImporter.getSampleTargetPath())
        
    def yearStyleCallback(self):
        self.userChoices.yearStyle = self.yearStyleCheck.get()
        self.sampleText.config(text = self.mediaImporter.getSampleTargetPath())
            

    def projectNameVarCallback(self, v, l , o):
        self.userChoices.projectName = self.projectName.get()
        self.sampleText.config(text = self.mediaImporter.getSampleTargetPath())            

    def displayCountOfFilesinSource(self):
        mediaTypes = self.mediaImporter.getMediaTypes()
        self.mediaTypesVar = []
        self.countOfFilesVar = []
        self.mediaTypesLabel = []
        self.countOfFilesLabel = []
        i = 0
        self.updateOutputBox(mediaTypes)
        for i, mediaType in enumerate(mediaTypes):
            self.mediaTypesVar.append(tk.StringVar())
            self.mediaTypesLabel.append(ttk.Label(self.master, textvariable=self.mediaTypesVar[i]))
            self.mediaTypesVar[i].set(mediaType)
            self.mediaTypesLabel[i].pack()
            
            self.countOfFilesVar.append(tk.IntVar())
            self.countOfFilesLabel.append(ttk.Label(self.master, textvariable=self.countOfFilesVar[i]))
            self.countOfFilesVar[i].set(0)
            self.countOfFilesLabel[i].pack()

    def updateCountOfFilesinSource(self):
        countOfFiles = self.mediaImporter.getCountsOfFilesInSource()
        i=0
        for mediaType, count in countOfFiles.items():
            if self.mediaTypesVar[i].get() == mediaType:
                self.countOfFilesVar[i].set(count)
            else:   
                self.countOfFilesVar[i].set(-1)   # if the list of mediaTypes goes out of sync for any reason...
                raise Exception('Media Types list out of sync')
            i+=1

    def startCallback(self):
        self.updateOutputBox('start')
        self.abortButton.state(['!disabled'])
        self.startButton.state(['disabled'])
        self.x = threading.Thread(target=self.mediaImporter.startImport)
        self.x.start()
        
    def abortCallback(self):
        self.updateOutputBox('abort')
        self.mediaImporter.abortImport()

    def updateOutputBox(self, textstring):
        self.outputBox.insert(tk.END, textstring)
        self.outputBox.insert(tk.END, '\n')
        self.outputBox.see(tk.END)


#class MIGUI():
#    def __init__(self, master):
#        master.title = 'MediaImporter'
#        frame = tk.Frame(master)
#        frame.pack(side="top", fill="both", expand = True)
# 
#        MainMediaImporterScreen(frame)




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

#def commandLine(args):
#    """ Run the command line version """
#    if args.source is None:
#        print("Source not defined")
#    if args.target is None:
#        print("Target not defined")
#    if (args.source is not None and args.target is not None) and args.defaults.lower() is None:
#        print("do something here....")
#        #cp = MICosole(sourceFolder=args.source, targetFolder=Noargs.targetne, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)
#    if args.defaults == True:
#        print("do it with mediaimporterconfig.ini defaults....")
#        #cp = MICosole(sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)


def main():
    config = Config()
    
    parser = parserCommandLine()
    args = parser.parse_args()
    print(args)
    if config.useCON or args.console:
        if args.defaults:    # args.source or 
            cp = MICosole(sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)
            ##commandLine(args)
            #pass
    
    if config.useGUI:
        root = tk.Tk()
        app = MIGUI(root)   #.pack(side="top", fill="both", expand=True)
        root.mainloop()
        #pass
    
if __name__ == '__main__':
    main()
    
    
    
    
    

    