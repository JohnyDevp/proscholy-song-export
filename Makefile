clean:
	rm -f *.pdf !("readme.pdf")
zip:
	zip proscholy_song_export.zip server.py exportpdf.py props.py readme.pdf readme.md
