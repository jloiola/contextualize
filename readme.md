
# get conda

```
MINICONDA_VERSION=4.5.4
curl -o miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-$MINICONDA_VERSION-MacOSX-x86_64.sh
bash ~/miniconda.sh -b
export PATH="$HOME/miniconda/bin:$PATH"
```

NOTE: You'll need to add the export PATH to your .profile (zsh|bash) for future sessions

Create the conda env
conda env create -f environment.yml
conda activate contextualize

python -m spacy download en_core_web_sm

Prod
gunicorn --workers 4 --worker-class=meinheld.gmeinheld.MeinheldWorker server:__hug_wsgi__

Dev
gunicorn --reload --workers 2 --worker-class=meinheld.gmeinheld.MeinheldWorker server:__hug_wsgi__
