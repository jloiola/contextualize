#!/usr/bin/env bash

if [ -x "$(command -v conda)" ]; then
  echo 'Activating conda env'
  source activate contextualize
fi

gunicorn --workers 4 --worker-class=meinheld.gmeinheld.MeinheldWorker server:__hug_wsgi__
