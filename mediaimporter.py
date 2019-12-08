import os
import re
import configparser
import platform
from datetime import datetime, date
import time
import pathlib
import shutil
import threading
from pynput import keyboard
from pubsub import pub


class MediaImporter():
    def __init__(self, userChoices=None, sourceFolder=None, targetFolder=None, folderStyle=None, fileStyle=None, yearStyle=None, projectName=None):
        if isinstance(userChoices, UserChoices):
            self.userChoices = userChoices
        else:
            self.userChoices = UserChoices()
        self.Config = Config()
        self.Import = Import()

        # sourceFolder takes priority over userChoices.  If both are blank, then get from Config.
        if sourceFolder != None and sourceFolder != '':
            self.userChoices.sourceFolder = sourceFolder
        if self.userChoices.sourceFolder == None:
            self.userChoices.sourceFolder = self.Config.userSourceFolder
        self.__sourceFolder = self.userChoices.sourceFolder

        if targetFolder != None and targetFolder != '':
            self.userChoices.targetFolder = targetFolder
        if self.userChoices.targetFolder == None:
            self.userChoices.targetFolder = self.Config.userTargetFolder
        self.__targetFolder = self.userChoices.targetFolder

        if folderStyle != None and folderStyle != '':
            self.userChoices.folderStyle = folderStyle
        if self.userChoices.folderStyle == None:
            self.userChoices.folderStyle = self.Config.userFolderStyle
        self.__folderStyle = self.userChoices.folderStyle

        if fileStyle != None and fileStyle != '':
            self.userChoices.fileStyle = fileStyle
        if self.userChoices.fileStyle == None:
            self.userChoices.fileStyle = self.Config.userFileStyle
        self.__fileStyle = self.userChoices.fileStyle

        if yearStyle != None and yearStyle != '':
            self.userChoices.yearStyle = yearStyle
        if self.userChoices.yearStyle == None:
            self.userChoices.yearStyle = self.Config.userYearStyle
        self.__yearStyle = self.userChoices.yearStyle

        if projectName != None and projectName != '':
            self.userChoices.projectName = projectName
        if self.userChoices.projectName == None:
            self.userChoices.projectName = self.Config.userProjectName
        self.__projectName = self.userChoices.projectName


        pub.subscribe(self.statusListener, 'STATUS')
        pub.subscribe(self.actionsListener, 'ACTIONS')
        pub.subscribe(self.progressListener, 'PROGRESS')

    def statusListener(self, status, value):
        print(status, value)

    def actionsListener(self, source, target, action):
        print(source, target, action)

    def progressListener(self, value):
        print('Progress %d' % value)

    def getFoldersProcessed(self):
        return self.Import.getFoldersProcessed()

    def getCountsOfFilesInSource(self):
        return self.Import.getCountsOfFilesInSource(self.userChoices)

    def getFileCount(self):
        return self.Import.fileCount

    @property
    def sourceFolder(self):
        return self.__sourceFolder
    @sourceFolder.setter
    def sourceFolder(self, value):
        self.__sourceFolder=value

    @property
    def targetFolder(self):
        return self.__targetFolder
    @targetFolder.setter
    def targetFolder(self, value):
        self.__targetFolder = value

    @property
    def sourceFile(self):
        return self.__sourceFile
    @sourceFile.setter
    def sourceFile(self, value):
        self.__sourceFile = value

    @property
    def targetFile(self):
        return self.__targetFile
    @targetFile.setter
    def targetFile(self, value):
        self.__targetFile = value

    @property
    def folderStyle(self):
        return self.__folderStyle
    @folderStyle.setter
    def folderStyle(self, value):
        self.__folderStyle = value

    @property
    def fileStyle(self):
        return self.__fileStyle
    @fileStyle.setter
    def fileStyle(self, value):
        self.__fileStyle = value

    @property
    def yearStyle(self):
        return self.__yearStyle
    @yearStyle.setter
    def yearStyle(self, value):
        self.__yearStyle = value

    @property
    def projectName(self):
        return self.__projectName
    @projectName.setter
    def projectName(self, value):
        self.__projectName = value
        
    def getSampleTargetPath(self):
        folder = self.Import.makeTargetFolder(self.userChoices, datetime.strptime('2019-12-25', '%Y-%m-%d').timestamp(), 'Photos')
        file = self.Import.makeTargetFilename(self.userChoices, 'IMG1234ABC.jpg', datetime.strptime('2019-12-25 15:30:55', '%Y-%m-%d %H:%M:%S').timestamp() , 1234)
        folder = folder.replace(self.userChoices.targetFolder,'')
        return folder + '/' + file

    def start(self):
        # https://pypi.org/project/pynput/
        self.listener = keyboard.Listener(on_press=self.on_keypress)
        self.listener.start()

        self.Import.start(self.userChoices)

        self.listener.stop()


    def abort(self):
        self.Import.abort()

    def on_keypress(self, key):
        if key == keyboard.Key.esc:
            self.abort()


