import os, time
from serv import HTTPError


def serve_static(address, root):

    size = len(address)

    def pattern(request):
        return request.url.startswith(address)

    def handler(request):

        fd = "%s/%s" % (root, request.url[size:])
        stat = os.stat(fd)

        if 'IF-MODIFIED-SINCE' in request.headers:
            if time.mktime(time.strptime(request.headers['IF-MODIFIED-SINCE'], '%a, %d %b %Y %H:%I:%S GMT')) > stat.st_mtime:
                request.reply('', '304', 'Not modified')
                return

        try:
            request.start_response(content_length=str(stat.st_size))
            return open(fd)

        except IOError:

            if IOError.errno == 2:
                raise HTTPError(404) # No such file or directory

            if IOError.errno == 13:
                raise HTTPError(403) # Permission denied

            if IOError.errno == 21:
                raise HTTPError(403) # Is a directory

    return pattern, handler
