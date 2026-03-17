// -------------------------------------------------------------------
// Core DockerRunArgs structure (mirrors the TypedDict you posted)
// -------------------------------------------------------------------
export type DeviceRequest = {
    driver: string;
    count: number;
    capabilities: string[];
};

export type VolumeConfig = {
    bind: string;                // host path
    mode: 'rw' | 'ro';
};

export type RestartPolicy = {
    Name: 'no' | 'on-failure' | 'always' | 'unless-stopped';
    MaximumRetryCount?: number; // only used when Name === 'on-failure'
};

export type Ulimit = {
    name: string;
    soft: number;
    hard: number;
};

export type LogConfig = {
    type: 'json-file' | 'syslog' | string;
    config?: Record<string, string>;
};

export type DockerRunArgs = {
    // ------------
    // DO NOT EDIT THESE (but they are still displayed for completeness)
    // ------------
    image: string;                 // user must fill it
    command: string | string[];    // user must fill it
    name: string;                  // auto‑generated; user must fill it
    detach: boolean;               // auto‑generated; fixed to true
    remove: boolean;               // auto‑generated; user can toggle

    // ------------ CORE SETTINGS ------------
    volumes: Record<string, VolumeConfig>; // hostPath => { bind, mode }
    environment: Record<string, string> | string[]; // key/value or simple array
    ports: Record<string, number | [number, number] | (number | string)[]>; // host:container
    network: string;
    runtime: string;
    device_requests: DeviceRequest[];
    restart_policy: RestartPolicy;
    mem_limit: string | number;
    nano_cpus: number;
    ulimits: Ulimit[];
    log_config: LogConfig;
    user: string | number;
    privileged: boolean;
    working_dir: string;

    // ------------ HIDDEN FROM USER (but still in type) ------------
    // These are *not* editable in our UI – they are filled automatically.
    // They are kept for TypeScript completeness.
    // (you can ignore them)
};