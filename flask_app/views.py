from .app import app

@app.route("/")
def index():
    raise Exception()
    return """<html>
    <head>
    <style>
    .center {
    text-align: center;
    }
    </style>
    </head>
    <body>
    <div class="center">
    <h1>Success!</h1>
    <img src="http://rack.1.mshcdn.com/media/ZgkyMDEzLzA4LzA1Lzk3LzMwcm9jay40ZDgyNC5naWYKcAl0aHVtYgk4NTB4NTkwPgplCWpwZw/f1b84963/086/30-rock.jpg">
    <div>Now all you have to do is write some code...</div>
    </div></body></html>"""
