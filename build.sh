set -o errexit

pip install -r requirements.txt

# collect staticfiles
python manage.py collectstatic --no-input

# to make migrations and migrate
python manage.py makemigrations
python manage.py migrate
