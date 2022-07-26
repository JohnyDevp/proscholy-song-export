import pdfkit

html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body>
    <p>&euro;</p>
    <p>áéíóúñö</p>
<body>
</html>
"""

pdfkit.from_string(html_content, 'out.pdf')