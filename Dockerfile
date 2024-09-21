FROM python:3.11-slim
WORKDIR /visa_forum_backend
COPY ./requirements.txt /my_blog
RUN pip install -r requirements.txt
COPY . .
RUN python3 manage.py collectstatic --noinput

# Start Server
EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "core.wsgi:application"]