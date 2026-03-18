# Private Services

A Tool to manage and supply private services for your own.

## Requirements

+ git (optional, you can just download zip)
+ docker (required)
+ docker-compose (required)

## Install

clone this repo then run

```bash
./init.sh
docker compose up -d
```

## Config samples

```json
{
  "name": "pdf",
  "info": {
    "activate": "docker",
    "present": "http",
    "activate_info": {
      "docker": {
        "image": "awwaawwa/pdfmathtranslate-next",
        "ports": {
          "7860": 7860
        },
        "environment": {
          "GRADIO_ROOT_PATH": "/pdf"
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
        "image": "docker-stable-diffusion-webui-save7",
          "ports": {
            "8080": 7861
          },
          "environment": {
            "NVIDIA_VISIBLE_DEVICES": "all",
            "NVIDIA_DRIVER_CAPABILITIES": "compute,utility",
            "GRADIO_ROOT_PATH": "/sd",
            "CLIP_PACKAGE": "clip",
            "OPENCLIP_PACKAGE": "open-clip-torch",
            "STABLE_DIFFUSION_REPO": "https://github.com/w-e-w/stablediffusion.git",
            "TORCH_INDEX_URL": "https://download.pytorch.org/whl/cu130",
            "TORCH_COMMAND": "pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu130",
            "REQS_FILE": "requirements.txt"
          },
          "volumes": {
            "D:/ai/stable-diffusion-webui/docker-stable-diffusion-webui/inputs": {
              "bind": "/app/stable-diffusion-webui/inputs",
              "mode": "rw"
            },
            "D:/ai/stable-diffusion-webui/docker-stable-diffusion-webui/textual_inversion_templates": {
              "bind": "/app/stable-diffusion-webui/textual_inversion_templates",
              "mode": "rw"
            },
            "D:/ai/stable-diffusion-webui/docker-stable-diffusion-webui/embeddings": {
              "bind": "/app/stable-diffusion-webui/embeddings",
              "mode": "rw"
            },
            "D:/ai/stable-diffusion-webui/docker-stable-diffusion-webui/extensions": {
              "bind": "/app/stable-diffusion-webui/extensions",
              "mode": "rw"
            },
            "D:/ai/stable-diffusion-webui/docker-stable-diffusion-webui/models": {
              "bind": "/app/stable-diffusion-webui/models",
              "mode": "rw"
            },
            "D:/ai/stable-diffusion-webui/docker-stable-diffusion-webui/localizations": {
              "bind": "/app/stable-diffusion-webui/localizations",
              "mode": "rw"
            },
            "D:/ai/stable-diffusion-webui/docker-stable-diffusion-webui/outputs": {
              "bind": "/app/stable-diffusion-webui/outputs",
              "mode": "rw"
            }
          },
          "command": ["--update-check", "--listen", "--port", "8080", "--skip-torch-cuda-test", "--disable-nan-check", "--disable-safe-unpickle", "--no-half", "--no-half-vae", "--precision", "full", "--subpath", "/sd"],
          "runtime": "nvidia"
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
        "image": "littleorange666/vision_translate:1.0.0",
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