import tkinter as tk
from tkinter import ttk
import threading
import time
from pubsub import pub

class MIGUI():
    def __init__(self, master):
        self.master = master
        self.mediaImporter = MediaImporter()
        self.startButton = ttk.Button(self.master, text='Start', command=self.startCallback)
        self.startButton.pack()
        self.abortButton = ttk.Button(self.master, text='Abort', command=self.abortCallback)
        self.abortButton.state(['disabled'])
        self.abortButton.pack()
        self.progress = ttk.Progressbar(self.master, length=300)
        self.progress.pack()
        pub.subscribe(self.statusListener, 'STATUS')
        pub.subscribe(self.progressListener, 'PROGRESS')
    def statusListener(self, status, value):
        print('MIGUI', status, value)
        if status == 'copying' and (value == 'finished' or value == 'aborted'):
            self.startButton.state(['!disabled'])
            self.abortButton.state(['disabled'])
    def progressListener(self, value):
        print('Progress %d' % value)
        self.progress['maximum'] = 100
        self.progress['value'] = value
    def startCallback(self):
        print('startCallback')
        self.abortButton.state(['!disabled'])
        self.startButton.state(['disabled'])
        self.x = threading.Thread(target=self.mediaImporter.startImport)
        self.x.start()
        # original issue had join() here, which was blocking.
    def abortCallback(self):
        print('abortCallback')
        self.mediaImporter.abortImport()

class MediaImporter():
    """ Interface between user (GUI / console) and worker classes """
    def __init__(self):
        self.Import = Import()
        #other worker classes exist too
        pub.subscribe(self.statusListener, 'STATUS')
    def statusListener(self, status, value):
        #perhaps do something
        pass
    def startImport(self):
        self.Import.start()
    def abortImport(self):
        self.Import.abort()

class Import():
    """ Worker
        Does not know anything about other non-worker classes or UI.
        It does use pubsub to publish messages - such as the status and progress.
        The UI and interface classes can subsribe to these messages and perform actions. (see listener methods)
    """
    def __init__(self):
        self._wantAbort = False
    def start(self):
        self._wantAbort = False
        self.doImport()
    def abort(self):
        pub.sendMessage('STATUS', status='abort', value='requested')
        self._wantAbort = True
    def doImport(self):
        self.max = 13
        pub.sendMessage('STATUS', status='copying', value='started')
        for i in range(1,self.max):
            #actual code has nested for..loops
            progress = ((i+1) / self.max * 100.0)
            pub.sendMessage('PROGRESS', value=progress)
            time.sleep(.1)
            if self._wantAbort:
                pub.sendMessage('STATUS', status='copying', value='aborted')
                return
        pub.sendMessage('STATUS', status='copying', value='finished')

def main():
    gui = True
    console = False
    if gui:
        root = tk.Tk()
        app = MIGUI(root)
        root.mainloop()
    if console:
        #do simple console output without tkinter - threads not necessary
        pass
if __name__ == '__main__':
    main()