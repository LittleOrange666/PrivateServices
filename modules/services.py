from typing import TypedDict, Literal, NotRequired, Union

import docker
from loguru import logger
from python_on_whales import DockerClient

from .data import SessionLocal, ServicesDB

ActivateType = Literal["none", "docker-compose", "docker"]

PresentType = Literal["none", "http"]


class DeviceRequest(TypedDict):
    driver: str
    count: int
    capabilities: list[list[str]]


class VolumeConfig(TypedDict):
    bind: str  # 容器內部的掛載路徑
    mode: Literal['rw', 'ro']  # 讀寫權限：只允許 'rw' 或 'ro'


# 定義重啟策略 (例如: {"Name": "on-failure", "MaximumRetryCount": 5})
class RestartPolicy(TypedDict):
    Name: Literal['no', 'on-failure', 'always', 'unless-stopped']
    MaximumRetryCount: NotRequired[int]  # 僅在 'on-failure' 時有效


# 定義 Ulimit 設定
class Ulimit(TypedDict):
    name: str
    soft: int
    hard: int


# 定義日誌配置
class LogConfig(TypedDict):
    type: str  # 如 'json-file', 'syslog'
    config: NotRequired[dict[str, str]]


class DockerRunArgs(TypedDict, total=False):
    # 基礎設定
    # image: str (user should not modify this)
    command: Union[str, list[str]]
    # name: str (user should not modify this)
    # detach: bool (user should not modify this)
    remove: bool  # 對應 SDK 的 auto_remove

    # 核心：儲存空間 (Key 是 Host 路徑)
    # 範例: {"/home/user/data": {"bind": "/app/data", "mode": "rw"}}
    volumes: dict[str, VolumeConfig]

    # 網路與環境
    environment: Union[dict[str, str], list[str]]
    ports: dict[str, Union[int, tuple, list]]
    network: str

    # 策略與限制
    restart_policy: RestartPolicy
    mem_limit: Union[int, str]
    nano_cpus: int
    ulimits: list[Ulimit]
    log_config: LogConfig

    # 權限
    user: Union[str, int]
    privileged: bool
    working_dir: str


class DockerComposeInfo(TypedDict):
    filepath: str


class DockerInfo(TypedDict):
    image_name: str
    config: DockerRunArgs


class ActivateInfo(TypedDict):
    docker_compose: NotRequired[DockerComposeInfo]
    docker: NotRequired[DockerInfo]


class HttpInfo(TypedDict):
    hostname: str
    port: int
    use_root: NotRequired[bool]


class PresentInfo(TypedDict):
    http: NotRequired[HttpInfo]


class ServiceInfo(TypedDict):
    activate: ActivateType
    present: PresentType
    activate_info: ActivateInfo
    present_info: PresentInfo


def get_default_service_info() -> ServiceInfo:
    return {
        "activate": "none",
        "present": "none",
        "activate_info": {},
        "present_info": {}
    }


async def update_nginx_conf():
    logger.info("正在更新nginx配置...")
    with open("/app/templates/nginx/default.conf") as f:
        lines = f.readlines()
    place_line = [i for i in range(len(lines)) if "SERVICE_CONFIG_PLACEHOLDER" in lines[i]]
    if len(place_line) == 0:
        logger.error("template error")
        return
    add_lines = []
    db = SessionLocal()
    try:
        services = db.query(ServicesDB).all()
        for service in services:
            if service.host:
                name = service.service_name
                host = service.host
                path = f"/{name}/"
                cur = [
                    f"location {path} {{",
                    "    auth_request /auth-check;",
                    # "    auth_request_set $user_id $upstream_http_x_user_id;",
                    # "    proxy_set_header X-User-ID $user_id;",
                    f"    proxy_pass http://{host}/;",
                    # f"    proxy_redirect / /{name}/;",
                    # f"    sub_filter 'href=\"/' 'href=\"/{name}/';",
                    # f"    sub_filter 'src=\"/' 'src=\"/{name}/';",
                    # "    sub_filter_once off;",
                    # "    sub_filter_types text/html text/css application/javascript;",
                    "    proxy_read_timeout 3600s;",
                    "    proxy_connect_timeout 3600s;",
                    "    proxy_send_timeout 3600s;",
                    "    proxy_buffering off;",
                    "    client_max_body_size 50M;",
                    "    proxy_request_buffering off;",
                    "    proxy_buffer_size 128k;",
                    "    proxy_buffers 4 256k;",
                    "    proxy_busy_buffers_size 256k;",
                    "    proxy_cache off;",
                    "    proxy_redirect off;",
                    "    proxy_http_version 1.1;",
                    "    proxy_set_header Connection 'upgrade';",
                    "    proxy_set_header Upgrade $http_upgrade;",
                    "    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
                    "    proxy_set_header X-Forwarded-Proto $proxy_x_forwarded_proto;",
                    "    proxy_set_header Host $host;",
                    "}"
                ]
                add_lines.extend(cur)
    finally:
        db.close()
    output_lines = lines[:place_line[0]] + ["    " + l + "\n" for l in add_lines] + lines[place_line[0] + 1:]
    with open("/app/nginx/default.conf", "w") as f:
        f.writelines(output_lines)


def restart_nginx():
    DockerClient().container.restart("private_services_nginx")


async def service_on(service: ServicesDB):
    info: ServiceInfo = service.info
    match info["activate"]:
        case "none":
            pass
        case "docker-compose":
            client = DockerClient(compose_files=[info["activate_info"]["docker_compose"]["filepath"]])
            client.compose.up(detach=True)
        case "docker":
            client = docker.from_env()
            name = service.service_name + "_container"
            client.containers.run(info["activate_info"]["docker"]["image_name"], detach=True, name=name,
                                  **info["activate_info"]["docker"]["config"])


async def service_off(service: ServicesDB):
    info: ServiceInfo = service.info
    match info["activate"]:
        case "none":
            client = DockerClient(compose_files=[info["activate_info"]["docker_compose"]["filepath"]])
            client.compose.down()
        case "docker":
            client = docker.from_env()
            name = service.service_name + "_container"
            client.containers.get(name).stop()