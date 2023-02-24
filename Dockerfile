FROM fnndsc/python-poetry

WORKDIR /usr/src/app
COPY . /usr/src/app/

RUN poetry install

EXPOSE 8050

ENTRYPOINT ["python", "frontend/app.py"]
