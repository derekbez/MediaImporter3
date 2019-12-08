# MediaImporter3
Import media files - photos, videos, audio - into appropriate locations, and rename the files consistently.

While Lightroom will import and rename files from SD/CF cards, it puts all photos and videos in the same place, which may not be optimal for processing in different applications and general media management.

MediaImporter3 separates Photos, Videos and Audio media types into locations appropriate to your style of working.  Technically it can handle any files - the "type" is determined by the file extension, and is congifurable in the mediaimporterconfig.ini file.

The default media types are:
'Photos','Videos','Audio'

The default extensions are:
Photos:
'3fr', 'ari', 'arw', 'srf', 'sr2', 'bay', 'cri', 'crw', 'cr2', 'cr3', 'cap', 'iiq', 'eip', 'dcs', 'dcr', 'drf', 'k25', 'kdc', 'dng', 'erf', 'fff', 'mef', 'mdc', 'mos', 'mrw', 'nef', 'nrw', 'orf', 'pef', 'ptx', 'pxn', 'R3D', 'raf', 'raw', 'rw2', 'raw', 'rwl', 'dng', 'rwz', 'srw', 'x3f', 'x3f','jpg','tif'
Videos:
'mp4','mov','flv','wmv','avi'
Audio:
'mp3','wav','au','aiff','wma','aac','flac','m4a'

The default Folder Styles are:
'[type]/[date]','[date]/[type]','[date]','[type]','[projectname]/[type]/[date]'

The default File Styles are:
'[datetime]_[origid]','[datetime]', '[datetime]_[origid]_[projectname]'