class UserChoices():
    def __init__(self):
        self.__sourceFolder = None
        self.__targetFolder = None
        self.__sourceFile = None
        self.__targetFile = None
        self.__folderStyle = None
        self.__fileStyle = None
        self.__yearStyle = None
        self.__projectName = None


    @property
    def sourceFolder(self):
        return self.__sourceFolder
    @sourceFolder.setter
    def sourceFolder(self, value):
        self.__sourceFolder=value

    @property
    def targetFolder(self):
        return self.__targetFolder
    @targetFolder.setter
    def targetFolder(self, value):
        self.__targetFolder = value

    @property
    def sourceFile(self):
        return self.__sourceFile
    @sourceFile.setter
    def sourceFile(self, value):
        self.__sourceFile = value

    @property
    def targetFile(self):
        return self.__targetFile
    @targetFile.setter
    def targetFile(self, value):
        self.__targetFile = value

    @property
    def folderStyle(self):
        return self.__folderStyle
    @folderStyle.setter
    def folderStyle(self, value):
        self.__folderStyle = value

    @property
    def fileStyle(self):
        return self.__fileStyle
    @fileStyle.setter
    def fileStyle(self, value):
        self.__fileStyle = value

    @property
    def yearStyle(self):
        return self.__yearStyle
    @yearStyle.setter
    def yearStyle(self, value):
        self.__yearStyle = value

    @property
    def projectName(self):
        return self.__projectName
    @projectName.setter
    def projectName(self, value):
        self.__projectName = value


