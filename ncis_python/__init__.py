from ncis import route, api_response, request, ncis_weakrefs
import sys
import platform
import inspect

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


@route("/inspect/<refid>", method="GET")
def _inspect(refid):
    refid = int(refid)
    try:
        obj = ncis_weakrefs.get(refid)
        if obj is None:
            return api_response(None)
        obj = obj()
        if obj is None:
            ncis_weakrefs.pop(refid, None)
            return api_response(None)
        result = inspect.getmembers(obj)
        return api_response(result)
    except Exception as e:
        import traceback; traceback.print_exc()
        ncis_weakrefs.pop(refid, None)
        return api_response(None)
