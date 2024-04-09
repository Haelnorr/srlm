from flask import request


def force_refresh(*args, **kwargs):
    cached = request.args.get('cached', None)

    override = False

    if cached == 'false' or cached == 'False' or cached == 'No' or cached == 'no':
        override = True

    return override
