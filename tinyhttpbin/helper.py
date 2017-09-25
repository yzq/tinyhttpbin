from flask import request

from structures import CaseInsensitiveDict

ROBOT_TXT = """User-agent: *
Disallow: /deny
"""

ANGRY_ASCII = """
          .-''''''-.
        .' _      _ '.
       /   O      O   \\
      :                :
      |                |
      :       __       :
       \  .-"`  `"-.  /
        '.          .'
          '-......-'
     YOU SHOULDN'T BE HERE
"""

ENV_HEADERS = (
    'X-Varnish',
    'X-Request-Start',
    'X-Heroku-Queue-Depth',
    'X-Real-Ip',
    'X-Forwarded-Proto',
    'X-Forwarded-Protocol',
    'X-Forwarded-Ssl',
    'X-Heroku-Queue-Wait-Time',
    'X-Forwarded-For',
    'X-Heroku-Dynos-In-Use',
    'X-Forwarded-For',
    'X-Forwarded-Protocol',
    'X-Forwarded-Port',
    'X-Request-Id',
    'Via',
    'Total-Route-Time',
    'Connect-Time'
)


def multidict_to_dict(md):
    if md:
        dict = md.to_dict(flat=False)
        for k, v in dict.items():
            if len(v) == 1:
                dict[k] = v[0]
        return dict
    else:
        return md


def get_headers(hide_env=True):
    """Returns headers dict from request context."""

    headers = dict(request.headers.items())

    if hide_env and ('show_env' not in request.args):
        for key in ENV_HEADERS:
            try:
                del headers[key]
            except KeyError:
                pass

    return CaseInsensitiveDict(headers.items())
