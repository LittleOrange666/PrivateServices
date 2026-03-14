from typing import TypedDict, Literal, NotRequired

from .data import SessionLocal, ServicesDB

ActivateType = Literal["none", "docker-compose"]

PresentType = Literal["none", "http"]


class DockerComposeInfo(TypedDict):
    filepath: str


class ActivateInfo(TypedDict):
    docker_compose: NotRequired[DockerComposeInfo]


class HttpInfo(TypedDict):
    hostname: str
    port: int


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
    with open("/app/templates/nginx/default.conf") as f:
        lines = f.readlines()
    place_line = [i for i in range(len(lines)) if "SERVICE_CONFIG_PLACEHOLDER" in lines[i]]
    if len(place_line) == 0:
        print("template error")
        return
    add_lines = []
    db = SessionLocal()
    try:
        services = db.query(ServicesDB).all()
        for service in services:
            if service.host:
                name = service.service_name
                host = services.host
                cur = [
                    f"location /{name}/ {{",
                    "    auth_request /auth-check;",
                    "    auth_request_set $user_id $upstream_http_x_user_id;",
                    "    proxy_set_header X-User-ID $user_id;",
                    f"    proxy_pass http://{host}/;",
                    "}"
                ]
                add_lines.extend(cur)
    finally:
        db.close()
    output_lines = lines[:place_line[0]] + ["    "+l+"\n" for l in add_lines] + lines[place_line[0]+1:]
    with open("/app/nginx/default.conf", "w") as f:
        f.writelines(output_lines)
