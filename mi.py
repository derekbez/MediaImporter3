import argparse
import time
from mediaimporter import UserChoices
from mediaimporter import MediaImporter
from mediaimporter import Config
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.scrolledtext as tkscrolled
import threading
from pubsub import pub


def main():
    config = Config()

    parser = parserCommandLine()
    args = parser.parse_args()
    print(args)
    if config.useCON or args.console:
        commandLine(args)

    if config.useGUI:
        preroot = tk.Tk() 
        preroot.update_idletasks()
        preroot.attributes('-fullscreen', True)
        preroot.state('iconic')
        geometry = preroot.winfo_geometry()
        preroot.destroy()
        
        global screenWidth
        global screenHeight
        x = geometry.split('+')  # 2048x1152+0+0
        geometryList = x[0].split('x')
        screenWidth = int(geometryList[0])
        screenHeight = int(geometryList[1])
        #print(screenWidth, screenHeight)
        
        root = tk.Tk()
        root.title('Media Importer v3') 

        app = MIGUI(root)
        root.mainloop()

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

    parser.add_argument('--folderstyle'
                        ,help="Folder Style to use.   eg: [type]/[date]   Valid keywords are: [type] [date] [projectname]")

    parser.add_argument('--filestyle'
                        ,help="Filename Style to use.   eg: [datetime]_[origid]   Valid keywords are: [datetime] [origid] [projectname]")

    parser.add_argument('--yearstyle'
                        ,choices=['True','False']
                        ,help="Whether to use a separate year folder.   eg: Photos/2019/2019_12_25/")

    parser.add_argument('--project'
                        ,help="Project Name. Text to be included in Folder Style or Filename Style.")


    #parser.print_help()
    return parser

def commandLine(args):
    """ Run the command line version """
    if args.defaults == True:
        print("do it with mediaimporterconfig.ini defaults....")
        cp = MICosole(sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)
    else:
        cp = MICosole(sourceFolder=args.source
                    , targetFolder=args.target
                    , folderStyle=args.folderstyle
                    , fileStyle=args.filestyle
                    , yearStyle=args.yearstyle
                    , projectName=args.project)





class MICosole():

    def __init__(self, sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None):

        self._sourceFolder = sourceFolder
        self._targetFolder = targetFolder
        self._folderStyle = folderStyle
        self._fileStyle = fileStyle
        self._yearStyle = yearStyle
        self._projectName = projectName

        self.config = Config()
        self.userChoices = UserChoices()
        self.mediaImporter = MediaImporter(self.userChoices, sourceFolder=self._sourceFolder
                                                    , targetFolder=self._targetFolder
                                                    , folderStyle=self._folderStyle
                                                    , fileStyle=self._fileStyle
                                                    , yearStyle=self._yearStyle
                                                    , projectName=self._projectName)


        mediaTypes = self.config.getMediaTypes()
        print('Configured Media Types: ', mediaTypes)
        print('Configured Folder Styles: ', self.config.getFolderStyles())
        self.updateOutputBox('Source Folder: %s' %(self.userChoices.sourceFolder))
        self.updateOutputBox('Target Folder: %s' %(self.userChoices.targetFolder))
        self.updateOutputBox('Folder Style: %s' %self.userChoices.folderStyle)
        self.updateOutputBox('File Style: %s' %self.userChoices.fileStyle)
        self.updateOutputBox('Year Style: %s' %self.userChoices.yearStyle)
        self.updateOutputBox('Project Name: %s' %self.userChoices.projectName)
        self.updateOutputBox('Sample path: %s' %self.mediaImporter.getSampleTargetPath())

        pub.subscribe(self.statusListener, 'STATUS')
        pub.subscribe(self.progressListener, 'PROGRESS')
        pub.subscribe(self.actionsListener, 'ACTIONS')


        #print(mediaImporter.getCountsOfFilesInSource())
        #wrap with threading
        self.mediaImporter.startImport()
        ######
        #print(mediaImporter.getFoldersProcessed())

    def statusListener(self, status, value):
        if self.config.useDebug:
            self.updateOutputBox('MIGUI -> %s - %s' %(status , value))
        if status == 'copying':
            self.updateOutputBox(value)
        if status == 'copying' and (value == 'Finished' or value == 'ABORTED'):
            self.updateOutputBox('Summary of Target Folders:')
            for folder in self.mediaImporter.getFoldersProcessed():
                self.updateOutputBox(folder)
        if status == 'finishedFileCount':
            self.updateOutputBox('Copied %s  Skipped %s' %(value[1], value[2]))

    def progressListener(self, value):
        self.updateOutputBox('Progress %d%%' % value)

    def actionsListener(self, source, target, action):
        self.updateOutputBox('%s -> %s - %s' %(source, target, action))

    def updateOutputBox(self, textstring):
        print(textstring)



