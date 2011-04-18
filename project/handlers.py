import os, time
from serv import HTTPError


def serve_static(address, root):
    size = len(address)

    def pattern(request):
        return request.url.startswith(address)

    def handler(request):
        filename = "%s/%s" % (root, request.url[size:])

        try:
            stat = os.stat(filename)

            if 'IF-MODIFIED-SINCE' in request.headers:
                if time.mktime(time.strptime(request.headers['IF-MODIFIED-SINCE'], '%a, %d %b %Y %H:%I:%S GMT')) < stat.st_mtime:
                    request.reply('', '304', 'Not modified')
                    return


            request.start_response(content_length=str(stat.st_size), last_modified=time.strftime('%a, %d %b %Y %H:%I:%S GMT', time.gmtime(stat.st_mtime)))
            return open(filename)

        except (OSError, IOError) as err:

            if err.errno == 2:
                raise HTTPError(404) # No such file or directory

            if err.errno == 13:
                raise HTTPError(403) # Permission denied

            if err.errno == 21:
                raise HTTPError(403) # Is a directory

    return pattern, handler
