ProScholy song-book PPT, PDF EXPORT
====

Autor
-----
Jan Holáň, 2022 <br>
Under Creative Commons Licence
 
Files
---
- doc/readme.md - short documentation
- doc/readme.pdf - short documentation for download
- src/requirements.txt - all dependencies 
- src/core.py - module handling all neccessary tasks and the exporting process
- src/props.py - module consisting of helper objects
- src/song.py - module with Song object representing the song
- server.py - flask server handling requests

Run
---
In bash on Linux:
<pre>
$ export FLASK_APP=server
$ flask run
</pre>
In PowerShell on Windows:
<pre>
> flask --app server run 
</pre>

Then go to the IP address and port which has been written out in terminal (usually 127.0.0.1:5000). For detailed usage continue
below.

Description of usage
---
Song can be exported at link <pre>/export_song</pre> with parameters:
- songnumber ... the only REQUIRED parameter - song id in database
(The rest of parameters are optional and so has its own default value if not set)
- fontfamily ... <b>arial</b>, <b>times</b>, <b>opensans</b> - representing family of font to use in exported file
- fontsize ... <b>number</b> representing size of font to use in exported file
- background ... <b>color/url</b> representing backgournd color or image
- maxlines ... <b>number</b> representing maximum of lines to appear at one slide
- fileformat ... <b>pdf</b> or <b>ppt</b> for slides or <b>rawpdf</b> for just raw pdf text 
- songformat ... <b>number</b> consists of digits (representing verses) and letters 'B' or 'R' or 'C' (B for bridge and both R and C for chorus)

Example
---
<pre>
- 127.0.0.1:5000/export_song (default page of API)
- 127.0.0.1:5000/export_song?songnumber=3 (only one parameter - the required one, specifying which song to download)
- 127.0.0.1:5000/export_song?songnumber=7&fontsize=12&fontfamily=arial&fileformat=pd    f&songformat=12BR
</pre>

Operating system differences
---
Both platforms requires all neccessary packages to be installed, so make yourself sure that this is done. (if you start the app, it will show you what package is currently missing - you will probably have to do this start-install process more times) <br>
If you are on:
- Windows - find every comment <b>WINDOWS</b>, uncomment the next lines, which are marked and comment each block of code marked with word <b>LINUX</b>. Make sure that every line you uncomment make sense considering your personal PC setup (especially paths).
- Linux - change words <b>WINDOWS</b> and <b>LINUX</b> and do the steps written above

Exceptions
---
When any exception occurs warning appears usually in web browser, sometimes also the description of it is shown in terminal on server. <br>
Mistakes or errors considering parameters are left without any warning.
