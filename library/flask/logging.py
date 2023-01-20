import logging
from flask import Response
from bson.json_util import dumps


class FlaskLogging:
  @staticmethod
  def get():
    logging.debug('FlaskLogging.get - request hit')
    return Response(dumps({
      'status': 'OK'
    }), mimetype='text/json'), 200