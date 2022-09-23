run:
	export PYTHONPATH="/home/johnny/code_repo/proScholy/proscholy-song-export/src:/home/johnny/code_repo/proScholy/proscholy-song-export"

cleanpdf:
	rm -f *.pdf

zip:
	zip proscholy_song_export.zip server.py exportpdf.py props.py readme.pdf readme.md
