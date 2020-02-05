# MediaImporter3
Import media files - photos, videos, audio - into appropriate locations, and rename the files consistently.

While Adobe Lightroom will import and rename files from SD/CF cards, it puts all photos and videos in the same place, which may not be optimal for processing in different applications and general media management.  To keep all my photos (and videos and audio files) neat and tidy, I want them renamed from IMG00001 to the date-time it was taken. And, for me, I want them in date folders.  While Lightroom Import module mostly does this, it puts all photos and videos in the same place, which isn't appropriate.  And it doesn't handle audio files from a Zoom or other recorder.

MediaImporter3 separates Photos, Videos and Audio media types into locations appropriate to your style of working.  Technically it can handle any files - the "type" is determined by the file extension, and is congifurable in the mediaimporterconfig.ini file.
---

Works like this:
Source Folder is your SD or CF card (or it could be an existing folder on your drive).
Target Folder is where you want the media files copied to.

Folder Style and File Style describe the way the files will be renamed when they are copied.  Watch the Sample as you select different options.

When you change the Source Folder, you can see how many of each Type will be copied.

Click Start button and watch it copy...
---

The first time you run it, you will notice that it creates an mediaimporterconfig.ini file in the same folder.  You can edit this file to change the defaults in the [USER] section to suit your needs.  You could change stuff in the [GLOBAL] section too.  Some things you could do by manipulating the [GLOBAL] section:
- Add custom Folder and File styles, so long as you use the tags (eg: [date]).
- Split the Photos Type into Photos-RAW and Photos-JPG.
- Change the date format to use - (dashes) instead of _ (underscores).  Strongly recommend keeping the yearmonthday structure so files sort appropriately though.
---

The application can be run in console mode too.  
See: mi.exe --help
If running in console mode regularly, it may be prudent to change the config settings for GUI and CON.
---

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

---
The application is written in Python, and should run on OSX and Linux (tested on Raspberry Pi).

Github repository:
https://github.com/derekbez/MediaImporter3

All feedback welcome.