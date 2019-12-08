import unittest
import os
from mediaimporter import UserChoices
from mediaimporter import Config
from mediaimporter import Import
from mediaimporter import MediaImporter

class Tests(unittest.TestCase):
    
    def setUp(self):
        self.userChoices = UserChoices()       
        self.Config = Config()
        self.Import = Import()
        self.mediaImporter = MediaImporter()
    
    def test_userChoice_sourceFolder_equalsNone(self):
        sourceFolder = self.userChoices.sourceFolder
        self.assertEqual(sourceFolder, None)

    def test_userChoice_sourceFolder_equalstestvalue(self):     
        self.userChoices.sourceFolder = 'testvalue'
        sourceFolder = self.userChoices.sourceFolder
        self.assertEqual(sourceFolder, 'testvalue')
        
    def test_userChoice_targetFolder_equalsNone(self):
        targetFolder = self.userChoices.targetFolder
        self.assertEqual(targetFolder, None)
        
    def test_userChoice_targetFolder_equalstestvalue(self):
        self.userChoices.targetFolder = 'testvalue'
        targetFolder = self.userChoices.targetFolder
        self.assertEqual(targetFolder, 'testvalue')
        
    def test_userChoice_sourceFile_equalsNone(self):
        sourceFile = self.userChoices.sourceFile
        self.assertEqual(sourceFile, None)

    def test_userChoice_sourceFile_equalstestvalue(self):     
        self.userChoices.sourceFile = 'testvalue'
        sourceFile = self.userChoices.sourceFile
        self.assertEqual(sourceFile, 'testvalue')

    def test_userChoice_targetFile_equalsNone(self):
        targetFile = self.userChoices.targetFile
        self.assertEqual(targetFile, None)
        
    def test_userChoice_targetFile_equalstestvalue(self):
        self.userChoices.targetFile = 'testvalue'
        targetFile = self.userChoices.targetFile
        self.assertEqual(targetFile, 'testvalue')    
        
    def test_userChoice_folderStyle_equalsNone(self):
        folderStyle = self.userChoices.folderStyle
        self.assertEqual(folderStyle, None)
        
    def test_userChoice_folderStyle_equalstestvalue(self):
        self.userChoices.folderStyle = 'testvalue'
        folderStyle = self.userChoices.folderStyle
        self.assertEqual(folderStyle, 'testvalue')      
        
    def test_userChoice_fileStyle_equalsNone(self):
        fileStyle = self.userChoices.fileStyle
        self.assertEqual(fileStyle, None)
        
    def test_userChoice_fileStyle_equalstestvalue(self):
        self.userChoices.fileStyle = 'testvalue'
        fileStyle = self.userChoices.fileStyle
        self.assertEqual(fileStyle, 'testvalue')           

    def test_userChoice_yearStyle_equalsNone(self):
        yearStyle = self.userChoices.yearStyle
        self.assertEqual(yearStyle, None)
        
    def test_userChoice_yearStyle_equalstestvalue(self):
        self.userChoices.yearStyle = 'testvalue'
        yearStyle = self.userChoices.yearStyle
        self.assertEqual(yearStyle, 'testvalue') 

    def test_userChoice_projectName_equalsNone(self):
        projectName = self.userChoices.projectName
        self.assertEqual(projectName, None)
        
    def test_userChoice_projectName_equalstestvalue(self):
        self.userChoices.projectName = 'testvalue'
        projectName = self.userChoices.projectName
        self.assertEqual(projectName, 'testvalue')          

    # config
    def test_Config_useDebug_equals1(self):
        useDebug = self.Config.useDebug
        self.assertEqual(useDebug, 1)
        
    def test_Config_useCON_equals1(self):
        useCON = self.Config.useCON
        self.assertEqual(useCON, 1)
        
    def test_Config_useGUI_equals1(self):
        useGUI = self.Config.useGUI
        self.assertEqual(useGUI, 1)    
        
    def test_Config_MediaTypes_default(self):
        types = self.Config.MediaTypes
        self.assertTupleEqual(types, ('Photos','Videos','Audio'))

    def test_Config_MediaTypeExtensions_tuplesize(self):
        typeExtensionsLen = len(self.Config.MediaTypeExtensions)
        typesLen = len(self.Config.getMediaTypes())
        self.assertEqual(typesLen, typeExtensionsLen)
        
    #def test_Config_getFolderStyles_default(self):
    #    folderStyles = self.Config.getFolderStyles()
    #    self.assertTupleEqual(folderStyles, ('[type]/[date]','[date]/[type]','[date]','[type]'))        
        
    #def test_Config_getFileStyles_default(self):
    #    FileStyles = self.Config.getFileStyles()
    #    self.assertTupleEqual(FileStyles, ('[datetime]_[origid]','[datetime]'))     
        
    def test_Config_getFolderYearStyle_equals1(self):
        FolderYearStyle = self.Config.getFolderYearStyle()
        self.assertEqual(FolderYearStyle, 1)    
        
    def test_Config_getDateFmt_default(self):
        dateFmt = self.Config.getDateFmt()
        self.assertEqual(dateFmt, '%Y_%m_%d')     
        
    def test_Config_getDateFmt_default(self):
        dateTimeFmt = self.Config.getDateTimeFmt()
        self.assertEqual(dateTimeFmt, '%Y_%m_%d_%H_%M_%S')    
        
    def test_Config_userSourceFolder_default(self):
        userSourceFolderOrig = self.Config.userSourceFolder
        self.Config.userSourceFolder = 'xxxx'
        userSourceFolder = self.Config.userSourceFolder
        self.assertEqual(userSourceFolder, 'xxxx')      
        self.Config.userSourceFolder = userSourceFolderOrig
        
    def test_Config_userTargetFolder_default(self):
        userTargetFolderOrig = self.Config.userTargetFolder
        self.Config.userTargetFolder = 'xxxx'
        userTargetFolder = self.Config.userTargetFolder
        self.assertEqual(userTargetFolder, 'xxxx')      
        self.Config.userTargetFolder = userTargetFolderOrig    
        
    def test_Config_userFolderStyle_default(self):
        userFolderStyleOrig = self.Config.userFolderStyle
        self.Config.userFolderStyle = 'xxxx'
        userFolderStyle = self.Config.userFolderStyle
        self.assertEqual(userFolderStyle, 'xxxx')      
        self.Config.userFolderStyle = userFolderStyleOrig     
        
    def test_Config_userFileStyle_default(self):
        userFileStyleOrig = self.Config.userFileStyle
        self.Config.userFileStyle = 'xxxx'
        userFileStyle = self.Config.userFileStyle
        self.assertEqual(userFileStyle, 'xxxx')      
        self.Config.userFileStyle = userFileStyleOrig     

    def test_Config_userYearStyle_default(self):
        userYearStyleOrig = self.Config.userYearStyle
        self.Config.userYearStyle = 'xxxx'
        userYearStyle = self.Config.userYearStyle
        self.assertEqual(userYearStyle, 'xxxx')      
        self.Config.userYearStyle = userYearStyleOrig     

    def test_Config_projectName_default(self):
        projectName = self.Config.userProjectName
        self.assertIsNone(projectName)

    #Import
    def test_Import_getCountsOfFilesInSource_default(self):
        self.userChoices.sourceFolder = '.\\test\\tempsource'
        CountsMediaInSource = self.Import.getCountsOfFilesInSource(self.userChoices)
        self.assertEqual(CountsMediaInSource['Photos'],11)
        self.assertEqual(CountsMediaInSource['Videos'],3)
        self.assertEqual(CountsMediaInSource['Audio'],2)
        
        
    def test_Import_getFileModifiedDate_firstfileintestsource(self):
        self.userChoices.sourceFolder = '.\\test\\tempsource\\'
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        modifiedTime = self.Import.getFileModifiedDate(self.userChoices.sourceFolder + sourceFilename)
        #print(modifiedTime)
        self.assertEqual(modifiedTime, 1328390293.7891483)
        
    def test_Import_getFileCreatedDate_firstfileintestsource(self):
        self.userChoices.sourceFolder = '.\\test\\tempsource\\'
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        createdTime = self.Import.getFileCreatedDate(self.userChoices.sourceFolder + sourceFilename)
        #print(createdTime)
        self.assertEqual(createdTime, 1575298494.3014073)    
        
    def test_Import_getFileDate_firstfileintestsource(self):
        self.userChoices.sourceFolder = '.\\test\\tempsource\\'
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        fileDate = self.Import.getFileDate(self.userChoices.sourceFolder + sourceFilename)
        self.assertEqual(fileDate, 1328390293.7891483)
     
    def test_Import_getFileSuffix_firstfileintestsource(self):
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        fileSuffix = self.Import.getFileSuffix(sourceFilename)
        self.assertEqual(fileSuffix, '2831')
        
    def test_Import_getFileExtension_firstfileintestsource(self):
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        fileExt = self.Import.getFileExtension(sourceFilename)
        self.assertEqual(fileExt, '.CR2')   
        
    def test_Import_makeTargetFolder_testtarget_yearstyle_false(self):
        self.userChoices.yearStyle = False
        self.userChoices.folderStyle = '[type]/[date]'
        self.userChoices.targetFolder = './test/temptarget'
        #UserTargetFolder = self.userChoices.targetFolder
        self.userChoices.sourceFolder = './test/tempsource/'
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        fileDate = self.Import.getFileDate(self.userChoices.sourceFolder + sourceFilename)
        mediaType = 'Photos'
        targetFolder = self.Import.makeTargetFolder(self.userChoices, fileDate, mediaType)
        self.assertEqual(targetFolder, './test/temptarget/Photos/2012_02_04')  
        
    def test_Import_makeTargetFolder_testtarget_yearstyle_true(self):
        self.userChoices.yearStyle = True
        self.userChoices.folderStyle = '[type]/[date]'
        self.userChoices.targetFolder = './test/temptarget'
        #UserTargetFolder = self.userChoices.targetFolder
        self.userChoices.sourceFolder = './test/tempsource/'
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        fileDate = self.Import.getFileDate(self.userChoices.sourceFolder + sourceFilename)
        mediaType = 'Photos'
        targetFolder = self.Import.makeTargetFolder(self.userChoices, fileDate, mediaType)
        self.assertEqual(targetFolder, './test/temptarget/Photos/2012/2012_02_04')        
           
    def test_Import_makeTargetFilename_firstfileintestsource_datetime_origid(self):
        self.userChoices.sourceFolder = './test/tempsource/'
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        fileDate = self.Import.getFileDate(self.userChoices.sourceFolder + sourceFilename)
        self.userChoices.fileStyle = '[datetime]_[origid]'
        fileCount = 1
        targetFilename = self.Import.makeTargetFilename(self.userChoices, sourceFilename, fileDate, fileCount)
        self.assertEqual(targetFilename, '2012_02_04_21_18_13_2831.CR2')
        
    def test_Import_makeTargetFilename_firstfileintestsource_datetime_origid_nosuffix(self):
        self.userChoices.sourceFolder = './test/tempsource/'
        sourceFilename = 'Christmas Card.jpg'
        fileDate = self.Import.getFileDate(self.userChoices.sourceFolder + sourceFilename)
        self.userChoices.fileStyle = '[datetime]_[origid]'
        fileCount = 1
        targetFilename = self.Import.makeTargetFilename(self.userChoices, sourceFilename, fileDate, fileCount)
        self.assertEqual(targetFilename, '2015_12_11_17_41_51_0001.jpg')    
        
    def test_Import_makeTargetFilename_firstfileintestsource_datetime(self):
        self.userChoices.sourceFolder = './test/tempsource/'
        sourceFilename = '2012_02_04_21_18_13_2831.CR2'
        fileDate = self.Import.getFileDate(self.userChoices.sourceFolder + sourceFilename)
        self.userChoices.fileStyle = '[datetime]'
        fileCount = 1
        targetFilename = self.Import.makeTargetFilename(self.userChoices, sourceFilename, fileDate, fileCount)
        self.assertEqual(targetFilename, '2012_02_04_21_18_13.CR2')    
    
    def test_Import_cleanFolder_notrailingslash(self):
        self.userChoices.sourceFolder = './test/tempsource/'
        folderName = self.Import.cleanFolderName(self.userChoices.sourceFolder)
        self.assertEqual(folderName,'./test/tempsource')
        
    def test_Import_cleanFolder_backslash(self):
        self.userChoices.sourceFolder = 'c:\\test\\tempsource\\'
        folderName = self.Import.cleanFolderName(self.userChoices.sourceFolder)
        self.assertEqual(folderName,'c:/test/tempsource')    
        
    def test_Import_targetPathExists_Foldertrue(self): 
        targetFolderExists = self.Import.targetPathExists('.')
        self.assertTrue(targetFolderExists)
    
    def test_Import_targetPathExists_Folderfalse(self): 
        targetFolderExists = self.Import.targetPathExists('x:/xxxxxxxxxxx')
        self.assertFalse(targetFolderExists)
    
    def test_Import_targetPathExists_Filetrue(self): 
        targetFileExists = self.Import.targetPathExists('./test/tempsource/2012_02_04_21_18_13_2831.CR2')
        self.assertTrue(targetFileExists)
    
    def test_Import_targetPathExists_Filefalse(self): 
        targetFileExists = self.Import.targetPathExists('x:/xxxxxxxxxxx/xxxxxxxxxx')
        self.assertFalse(targetFileExists)
     
    def test_Import_fileCount_0(self):
        self.Import.fileCount = 0
        self.assertEqual(self.Import.fileCount,0)
     
    def test_Import_fileCount_1(self):
        self.Import.fileCount += 1
        self.assertEqual(self.Import.fileCount,1)        

    def test_Import_typeCount_0(self):
        self.Import.typeCount = 0
        self.assertEqual(self.Import.typeCount,0)
     
    def test_Import_typeCount_1(self):
        self.Import.typeCount += 1
        self.assertEqual(self.Import.typeCount,1)         
        
    def test_Import_resetFoldersProcessed_empty(self):
        foldersProcessed = self.Import.resetFoldersProcessed()
        self.assertEqual(foldersProcessed, None)
        
    def test_Import_set_getFoldersProcessed_testvalues(self):
        self.Import.setFoldersProcessed('test1')
        self.Import.setFoldersProcessed('test2')
        foldersProcessed = self.Import.getFoldersProcessed()
        self.assertEqual(foldersProcessed, ['test1','test2'])
        
    def test_Import_cleanProjectName_nospecchars(self):
        project = self.Import.cleanProjectName('0-9a-zA-Z-._')
        self.assertEqual(project, '0-9a-zA-Z-._')
     
    def test_Import_cleanProjectName_withspecchars(self):
        project = self.Import.cleanProjectName('name1 !"£$%^&*(){}:~:#;/\|`,')
        self.assertEqual(project, 'name1_') 
        
    def test_Import_cleanProjectName_allspecchars(self):
        project = self.Import.cleanProjectName('!"£$%^&*(){}:~:#;/\|`,')
        self.assertEqual(project, 'InvalidProjectName') 

    def test_Import_cleanProjectName_none(self):
        project = self.Import.cleanProjectName(None)
        self.assertEqual(project, 'NoProjectName') 

    def test_MediaImporter_sourceFolder_notNone(self): 
        self.assertIsNotNone(self.mediaImporter.sourceFolder)
        self.assertNotEqual(self.mediaImporter.sourceFolder, '')

    def test_MediaImporter_targetFolder_notNone(self): 
        self.assertIsNotNone(self.mediaImporter.targetFolder)
        self.assertNotEqual(self.mediaImporter.targetFolder, '')

    def test_MediaImporter_folderStyle_notNone(self): 
        self.assertIsNotNone(self.mediaImporter.folderStyle)
        self.assertNotEqual(self.mediaImporter.folderStyle, '')

    def test_MediaImporter_fileStyle_notNone(self): 
        self.assertIsNotNone(self.mediaImporter.fileStyle)
        self.assertNotEqual(self.mediaImporter.fileStyle, '')
        
    def test_MediaImporter_yearStyle_notNone(self): 
        self.assertIsNotNone(self.mediaImporter.yearStyle)
        self.assertNotEqual(self.mediaImporter.yearStyle, '')    

    def test_MediaImporter_projectName_notNone(self): 
        self.mediaImporter.projectName = 'projectname'
        self.assertIsNotNone(self.mediaImporter.projectName)
        self.assertNotEqual(self.mediaImporter.projectName, '') 
        
    def test_MediaImporter_getSampleTargetPath_noproject(self):
        self.mediaImporter.userChoices.folderStyle = '[type]/[date]'
        self.mediaImporter.userChoices.fileStyle = '[datetime]_[origid]'
        self.mediaImporter.userChoices.yearStyle = 1
        self.mediaImporter.userChoices.projectName = None
        sample = self.mediaImporter.getSampleTargetPath()
        self.assertEqual(sample, '/Photos/2019/2019_12_25/2019_12_25_15_30_55_1234.jpg')
        
    def test_MediaImporter_getSampleTargetPath_withproject(self):
        self.mediaImporter.userChoices.folderStyle = '[projectname]/[type]/[date]'
        self.mediaImporter.userChoices.fileStyle = '[datetime]_[origid]'
        self.mediaImporter.userChoices.yearStyle = 0
        self.mediaImporter.userChoices.projectName = 'MyProject 1'
        sample = self.mediaImporter.getSampleTargetPath()
        self.assertEqual(sample, '/MyProject_1/Photos/2019_12_25/2019_12_25_15_30_55_1234.jpg')   

    def test_MediaImporter_getSampleTargetPath_withprojectnone(self):
        self.mediaImporter.userChoices.folderStyle = '[type]/[date]'
        self.mediaImporter.userChoices.fileStyle = '[datetime]_[origid]_[projectname]'
        self.mediaImporter.userChoices.yearStyle = 0
        self.mediaImporter.userChoices.projectName = None
        sample = self.mediaImporter.getSampleTargetPath()
        self.assertEqual(sample, '/Photos/2019_12_25/2019_12_25_15_30_55_1234_NoProjectName.jpg')        
        
        
    """
    def test_MediaImporter_Start_1(self):
        s = self.mediaImporter.start()
        self.assertEqual(s,1)
        
    def test_MediaImporter_Abort_none(self):
        s = self.mediaImporter.abort()
        self.assertIsNone(s)    
        
        
        
        
    def test_run(self):
        self.userChoices.sourceFolder = './test/tempsource/'
        self.userChoices.targetFolder = './test/temptarget/'
        self.userChoices.folderStyle = 'type/date'
        self.userChoices.fileStyle = 'datetime_origid'
        self.userChoices.yearStyle = 1
        self.Import.run(self.userChoices)
    """    
 
if __name__ == '__main__':
    unittest.main()