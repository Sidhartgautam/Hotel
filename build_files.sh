mkdir -p staticfiles_build
export STATIC_ROOT=staticfiles_build
pip3 install -r requirements.txt
python3 manage.py collectstatic --noinput