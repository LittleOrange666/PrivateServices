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
```json
{
  "name": "sd",
  "info": {
    "activate": "docker",
    "present": "http",
    "activate_info": {
      "docker": {
        "image_name": "docker-stable-diffusion-webui",
        "config": {
          "ports": {
            "7861": 7861
          },
          "environment": {
            "GRADIO_ROOT_PATH": "/sd"
          },
          "device_requests": [
            {
              "count": -1,
              "capabilities": [["gpu"]]
            }
          ],
          "volumes": {
            "/mnt/d/ai/stable-diffusion-webui/inputs": {
              "bind": "/app/stable-diffusion-webui/inputs",
              "mode": "rw"
            },
            "/mnt/d/ai/stable-diffusion-webui/textual_inversion_templates": {
              "bind": "/app/stable-diffusion-webui/textual_inversion_templates",
              "mode": "rw"
            },
            "/mnt/d/ai/stable-diffusion-webui/embeddings": {
              "bind": "/app/stable-diffusion-webui/embeddings",
              "mode": "rw"
            },
            "/mnt/d/ai/stable-diffusion-webui/extensions": {
              "bind": "/app/stable-diffusion-webui/extensions",
              "mode": "rw"
            },
            "/mnt/d/ai/stable-diffusion-webui/models": {
              "bind": "/app/stable-diffusion-webui/models",
              "mode": "rw"
            },
            "/mnt/d/ai/stable-diffusion-webui/localizations": {
              "bind": "/app/stable-diffusion-webui/localizations",
              "mode": "rw"
            },
            "/mnt/d/ai/stable-diffusion-webui/outputs": {
              "bind": "/app/stable-diffusion-webui/outputs",
              "mode": "rw"
            }
          },
          "command": ["--skip-torch-cuda-test", "--no-half", "--no-half-vae", "--precision", "full"]
        }
      }
    },
    "present_info": {
      "http": {
        "hostname": "host.docker.internal",
        "port": 7861
      }
    }
  }
}
```
```json
{
  "name": "vt",
  "info": {
    "activate": "docker",
    "present": "http",
    "activate_info": {
      "docker": {
        "image_name": "littleorange666/vision_translate:1.0.0",
        "config": {
          "ports": {
            "7862": 7862
          },
          "environment": {
            "GRADIO_ROOT_PATH": "/vt",
            "OLLAMA_HOST": "http://host.docker.internal:11434",
            "MODEL_NAME": "translategemma:12b",
            "SERVER_PORT": "7862"
          }
        }
      }
    },
    "present_info": {
      "http": {
        "hostname": "host.docker.internal",
        "port": 7862
      }
    }
  }
}
```
```json
{
  "name": "ai",
  "info": {
    "activate": "docker",
    "present": "http",
    "activate_info": {
      "docker": {
        "image_name": "ghcr.io/open-webui/open-webui:main",
        "config": {
          "ports": {
            "8080": 7960
          },
          "volumes": {
            "open-webui": {
              "bind": "/app/backend/data",
              "mode": "rw"
            }
          }
        }
      }
    },
    "present_info": {
      "http": {
        "hostname": "host.docker.internal",
        "port": 7960,
        "use_root": true
      }
    }
  }
}
```