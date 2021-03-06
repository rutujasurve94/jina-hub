# ArrayBytesReader

**ArrayBytesReader** is a numeric crafter that converts a byte stream into a numpy array and saves it to the Document. 

The **ArrayBytesReader** executor needs the following parameters:

## Snippets:

Initialise ArrayBytesReader:

| `param_name`                  | `param_remarks`                    |
| ----------------------------- | ---------------------------------- |
| `as_type`                     | The numpy array will be this type  |

**NOTE**: 

- `MODULE_VERSION` is the version of the ArrayBytesReader, in semver format. E.g. `0.0.8`.
- `JINA_VERSION` is the version of the Jina core version with which the Docker image was built. E.g. `1.0.8` 

- Flow API

  ```python
    from jina.flow import Flow
    f = (Flow()
        .add(name='my-crafter', uses='docker://jinahub/pod.crafter.arraybytesreader:MODULE_VERSION-JINA_VERSION')
    ```
- Flow YAML file
  This is the only way to provide arguments to its parameters:
  
  ```yaml
  pods:
    - name: ngt
      uses: crafters/numeric/ArrayBytesReader/config.yml
  ```
  
  and then in `byte-reader.yml`:
  ```yaml
  !ArrayBytesReader
  metas:
    - py_modules:
        - __init__.py
  ```
- Jina CLI
  
  ```bash
  jina pod --uses docker://jinahub/pod.crafter.arraybytesreader:MODULE_VERSION-JINA_VERSION
  ```
- Conventional local usage with `uses` argument
  
  ```bash
  jina pod --uses crafters/numeric/ArrayBytesReader/config.yml --port-in 55555 --port-out 55556
  ```
- Run with Docker (`docker run`)
 
  Specify the image name along with the version tag. The snippet below uses Jina version as `JINA_VERSION`.
  ```bash
    docker run --network host docker://jinahub/pod.crafter.arraybytesreader:MODULE_VERSION-JINA_VERSION --port-in 55555 --port-out 55556
    ```