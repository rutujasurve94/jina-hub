FROM jinaai/jina:1.0.7

# setup the workspace
COPY . /workspace
WORKDIR /workspace

# install the third-party requirements
RUN pip install -r requirements.txt

# for testing the image
RUN pip install pytest pytest-mock mock && pytest

ENTRYPOINT ["jina", "pod", "--uses", "config.yml", "--timeout-ready", "120000"]
