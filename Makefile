cleanpdf:
	rm -f *.pdf

zip:
	zip proscholy_song_export.zip server.py exportpdf.py props.py readme.pdf readme.md