class MIGUI():
    def __init__(self, root, **kwargs):
        self.root = root
        self.config = Config()
        self.userChoices = UserChoices()

        self.mediaImporter = MediaImporter(self.userChoices, sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None)

        self.screenLayoutPack()

        pub.subscribe(self.statusListener, 'STATUS')
        pub.subscribe(self.progressListener, 'PROGRESS')
        pub.subscribe(self.actionsListener, 'ACTIONS')

        #self.displayCountOfFilesinSource()
        self.updateCountOfFilesinSource()

    def screenLayoutGrid(self):
        """deprecated"""
        #https://tkdocs.com/tutorial/grid.html
        self.content = ttk.Frame(self.master, padding=(3,3,12,12))   #, bg='red'
        self.content.grid(row=0, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

        self.countOfFilesFrame = ttk.Frame(self.content, borderwidth=2, relief="sunken")
        self.countOfFilesFrame.grid(row=0, column=1, sticky=(tk.N,tk.S,tk.E,tk.W), rowspan=3)

        self.sourceFolderFrame = ttk.Frame(self.content)
        self.sourceFolderFrame.grid(row=0, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

        self.targetFolderFrame = ttk.Frame(self.content)
        self.targetFolderFrame.grid(row=1, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

        self.folderStylesFrame = ttk.Frame(self.content)
        self.folderStylesFrame.grid(row=2, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

        self.fileStylesFrame = ttk.Frame(self.content)
        self.fileStylesFrame.grid(row=3, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

        self.projectNameFrame = ttk.Frame(self.content)
        self.projectNameFrame.grid(row=4, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

        self.sampleFrame = ttk.Frame(self.content)
        self.sampleFrame.grid(row=5, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

        self.buttonsFrame = ttk.Frame(self.content)
        self.buttonsFrame.grid(row=7, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

        self.sourceFolder = tk.StringVar()
        self.sourceFolderLabel = ttk.Label(self.sourceFolderFrame, text='Source Folder:')
        self.sourceFolderLabel.grid(row=0, column=0, sticky=tk.W, pady=5, padx=2)
        self.sourceFolderEntry = ttk.Entry(self.sourceFolderFrame, width=45, textvariable=self.sourceFolder)
        self.sourceFolder.set(self.userChoices.sourceFolder)
        self.sourceFolderEntry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=2)
        self.sourceFolderButton = ttk.Button(self.sourceFolderFrame, text='Browse', command=self.sourceFolderButtonCallback)
        self.sourceFolderButton.grid(row=0, column=2, sticky=tk.W, pady=5, padx=2)
        self.sourceFolder.trace('w', self.sourceFolderVarCallback)

        self.targetFolder = tk.StringVar()
        self.targetFolderLabel = ttk.Label(self.targetFolderFrame, text='Target Folder:')
        self.targetFolderLabel.grid(row=0, column=0, sticky=tk.W, pady=5, padx=2)
        self.targetFolderEntry = ttk.Entry(self.targetFolderFrame, width=45, textvariable=self.targetFolder)
        self.targetFolder.set(self.userChoices.targetFolder)
        self.targetFolderEntry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=2)
        self.targetFolderButton = ttk.Button(self.targetFolderFrame, text='Browse', command=self.targetFolderButtonCallback)
        self.targetFolderButton.grid(row=0, column=2, sticky=tk.W, pady=5, padx=2)
        self.targetFolder.trace('w', self.targetFolderVarCallback)

        self.folderStyles = list(self.config.getFolderStyles())
        self.folderStyleLabel = ttk.Label(self.folderStylesFrame, text='Folder Style:')
        self.folderStyleLabel.grid(row=0, column=0, sticky=tk.W, pady=5, padx=2)
        self.folderStyle = ttk.Combobox(self.folderStylesFrame, width=30, values=self.folderStyles)
        self.folderStyle.set(self.userChoices.folderStyle)
        self.folderStyle.grid(row=0, column=1, sticky=tk.W, pady=5, padx=2)
        self.folderStyle.bind('<<ComboboxSelected>>', self.folderStyleCallback)

        self.yearStyleCheck = tk.BooleanVar()
        self.yearStyle = ttk.Checkbutton(self.folderStylesFrame, text='Use Year in Folder Structure?', variable=self.yearStyleCheck, onvalue=True, offvalue=False, command=self.yearStyleCallback)
        self.yearStyleCheck.set(self.userChoices.yearStyle)
        self.yearStyle.grid(row=0, column=2, sticky=tk.W, pady=5, padx=2)

        self.fileStyles = list(self.config.getFileStyles())
        self.fileStyleLabel = ttk.Label(self.fileStylesFrame, text='File Style:')
        self.fileStyleLabel.grid(row=0, column=0, sticky=tk.W, pady=5, padx=2)
        self.fileStyle = ttk.Combobox(self.fileStylesFrame, width=30, values=self.fileStyles)
        self.fileStyle.set(self.userChoices.fileStyle)
        self.fileStyle.grid(row=0, column=1, sticky=tk.W, pady=5, padx=2)
        self.fileStyle.bind('<<ComboboxSelected>>', self.fileStyleCallback)

        self.projectName = tk.StringVar()
        self.projectNameLabel = ttk.Label(self.projectNameFrame, text='Project Name:')
        self.projectNameLabel.grid(row=0, column=0, sticky=tk.W, pady=5, padx=2)
        self.projectNameEntry = ttk.Entry(self.projectNameFrame, width=30, textvariable=self.projectName)
        self.projectName.set(self.userChoices.projectName)
        self.projectNameEntry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=2)
        self.projectName.trace('w', self.projectNameVarCallback)

        self.sampleLabel = ttk.Label(self.sampleFrame, text='Sample:')
        self.sampleLabel.grid(row=0, column=0, sticky=tk.E, pady=5, padx=2)
        self.sampleText = ttk.Label(self.sampleFrame, text=self.mediaImporter.getSampleTargetPath(), wraplength=550)
        self.sampleText.grid(row=0, column=1, sticky=tk.W, pady=5, padx=2, columnspan=3)

        self.startButton = ttk.Button(self.buttonsFrame, text='Start', command=self.startCallback)
        self.startButton.grid(row=0, column=0, sticky=tk.W, pady=5, padx=2)

        self.abortButton = ttk.Button(self.buttonsFrame, text='Abort', command=self.abortCallback)
        self.abortButton.state(['disabled'])
        self.abortButton.grid(row=0, column=1, sticky=tk.W, pady=5, padx=2)

        self.progress = ttk.Progressbar(self.content)
        self.progress.grid(row=8, column=0, sticky=(tk.E,tk.W), pady=5, padx=10, columnspan=3)

        self.outputBox = tkscrolled.ScrolledText(self.content, height=15, width=100, wrap='word')
        self.outputBox.grid(row=9, column=0, sticky=(tk.E,tk.W), pady=5, padx=2, columnspan=3)

    def screenLayoutPack(self):
        self.contentFrame = ttk.Frame(self.root) #, padding=(3,3,12,6))  
        self.contentFrame.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        self.content = Scrollable(self.contentFrame)   
        #self.content.configure(background='black')

        self.sourceFolderFrame = ttk.Frame(self.content)
        self.sourceFolderFrame.pack(side = tk.TOP, anchor = tk.NW, expand = True, pady = 3)
        
        self.targetFolderFrame = ttk.Frame(self.content)
        self.targetFolderFrame.pack(side = tk.TOP, anchor = tk.NW, expand = True, pady = 3)

        self.folderStylesFrame = ttk.Frame(self.content)
        self.folderStylesFrame.pack(side = tk.TOP, anchor = tk.NW, expand = True, pady = 3)

        self.fileStylesFrame = ttk.Frame(self.content)
        self.fileStylesFrame.pack(side = tk.TOP, anchor = tk.NW, expand = True, pady = 3)

        self.projectNameFrame = ttk.Frame(self.content)
        self.projectNameFrame.pack(side = tk.TOP, anchor = tk.NW, expand = True, pady = 3)

        self.sampleFrame = ttk.Frame(self.content)
        self.sampleFrame.pack(side = tk.TOP, anchor = tk.NW, expand = True, pady = 3)

        self.buttonsFrame = ttk.Frame(self.content)
        self.buttonsFrame.pack(side = tk.TOP, anchor = tk.NW, expand = True, pady = 3)

        self.outputBoxFrame = ttk.Frame(self.content)
        self.outputBoxFrame.pack(side = tk.TOP, anchor = tk.NW, expand = True, pady = 3)

        leftOrTop = self.determineLeftOrTop()
        
        self.sourceFolder = tk.StringVar()
        self.sourceFolderLabel = ttk.Label(self.sourceFolderFrame, text='Source Folder:')
        self.sourceFolderLabel.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.sourceFolderEntry = ttk.Entry(self.sourceFolderFrame, width=45, textvariable=self.sourceFolder)
        self.sourceFolder.set(self.userChoices.sourceFolder)
        self.sourceFolderEntry.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.sourceFolderButton = ttk.Button(self.sourceFolderFrame, text='Browse', command=self.sourceFolderButtonCallback)
        self.sourceFolderButton.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.sourceFolder.trace('w', self.sourceFolderVarCallback)

        self.targetFolder = tk.StringVar()
        self.targetFolderLabel = ttk.Label(self.targetFolderFrame, text='Target Folder:')
        self.targetFolderLabel.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.targetFolderEntry = ttk.Entry(self.targetFolderFrame, width=45, textvariable=self.targetFolder)
        self.targetFolder.set(self.userChoices.targetFolder)
        self.targetFolderEntry.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.targetFolderButton = ttk.Button(self.targetFolderFrame, text='Browse', command=self.targetFolderButtonCallback)
        self.targetFolderButton.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.targetFolder.trace('w', self.targetFolderVarCallback)

        self.folderStyles = list(self.config.getFolderStyles())
        self.folderStyleLabel = ttk.Label(self.folderStylesFrame, text='Folder Style:')
        self.folderStyleLabel.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.folderStyle = ttk.Combobox(self.folderStylesFrame, width=30, values=self.folderStyles)
        self.folderStyle.set(self.userChoices.folderStyle)
        self.folderStyle.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.folderStyle.bind('<<ComboboxSelected>>', self.folderStyleCallback)

        self.yearStyleCheck = tk.BooleanVar()
        self.yearStyle = ttk.Checkbutton(self.folderStylesFrame, text='Use Year in Folder Structure?', variable=self.yearStyleCheck, onvalue=True, offvalue=False, command=self.yearStyleCallback)
        self.yearStyleCheck.set(self.userChoices.yearStyle)
        self.yearStyle.pack(side = leftOrTop, anchor = tk.NW, padx=3)

        self.fileStyles = list(self.config.getFileStyles())
        self.fileStyleLabel = ttk.Label(self.fileStylesFrame, text='File Style:')
        self.fileStyleLabel.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.fileStyle = ttk.Combobox(self.fileStylesFrame, width=30, values=self.fileStyles)
        self.fileStyle.set(self.userChoices.fileStyle)
        self.fileStyle.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.fileStyle.bind('<<ComboboxSelected>>', self.fileStyleCallback)

        self.projectName = tk.StringVar()
        self.projectNameLabel = ttk.Label(self.projectNameFrame, text='Project Name:')
        self.projectNameLabel.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.projectNameEntry = ttk.Entry(self.projectNameFrame, width=30, textvariable=self.projectName)
        self.projectName.set(self.userChoices.projectName)
        self.projectNameEntry.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.projectName.trace('w', self.projectNameVarCallback)

        self.sampleLabel = ttk.Label(self.sampleFrame, text='Sample:')
        self.sampleLabel.pack(side = leftOrTop, anchor = tk.NW, padx=3)
        self.sampleText = ttk.Label(self.sampleFrame, text=self.mediaImporter.getSampleTargetPath(), wraplength=550)
        self.sampleText.pack(side = leftOrTop, anchor = tk.NW, padx=3)

        self.startButton = ttk.Button(self.buttonsFrame, text='Start', command=self.startCallback)
        self.startButton.pack(side = tk.LEFT, anchor = tk.NW, padx=3)

        self.abortButton = ttk.Button(self.buttonsFrame, text='Abort', command=self.abortCallback)
        self.abortButton.state(['disabled'])
        self.abortButton.pack(side = tk.LEFT, anchor = tk.NW, padx=3)

        self.progress = ttk.Progressbar(self.outputBoxFrame)
        self.progress.pack(side = tk.TOP, expand = True, fill = tk.X, padx = 3)

        self.outputBox = tkscrolled.ScrolledText(self.outputBoxFrame, wrap='word')
        self.outputBox.pack(side = tk.TOP, expand = True, fill = tk.BOTH, padx = 3)

        outboxWidth = self.determineWidthFromScreen() - 24
        self.outputBoxspacer = tk.Frame(self.outputBoxFrame, width=outboxWidth, height=1)
        self.outputBoxspacer.pack()

        self.content.update()
        self.root.geometry('%dx%d' %(self.content.winfo_width(), self.determineHeightFromScreen()))

        #self.root.geometry('%dx%d' %(self.determineWidthFromScreen(), self.determineHeightFromScreen()))
        #print('screen %dx%d' %(self.determineWidthFromScreen(), self.determineHeightFromScreen()))
        #print('self.root.geometry() %s' %self.root.geometry())
        #print('self.content.winfo_width() %s' %self.content.winfo_width())  
        #print('outbox %d %d' %(self.outputBoxFrame.winfo_width(), self.outputBoxFrame.winfo_height()))

    def determineWidthFromScreen(self):
        if screenWidth < 800:
            return screenWidth
        else:
            return 960
            
    def determineHeightFromScreen(self):
        if screenHeight <= 800:
            return 800
        else:
            return 640       
            
    def determineLeftOrTop(self):
        if screenWidth < 800: # or 1==1:
            return 'top'
        else:
            return 'left'


    def statusListener(self, status, value):
        if self.config.useDebug:
            self.updateOutputBox('MIGUI -> %s - %s' %(status , value))
        if status == 'copying':
            self.updateOutputBox(value)
        if status == 'copying' and (value == 'Finished' or value == 'ABORTED' or value.find('Error') >= 0 ):
            self.updateOutputBox('Summary of Target Folders:')
            for folder in self.mediaImporter.getFoldersProcessed():
                self.updateOutputBox(folder)
            self.startButton.state(['!disabled'])
            self.abortButton.state(['disabled'])
        if status == 'finishedFileCount':
            self.updateOutputBox('Copied %s  Skipped %s' %(value[1], value[2]))

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
            #self.updateCountOfFilesinSource()  # this might not be necessary

    def sourceFolderVarCallback(self, v, l, o):
        #https://stackoverflow.com/questions/29690463/what-are-the-arguments-to-tkinter-variable-trace-method-callbacks
        self.userChoices.sourceFolder = self.sourceFolder.get()
        self.updateCountOfFilesinSource()

    def targetFolderButtonCallback(self):
        folder = filedialog.askdirectory(initialdir=self.targetFolder.get(), title='Please select the Target Folder')
        if self.config.useDebug:
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
        """deprecated"""
        mediaTypes = self.mediaImporter.getMediaTypes()
        self.mediaTypesVar = []
        self.countOfFilesVar = []
        self.mediaTypesLabel = []
        self.countOfFilesLabel = []
        i = 0
        self.updateOutputBox(mediaTypes)
        for i, mediaType in enumerate(mediaTypes):
            self.mediaTypesVar.append(tk.StringVar())
            self.mediaTypesLabel.append(ttk.Label(self.countOfFilesFrame, textvariable=self.mediaTypesVar[i]))
            self.mediaTypesVar[i].set(mediaType)
            self.mediaTypesLabel[i].grid(row=i, column=0)

            self.countOfFilesVar.append(tk.IntVar())
            self.countOfFilesLabel.append(ttk.Label(self.countOfFilesFrame, textvariable=self.countOfFilesVar[i]))
            self.countOfFilesVar[i].set(0)
            self.countOfFilesLabel[i].grid(row=i, column=1)

    def updateCountOfFilesinSource_deprecated(self):
        """deprecated"""
        countOfFiles = self.mediaImporter.getCountsOfFilesInSource()
        i=0
        for mediaType, count in countOfFiles.items():
            if self.mediaTypesVar[i].get() == mediaType:
                self.countOfFilesVar[i].set(count)
            else:
                self.countOfFilesVar[i].set(-1)   # if the list of mediaTypes goes out of sync for any reason...
                raise Exception('Media Types list out of sync')
            i+=1

    def updateCountOfFilesinSource(self):
        countOfFiles = self.mediaImporter.getCountsOfFilesInSource()
        self.updateOutputBox('Number of files in Source Folder:')
        for mediaType, count in countOfFiles.items():
            self.updateOutputBox(mediaType + '\t' + str(count))

    def startCallback(self):
        self.abortButton.state(['!disabled'])
        self.startButton.state(['disabled'])
        self.x = threading.Thread(target=self.mediaImporter.startImport)
        self.x.start()

    def abortCallback(self):
        self.updateOutputBox('Abort requested')
        self.mediaImporter.abortImport()

    def updateOutputBox(self, textstring):
        self.outputBox.insert(tk.END, textstring)
        self.outputBox.insert(tk.END, '\n')
        self.outputBox.see(tk.END)

class Scrollable(ttk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame, 
       call the update() method to refresh the scrollable area.
       https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
    """
    def __init__(self, frame, width=16):
        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        ttk.Frame.__init__(self, frame)         

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)
        
    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"
        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)  
        #print('canvas %s' %canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
        #print('canvas winfo_width %s' %self.canvas.winfo_width())


if __name__ == '__main__':
    main()