class Config():
    """ This class is the persistent storage layer
        and gets and sets the static vars, as well as the user options
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        if not os.path.exists('mediaimporterconfig.ini'):
            self.config.add_section('OUTPUT')
            self.write_file()

        #defaults
        self.debug_default = '1'
        self.con_default = '0'
        self.gui_default = '1'
        self.media_types_default = ('Photos','Videos','Audio')
        self.media_type_extensions_default = (('3fr', 'ari', 'arw', 'srf', 'sr2', 'bay', 'cri', 'crw', 'cr2', 'cr3', 'cap', 'iiq', 'eip', 'dcs', 'dcr', 'drf', 'k25', 'kdc', 'dng', 'erf', 'fff', 'mef', 'mdc', 'mos', 'mrw', 'nef', 'nrw', 'orf', 'pef', 'ptx', 'pxn', 'R3D', 'raf', 'raw', 'rw2', 'raw', 'rwl', 'dng', 'rwz', 'srw', 'x3f', 'x3f','jpg','tif'), \
        ('mp4','mov','flv','wmv','avi'), \
        ('mp3','wav','au','aiff','wma','aac','flac','m4a'))
        self.folder_styles_default = ('[type]/[date]','[date]/[type]','[date]','[type]','[projectname]/[type]/[date]')
        self.file_styles_default = ('[datetime]_[origid]','[datetime]', '[datetime]_[origid]_[projectname]')
        self.folder_year_style_default = 1
        self.date_fmt_default = '%Y_%m_%d'
        self.datetime_fmt_default = '%Y_%m_%d_%H_%M_%S'
        self.project_name_default = '##None##'

        self._debug = None
        self._gui = None
        self._con = None

        self._source_folder = None
        self._target_folder = None
        self._folder_style = None
        self._file_style = None
        self._year_style = None
        self._project_name = None

        self.read_file()
        if not self.config.has_section('OUTPUT'):
            self.config.add_section('OUTPUT')
            #print('created OUTPUT')
        if not self.config.has_section('USER'):
            self.config.add_section('USER')
            #print('created USER')
        if not self.config.has_section('GLOBAL'):
            self.config.add_section('GLOBAL')
            #print('created GLOBAL')
        if not self.config.has_option('GLOBAL','# default folder_styles'):
            self.config['GLOBAL']['# default folder_styles'] = ', '.join(self.folder_styles_default)
        if not self.config.has_option('GLOBAL','# default file_styles'):
            self.config['GLOBAL']['# default file_styles'] = ', '.join(self.file_styles_default)
        self.read_file()

    def write_file(self):
        self.config.write(open('mediaimporterconfig.ini','w'))
    def read_file(self):
        self.config.read('mediaimporterconfig.ini')

    def getDebug(self):
        if not self.config.has_option('OUTPUT','debug'):
            self.config['OUTPUT']['debug'] = self.debug_default   # 0 = none | 1 = CON | 2 = GUI | 3 = CON + GUI
            self.write_file()
            #print('created missing style : debug')
        s = self.config.getint('OUTPUT','debug')
        return s
    @property
    def useDebug(self):
        if self._debug == None:
            s = self.getDebug()
        else:
            s = self._debug
        return s
    @useDebug.setter
    def useDebug(self, value):
        self._debug = value

    def getCON(self):
        if not self.config.has_option('OUTPUT','con'):
            self.config['OUTPUT']['con'] = self.con_default
            self.write_file()
            #print('created missing style : con')
        s = self.config.getint('OUTPUT','con')
        return s
    @property
    def useCON(self):
        if self._con == None:
            s = self.getCON()
        else:
            s = self._con
        return s
    @useCON.setter
    def useCON(self, value):
        self._con = value

    def getGUI(self):
        if not self.config.has_option('OUTPUT','gui'):
            self.config['OUTPUT']['gui'] = self.gui_default
            self.write_file()
            #print('created missing style : gui')
        s = self.config.getint('OUTPUT','gui')
        return s
    @property
    def useGUI(self):
        if self._gui == None:
            s = self.getGUI()
        else:
            s = self._gui
        return s
    @useGUI.setter
    def useGUI(self, value):
        self._gui = value

    def getMediaTypes(self):
        # if the Types option doesn't exist, add it using the Defaults above, and add the Default Extensions
        if not self.config.has_option('GLOBAL','media_types'):
            self.config['GLOBAL']['media_types'] = ', '.join(self.media_types_default)
            self.write_file()
            #print('created default types')
        for t,e in zip(self.media_types_default, self.media_type_extensions_default):
            #print(t,e)
            if not self.config.has_option('GLOBAL',t):
                self.config['GLOBAL'][t] = ', '.join(e)
                self.write_file()
                #print('created default media type extensions')
        types = self.config.get('GLOBAL','media_types')
        return tuple(types.split(', '))
    @property
    def MediaTypes(self):
        return self.getMediaTypes()

    def getMediaTypeExtensions(self):
        if not self.config.has_option('GLOBAL','media_types'):
            getMediaTypes()
        extensions = []
        types = self.config.get('GLOBAL','media_types')
        #print(types)
        for t in types.split(', '):
            # make sure it exists
            if not self.config.has_option('GLOBAL',t):
                self.config['GLOBAL'][t] = ''
                self.write_file()
                #print('created missing media type extension')
            e = self.config.get('GLOBAL',t)
            #print(t, e)
            extensions.append(tuple(e.split(', ')))
        return tuple(extensions)
    @property
    def MediaTypeExtensions(self):
        return self.getMediaTypeExtensions()
#end types

#styles
    def getFolderStyles(self):
        self.read_file()
        """if not self.config.has_option('GLOBAL','# default folder_styles'):
            self.config['GLOBAL']['# default folder_styles'] = ', '.join(self.folder_styles_default)
            self.write_file()
            self.read_file()
        """
        if not self.config.has_option('GLOBAL','folder_styles'):
            self.config['GLOBAL']['folder_styles'] = ', '.join(self.folder_styles_default)
            self.write_file()
            #print('created missing style : folder_styles')
        s = self.config.get('GLOBAL','folder_styles')
        return tuple(s.split(', '))

    def getFileStyles(self):
        self.read_file()
        """if not self.config.has_option('GLOBAL','# default file_styles'):
            self.config['GLOBAL']['# default file_styles'] = ', '.join(self.file_styles_default)
            self.write_file()
            self.read_file()
        """
        if not self.config.has_option('GLOBAL','file_styles'):
            self.config['GLOBAL']['file_styles'] = ', '.join(self.file_styles_default)
            self.write_file()
            #print('created missing style : file_styles')
        s = self.config.get('GLOBAL','file_styles')
        return tuple(s.split(', '))

    def getFolderYearStyle(self):
        self.read_file()
        if not self.config.has_option('GLOBAL','folder_year_style'):
            self.config['GLOBAL']['folder_year_style'] = str(self.folder_year_style_default)
            self.write_file()
            #print('created missing style : folder_year_style')
        s = self.config.getboolean('GLOBAL','folder_year_style')
        return s

    def getDateFmt(self):
        self.read_file()
        if not self.config.has_option('GLOBAL','date_fmt'):
            self.config['GLOBAL']['date_fmt'] = self.date_fmt_default.replace('%','%%')
            self.write_file()
            #print('created missing style : date_fmt')
        s = self.config.get('GLOBAL','date_fmt')
        return s.replace('%%','%')

    def getDateTimeFmt(self):
        self.read_file()
        if not self.config.has_option('GLOBAL','datetime_fmt'):
            self.config['GLOBAL']['datetime_fmt'] = self.datetime_fmt_default.replace('%','%%')
            self.write_file()
            #print('created missing style : datetime_fmt')
        s = self.config.get('GLOBAL','datetime_fmt')
        return s.replace('%%','%')
#end styles

# user choices
    def getSourceFolder(self):
        self.read_file()
        if not self.config.has_option('USER','source_folder'):
            self.config['USER']['source_folder'] = 'x:\\'
            self.write_file()
            #print('created missing user option : source_folder')
        s = self.config.get('USER','source_folder')
        return s
    @property
    def userSourceFolder(self):
        #print("userSourceFolder",self._source_folder)
        if self._source_folder == None:
            s = self.getSourceFolder()
        else:
            s = self._source_folder
        return s
    @userSourceFolder.setter
    def userSourceFolder(self, value):
        self._source_folder = value

    def getTargetFolder(self):
        self.read_file()
        if not self.config.has_option('USER','target_folder'):
            self.config['USER']['target_folder'] = 'y:\\'
            self.write_file()
            #print('created missing user option : target_folder')
        s = self.config.get('USER','target_folder')
        return s
    @property
    def userTargetFolder(self):
        if self._target_folder == None:
            s = self.getTargetFolder()
        else:
            s = self._target_folder
        return s
    @userTargetFolder.setter
    def userTargetFolder(self, value):
        self._target_folder = value

    def getFolderStyle(self):
        self.read_file()
        if not self.config.has_option('USER','folder_style'):
            self.config['USER']['folder_style'] = self.getFolderStyles()[0]
            self.write_file()
            #print('created missing user option : folder_style')
        s = self.config.get('USER','folder_style')
        return s
    @property
    def userFolderStyle(self):
        if self._folder_style == None:
            s = self.getFolderStyle()
        else:
            s = self._folder_style
        return s
    @userFolderStyle.setter
    def userFolderStyle(self, value):
        self._folder_style = value

    def getFileStyle(self):
        self.read_file()
        if not self.config.has_option('USER','file_style'):
            self.config['USER']['file_style'] = self.getFileStyles()[0]
            self.write_file()
            #print('created missing user option : file_style')
        s = self.config.get('USER','file_style')
        return s
    @property
    def userFileStyle(self):
        if self._file_style == None:
            s = self.getFileStyle()
        else:
            s = self._file_style
        return s
    @userFileStyle.setter
    def userFileStyle(self, value):
        self._file_style = value

    def getYearStyle(self):
        self.read_file()
        if not self.config.has_option('USER','year_style'):
            self.config['USER']['year_style'] = str(self.folder_year_style_default)
            self.write_file()
            #print('created missing user option : year_style')
        s = self.config.getboolean('USER','year_style')
        return s
    @property
    def userYearStyle(self):
        if self._year_style == None:
            s = self.getYearStyle()
        else:
            s = self._year_style
        return s
    @userYearStyle.setter
    def userYearStyle(self, value):
        self._year_style = value

    def getProjectName(self):
        self.read_file()
        if not self.config.has_option('USER','project_name'):
            self.config['USER']['project_name'] = str(self.project_name_default)
            self.write_file()
            #print('created missing user option : project_name')
        s = self.config.get('USER','project_name')
        if s == '##None##':
            s = None
        return s
    @property
    def userProjectName(self):
        if self._project_name == None:
            s = self.getProjectName()
        else:
            s = self._project_name
        return s
    @userProjectName.setter
    def userProjectName(self, value):
        self._project_name = value
# end user choices

    def setSaveUserSettings(self):
        #print(self._source_folder, self._target_folder, self._folder_style, self._file_style, self._year_style)
        self.config.set('USER','source_folder', self._source_folder)
        self.config.set('USER','target_folder', self._target_folder)
        self.config.set('USER','folder_style', self._folder_style)
        self.config.set('USER','file_style', self._file_style)
        self.config.set('USER','year_style', str(self._year_style))
        self.write_file()


class Import():
    def __init__(self, debug=False):
        self.Config = Config()
        self.debug = self.Config.useDebug
        self._wantAbort = False
        self.__fileCount = 0
        self.__typeCount = 0
        self.__foldersProcessed = []

    @property
    def fileCount(self):
        return self.__fileCount
    @fileCount.setter
    def fileCount(self, value):
        self.__fileCount = value

    @property
    def typeCount(self):
        return self.__typeCount
    @typeCount.setter
    def typeCount(self, value):
        self.__typeCount = value

    def getCountsOfFilesInSource(self, UserChoices):
        sourceFolder = UserChoices.sourceFolder
        mediaFiles = {}  #dictionary
        for type_offset,type_name in enumerate(self.Config.MediaTypes):
            count = 0
            for root, dirs, files in os.walk(sourceFolder):
                for filename in files:
                    if filename.lower().endswith(self.Config.MediaTypeExtensions[type_offset]):
                        count+=1
            #print(type_name,count)
            mediaFiles.update({type_name:count})
        return mediaFiles

    def getFoldersProcessed(self):
        return list(dict.fromkeys(self.__foldersProcessed))
    def setFoldersProcessed(self, value):
        self.__foldersProcessed.append(value)
    def resetFoldersProcessed(self):
        self.__foldersProcessed = []

    def getFileModifiedDate(self, pathToFile):
        return os.path.getmtime(pathToFile)

    def getFileCreatedDate(self, pathToFile):
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == 'Windows':
            return os.path.getctime(pathToFile)
        else:
            stat = os.stat(pathToFile)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime

    def getFileDate(self, pathToFile):
        createdDate = self.getFileCreatedDate(pathToFile)
        modifiedDate = self.getFileModifiedDate(pathToFile)
        if createdDate <= datetime.strptime('1980-01-01','%Y-%m-%d').timestamp() or createdDate > modifiedDate:
            return modifiedDate
        else:
            return createdDate

    def getFileSuffix(self, filename):
        # last four characters - on most media this should be an int.
        return os.path.splitext(filename)[0][-4:]

    def getFileExtension(self, filename):
        return os.path.splitext(filename)[1]

    def makeTargetFolder(self, UserChoices, fileDate, mediaType):
        target_folder = UserChoices.folderStyle.replace('[type]', mediaType)
        if UserChoices.yearStyle == True:
                            target_folder = target_folder.replace('[date]',time.strftime('%Y',time.localtime(fileDate))+'/[date]')
        target_folder = target_folder.replace('[date]', time.strftime(self.Config.getDateFmt(), time.localtime(fileDate)))
        target_folder = target_folder.replace('[projectname]', self.cleanProjectName(UserChoices.projectName))
        target_folder = '/'.join(filter(None,[UserChoices.targetFolder, target_folder]))
        return target_folder

    def makeTargetFilename(self, UserChoices, fileName, fileDate, count):
        target_file = UserChoices.fileStyle.replace('[datetime]', time.strftime(self.Config.getDateTimeFmt(), time.localtime(fileDate)))
        fileSuffix = self.getFileSuffix(fileName)
        if not fileSuffix.isdigit():
            fileSuffix = '{0:04d}'.format(count)
        target_file = target_file.replace('[origid]', fileSuffix)
        target_file = target_file.replace('[projectname]', self.cleanProjectName(UserChoices.projectName))
        target_file = target_file + self.getFileExtension(fileName)
        return target_file

    def cleanFolderName(self, folderName):
        folderName = folderName.replace('\\','/')
        if (folderName[-1:] == '/'):
            folderName = folderName[:-1]
        return folderName
        
    def cleanProjectName(self, projectName):
        if projectName == None:
            return 'NoProjectName'
        projectName = re.sub(' ', '_', projectName)
        projectName = re.sub('[^0-9a-zA-Z-._]+', '', projectName)
        if len(projectName) == 0:
            projectName = 'InvalidProjectName'
        return projectName

    def targetPathExists(self, pathName):
        return pathlib.Path(pathName).exists()

    def createFolder(self, folderName):
        return pathlib.Path(folderName).mkdir(parents=True, exist_ok=True)

    def copyFile(self, sourcePath, targetPath):
        try:
            shutil.copy2(sourcePath, targetPath)
            if self.debug == True:
                raise Exception('debug','copy fail test!')
        except (shutil.Error, IOError, OSError, Exception)  as e:
            #print('Error: %s' % e)
            return 'Error: ' + repr(e)
        else:
            return 'Copied'

    def abort(self):
        self._wantAbort = True

    def start(self,UserChoices):
        x = threading.Thread(target=self.runThreaded, args=(UserChoices,))
        x.start()
        x.join()

    def runThreaded(self, UserChoices):
        self.userChoices = UserChoices
        self.resetFoldersProcessed()
        self.fileCount = 0
        UserChoices.sourceFolder = self.cleanFolderName(UserChoices.sourceFolder)
        UserChoices.targetFolder = self.cleanFolderName(UserChoices.targetFolder)

        mediaFiles = self.getCountsOfFilesInSource(UserChoices)
        totalFiles = 0
        for value in mediaFiles.values():
            totalFiles += value
        
        #if '[projectname]' in UserChoices.fileStyle or '[projectname]' in UserChoices.folderStyle:
        #    UserChoices.projectName = cleanProjectName(UserChoices.ProjectName)
        
        pub.sendMessage('STATUS', status='copying', value='started')
        for type_offset,type_name in enumerate(self.Config.MediaTypes):
            self.typeCount = 0
            pub.sendMessage('STATUS', status='mediaType', value=type_name)

            for root, dirs, files in os.walk(UserChoices.sourceFolder):
                for filename in files:
                    if self._wantAbort:
                        pub.sendMessage('STATUS', status='abort', value='ABORT')
                        return
                    if filename.lower().endswith(self.Config.MediaTypeExtensions[type_offset]):
                        self.typeCount += 1
                        pub.sendMessage('STATUS', status='typeCount', value=self.typeCount)
                        sourcePath = '/'.join([root,filename])
                        fileDate = self.getFileDate(sourcePath)
                        targetFolder = self.makeTargetFolder(UserChoices, fileDate, type_name)
                        targetFile = self.makeTargetFilename(UserChoices, filename, fileDate, self.typeCount)
                        targetPath = '/'.join([targetFolder,targetFile])

                        self.fileCount += 1
                        pub.sendMessage('STATUS', status='fileCount', value=self.fileCount)

                        if not self.targetPathExists(targetFolder):
                            self.createFolder(targetFolder)

                        if not self.targetPathExists(targetPath):
                            copyMessage = self.copyFile(sourcePath, targetPath)
                            self.fileAction = copyMessage
                         #   print(sourcePath, targetPath, copyMessage )

                            pub.sendMessage( 'ACTIONS', source=sourcePath, target=targetPath, action=copyMessage)

                            self.setFoldersProcessed(targetFolder.replace(UserChoices.targetFolder,''))
                        else:
                            self.fileAction = 'Skipped'
                            #print(sourcePath, targetPath, 'Skipped' )
                            pub.sendMessage( 'ACTIONS', source=sourcePath, target=targetPath, action='Skipped')

                        progressPercent = self.fileCount / totalFiles * 100
                        pub.sendMessage('PROGRESS', value=progressPercent)

                    #time.sleep(0.25)

        pub.sendMessage('STATUS', status='copying', value='finished')