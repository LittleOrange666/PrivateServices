# Private Services

## Config samples

```json
{
  "name": "pdf",
  "info": {
    "activate": "docker",
    "present": "http",
    "activate_info": {
      "docker": {
        "image_name": "awwaawwa/pdfmathtranslate-next",
        "config": {
          "ports": {
            "7860": 7860
          },
          "environment": {
            "GRADIO_ROOT_PATH": "/pdf"
          }
        }
      }
    },
    "present_info": {
      "http": {
        "hostname": "host.docker.internal",
        "port": 7860
      }
    }
  }
}
```