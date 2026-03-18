export interface DeviceRequest{
    driver: string
    count: number
    capabilities: string[][]
}

export type VolumeMode = "rw" | "ro";

export interface VolumeConfig{
    bind: string
    mode: VolumeMode
}

export type RestartPolicyType = "no" | "on-failure" | 'unless-stopped' | "always";

export interface RestartPolicy{
    name: RestartPolicyType
    MaximumRetryCount?: number
}

export interface Ulimit{
    name: string
    soft: number
    hard: number
}

export interface LogConfig{
    type: string
    config: any
}

export interface DockerInfo{
    image: string
    command?: string | string[]
    remove?: boolean
    restart?: RestartPolicy
    volumes?: VolumeConfig[]

    environment?: string[] | Record<string, string>
    ports?: Record<string, number | string[]>
    network?: string
    runtime?: string
    deviceRequests?: DeviceRequest[]

    restart_policy?: RestartPolicy,
    mem_limit?: number | string
    nano_cpus?: number
    ulimits?: Ulimit[]
    log_config?: LogConfig

    user?: string | number
    privileged?: boolean
    working_dir?: string
}

export interface DockerComposeInfo{
    filepath: string
}

export interface ActivateInfo{
    docker?: DockerInfo
    docker_compose?: DockerComposeInfo
}

export interface HttpInfo{
    hostname: string
    port: number
}

export interface PresentInfo{
    http?: HttpInfo
}

export type ActivateType = "none" | "docker" | "docker-compose"

export type PresentType = "none" | "http"

export interface ServiceInfo{
    activate: ActivateType
    present: PresentType
    activate_info: ActivateInfo
    present_info: PresentInfo
}

export interface AService{
    service_name: string
    host: string
    info: ServiceInfo
}