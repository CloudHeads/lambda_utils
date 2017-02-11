HTTP_STATUS_CODES = {
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi Status',
    226: 'IM Used',  # see RFC 3229
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',  # unused
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: 'I\'m a teapot',  # see RFC 2324
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    426: 'Upgrade Required',
    428: 'Precondition Required',  # see RFC 6585
    429: 'Too Many Requests',
    431: 'Request Header Fields Too Large',
    449: 'Retry With',  # proprietary MS extension
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    507: 'Insufficient Storage',
    510: 'Not Extended'
}


class HTTPException(Exception):
    """
    Baseclass for all HTTP exceptions.
    """

    code = None

    def __init__(self, body=None, headers=None):
        Exception.__init__(self)
        self.body = body or self.name
        self.headers = headers

    @property
    def name(self):
        """The status name."""
        return HTTP_STATUS_CODES.get(self.code, 'Unknown Error')

    def __str__(self):
        return '%d: %s' % (self.code, self.name)

    def __repr__(self):
        return '<%s \'%s\'>' % (self.__class__.__name__, self)


class BadRequest(HTTPException):
    """*400* `Bad Request`

    Raise if the browser sends something to the application the application
    or server cannot handle.
    """
    code = 400


class Unauthorized(HTTPException):
    """*401* `Unauthorized`

    Raise if the user is not authorized.  Also used if you want to use HTTP
    basic auth.
    """
    code = 401


class Forbidden(HTTPException):
    """*403* `Forbidden`

    Raise if the user doesn't have the permission for the requested resource
    but was authenticated.
    """
    code = 403


class NotFound(HTTPException):
    """*404* `Not Found`

    Raise if a resource does not exist and never existed.
    """
    code = 404


class MethodNotAllowed(HTTPException):
    """*405* `Method Not Allowed`

    Raise if the server used a method the resource does not handle.  For
    example `POST` if the resource is view only.  Especially useful for REST.

    The first argument for this exception should be a list of allowed methods.
    Strictly speaking the response would be invalid if you don't provide valid
    methods in the header which you can do with that list.
    """
    code = 405


class NotAcceptable(HTTPException):
    """*406* `Not Acceptable`

    Raise if the server can't return any content conforming to the
    `Accept` headers of the client.
    """
    code = 406


class RequestTimeout(HTTPException):
    """*408* `Request Timeout`

    Raise to signalize a timeout.
    """
    code = 408


class Conflict(HTTPException):
    """*409* `Conflict`

    Raise to signal that a request cannot be completed because it conflicts
    with the current state on the server.

    """
    code = 409


class Gone(HTTPException):
    """*410* `Gone`

    Raise if a resource existed previously and went away without new location.
    """
    code = 410


class LengthRequired(HTTPException):
    """*411* `Length Required`

    Raise if the browser submitted data but no ``Content-Length`` header which
    is required for the kind of processing the server does.
    """
    code = 411


class PreconditionFailed(HTTPException):
    """*412* `Precondition Failed`

    Status code used in combination with ``If-Match``, ``If-None-Match``, or
    ``If-Unmodified-Since``.
    """
    code = 412


class RequestEntityTooLarge(HTTPException):
    """*413* `Request Entity Too Large`

    The status code one should return if the data submitted exceeded a given
    limit.
    """
    code = 413


class RequestURITooLarge(HTTPException):
    """*414* `Request URI Too Large`

    Like *413* but for too long URLs.
    """
    code = 414


class UnsupportedMediaType(HTTPException):
    """*415* `Unsupported Media Type`

    The status code returned if the server is unable to handle the media type
    the client transmitted.
    """
    code = 415


class RequestedRangeNotSatisfiable(HTTPException):
    """*416* `Requested Range Not Satisfiable`

    The client asked for a part of the file that lies beyond the end
    of the file.

    """
    code = 416


class ExpectationFailed(HTTPException):
    """*417* `Expectation Failed`

    The server cannot meet the requirements of the Expect request-header.

    """
    code = 417


class ImATeapot(HTTPException):
    """*418* `I'm a teapot`

    The server should return this if it is a teapot and someone attempted
    to brew coffee with it.

    """
    code = 418


class UnprocessableEntity(HTTPException):
    """*422* `Unprocessable Entity`

    Used if the request is well formed, but the instructions are otherwise
    incorrect.
    """
    code = 422


class PreconditionRequired(HTTPException):
    """*428* `Precondition Required`

    The server requires this request to be conditional, typically to prevent
    the lost update problem, which is a race condition between two or more
    clients attempting to update a resource through PUT or DELETE. By requiring
    each client to include a conditional header ("If-Match" or "If-Unmodified-
    Since") with the proper value retained from a recent GET request, the
    server ensures that each client has at least seen the previous revision of
    the resource.
    """
    code = 428


class TooManyRequests(HTTPException):
    """*429* `Too Many Requests`

    The server is limiting the rate at which this user receives responses, and
    this request exceeds that rate. (The server may use any convenient method
    to identify users and their request rates). The server may include a
    "Retry-After" header to indicate how long the user should wait before
    retrying.
    """
    code = 429


class RequestHeaderFieldsTooLarge(HTTPException):
    """*431* `Request Header Fields Too Large`

    The server refuses to process the request because the header fields are too
    large. One or more individual fields may be too large, or the set of all
    headers is too large.
    """
    code = 431


class InternalServerError(HTTPException):
    """*500* `Internal Server Error`

    Raise if an internal server error occurred.  This is a good fallback if an
    unknown error occurred in the dispatcher.
    """
    code = 500


class NotImplemented(HTTPException):
    """*501* `Not Implemented`

    Raise if the application does not support the action requested by the
    browser.
    """
    code = 501


class BadGateway(HTTPException):
    """*502* `Bad Gateway`

    If you do proxying in your application you should return this status code
    if you received an invalid response from the upstream server it accessed
    in attempting to fulfill the request.
    """
    code = 502


class ServiceUnavailable(HTTPException):
    """*503* `Service Unavailable`

    Status code you should return if a service is temporarily unavailable.
    """
    code = 503


class GatewayTimeout(HTTPException):
    """*504* `Gateway Timeout`

    Status code you should return if a connection to an upstream server
    times out.
    """
    code = 504


class HTTPVersionNotSupported(HTTPException):
    """*505* `HTTP Version Not Supported`

    The server does not support the HTTP protocol version used in the request.
    """
    code = 505
