DB_HOST = '127.0.0.1'
DB_PORT = 27017
DB_NAME = 'test_database'

PARSE_HTML = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset='utf-8'/>
        <title>TestHTML</title>
    </head>
    <body>
        <div class="container">
            <p>HTML parse test</p>
        </div>
    </body>
</html>"""


ORDER_HOST = "127.0.0.1"
ORDER_PORT = "8888"
ORDER_URL = "http://{0}:{1}".format(ORDER_HOST, ORDER_PORT)
ORDER_UA = "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
