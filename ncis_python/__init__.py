from ncis import route, api_response, request
import sys
import platform

__version__ = "0.1"
__author__ = "Mathieu Virbel <mat@kivy.org>"

@route("/version")
def version():
    vi = sys.version_info
    un = platform.uname()
    return api_response({
        "version": sys.version,
        "version_info": {
            "major": vi.major,
            "minor": vi.minor,
            "micro": vi.micro,
            "releaselevel": vi.releaselevel,
            "serial": vi.serial
        },
        "platform": {
            "system": un.system,
            "node": un.node,
            "release": un.release,
            "version": un.version,
            "machine": un.machine,
            "processor": un.processor
        }
    })


@route("/modules")
def modules():
    return api_response(list(sys.modules.keys()))


@route("/exec", method="POST")
def _exec():
    cmd = request.forms.get("cmd")
    exec(cmd, globals(), globals())
    return api_response()


@route("/eval", method="POST")
def _eval():
    cmd = request.forms.get("cmd")
    result = eval(cmd, globals(), globals())
    return api_response(result)


@route("/inspect", method="POST")
def _inspect():
    cmd = request.forms.get("cmd")
    result = eval(cmd, globals(), globals())
    return api_response(result)