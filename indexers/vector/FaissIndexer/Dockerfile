FROM jinaai/jina:1.1.0

COPY . /workspace
WORKDIR /workspace

RUN pip install -r requirements.txt
RUN pip install pytest && pytest tests/ -v -s

ENTRYPOINT ["jina", "pod", "--uses", "config.yml"]