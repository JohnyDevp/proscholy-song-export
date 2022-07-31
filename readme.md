ProScholy song-book PPT, PDF EXPORT
====

Autor
-----
Jan Holáň, 2022 <br>
Under Creative Commons Licence
 
Files
---
- readme.md - short documentation
- server.py - flask server handling requests
- exportpdf.py - module handling all export tasks
- props.py - module consisting of helper objects

Run
---
In bash:
<pre>
$ export FLASK_APP=server
$ flask run
</pre>

Then go to the IP address and port which has been written out in terminal (usually 127.0.0.1:5000). For detailed usage continue
below.

Description of usage
---
Song can be exported at link <pre>/export_song</pre> with parameters:
- songnumber ... the only REQUIRED parameter - song id in database
(The rest of parameters are optional and so has its own default value if not set)
- resx ... X component of resolution of desired output
- resy ... Y component of resolution of desired output
- fileformat ... either pdf or ppt
- songformat ... consists of numbers (representing verses) and letters 'B' or 'R' or 'C' (B for bridge and both R and C for chorus)

Example
---
<pre>
- 127.0.0.1:5000/export_song (default page of API)
- 127.0.0.1:5000/export_song?songnumber=3 (only one parameter - the required one, specifying which song to download)
- 127.0.0.1:5000/export_song?songnumber=7&resx=1920&resy=1080&fileformat=pdf&songformat=12BR
</pre>

Exceptions
---
When any exception occurse it appears usually in web browser, sometimes also the description of it is shown in terminal on server. <br>
Mistakes or errors considering parameters are left without any warning.
