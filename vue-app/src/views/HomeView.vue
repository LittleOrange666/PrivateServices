<template>
    <div class="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto"><h1 class="text-xl font-extrabold text-slate-900 mb-8 text-center tracking-tight">
            首頁
        </h1>
            <div class="space-y-4">
                <div v-for="name in names" :key="name"
                     class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden transition-all duration-300"
                     :class="{'ring-2 ring-indigo-100 shadow-lg': editingName === name}">
                    <div class="flex items-center justify-between px-6 py-4">
                        <div class="flex items-center gap-3">
                            <Status :status="displayStatus(name)" :title="statusText(name)" />
                            <span class="text-slate-700 font-semibold text-lg font-mono">
                {{ name }}
              </span>
                            <span v-if="statusText(name)" class="text-xs font-semibold"
                                  :class="displayStatus(name) === 'error' ? 'text-rose-600' : 'text-amber-600'">
                {{ statusText(name) }}
              </span>
                        </div>

                        <div class="flex items-center gap-2">
                            <a :href="`/${name}/`"
                               class="px-3 py-1.5 bg-indigo-50 text-indigo-700 text-sm font-bold rounded-lg hover:bg-indigo-100 transition-colors">
                                前往
                            </a>

                            <button @click="toggleEdit(name)" v-if="auth.role=='admin'"
                                    class="px-3 py-1.5 text-sm font-bold rounded-lg transition-colors flex items-center gap-1"
                                    :class="editingName === name ? 'bg-slate-200 text-slate-800' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                                {{ editingName === name ? '取消' : '編輯' }}
                            </button>

                            <button @click="handleStart(name)"
                                    class="px-3 py-1.5 bg-emerald-50 text-emerald-700 text-sm font-bold rounded-lg hover:bg-emerald-100 transition-colors">
                                啟動
                            </button>

                            <button @click="handleStop(name)"
                                    class="px-3 py-1.5 bg-rose-50 text-rose-700 text-sm font-bold rounded-lg hover:bg-rose-100 transition-colors">
                                停止
                            </button>

                            <button @click="handleRemove(name)"
                                    class="px-3 py-1.5 bg-rose-50 text-rose-700 text-sm font-bold rounded-lg hover:bg-rose-100 transition-colors">
                                刪除容器
                            </button>
                        </div>
                    </div>

                    <transition
                            enter-active-class="transition-[max-height] duration-300 ease-out"
                            enter-from-class="max-height-0"
                            enter-to-class="max-height-96"
                            leave-active-class="transition-[max-height] duration-200 ease-in"
                            leave-from-class="max-height-96"
                            leave-to-class="max-height-0"
                    >
                        <div v-if="editingName === name"
                             class="overflow-hidden border-t border-slate-100 bg-slate-50/50">
                            <div class="px-6 py-5">
                                <EditComponent :name="name" v-model="service_table[name] as ServiceInfo"
                                               @close="editingName = null"/>
                            </div>
                        </div>
                    </transition>

                </div>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">

import {onMounted, onUnmounted, ref} from "vue";
import axios from "axios";
import {show_modal} from "@/utils/modal.ts";
import {useAuthStore} from "@/stores/auth.ts";
import {useRouter} from "vue-router";
import type {AService, ServiceInfo} from "@/utils/types.ts";
import EditComponent from "@/components/EditComponent.vue";
import Status, {type StatusType} from "@/components/Status.vue";

const names = ref<string[]>([]);
const auth = useAuthStore();
const router = useRouter();

const services = ref<AService[]>([]);
const service_table = ref<Record<string, ServiceInfo>>({});
const service_status = ref<Record<string, string>>({});
// 網頁是否真的能開：undefined = 尚未檢查/檢查中
const web_ok = ref<Record<string, boolean | undefined>>({});
// 網頁檢查時拿到的 HTTP 狀態碼 (0 = 連線失敗/逾時)
const web_code = ref<Record<string, number>>({});
// 按下啟動後，等待網頁可用中的服務
const starting = ref<Record<string, boolean>>({});
// 每個服務的輪詢世代，用來取消舊的等待迴圈
const poll_gen: Record<string, number> = {};
let unmounted = false;

const WEB_CHECK_TIMEOUT = 8000;
const START_POLL_INTERVAL = 2000;
const START_POLL_LIMIT = 10 * 60 * 1000;

function isWebService(name: string) {
    return service_table.value[name]?.present === "http";
}

function displayStatus(name: string): StatusType {
    if (starting.value[name]) return "idle";
    if (service_status.value[name] !== "running") return "stopped";
    if (!isWebService(name)) return "running";
    const ok = web_ok.value[name];
    if (ok === undefined) return "idle";
    return ok ? "running" : "error";
}

function statusText(name: string): string {
    const st = displayStatus(name);
    if (st === "idle") return starting.value[name] ? "啟動中…" : "檢查中…";
    if (st === "error") {
        const code = web_code.value[name];
        return code ? `網頁無法開啟 (Error ${code})` : "網頁無法連線";
    }
    return "";
}

const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));

// 透過 nginx 實際請求 /{name}/，確認網頁能否打開
async function checkWeb(name: string): Promise<boolean> {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), WEB_CHECK_TIMEOUT);
    let ok = false, code = 0;
    try {
        const res = await fetch(`/${name}/`, {
            redirect: "manual",
            cache: "no-store",
            credentials: "same-origin",
            signal: ctrl.signal,
        });
        // 被導向（例如登入頁、應用本身的 redirect）也代表上游有回應
        ok = res.type === "opaqueredirect" || res.status < 500;
        code = res.status;
    } catch {
        ok = false;
        code = 0;
    } finally {
        clearTimeout(timer);
        ctrl.abort(); // 只需要狀態碼，不下載內容
    }
    web_ok.value[name] = ok;
    web_code.value[name] = code;
    return ok;
}

async function checkAllWeb() {
    await Promise.all(names.value
        .filter(name => service_status.value[name] === "running" && isWebService(name))
        .map(name => checkWeb(name)));
}

// 按下啟動後：保持黃色，直到網頁真的能打開
async function waitUntilReady(name: string) {
    const gen = (poll_gen[name] ?? 0) + 1;
    poll_gen[name] = gen;
    starting.value[name] = true;
    const deadline = Date.now() + START_POLL_LIMIT;
    try {
        while (!unmounted && poll_gen[name] === gen && Date.now() < deadline) {
            await loadStatus();
            if (poll_gen[name] !== gen) return;
            const st = service_status.value[name];
            if (st !== "running" && st !== "created" && st !== "restarting") break; // 容器掛了
            if (st === "running") {
                if (!isWebService(name)) break;
                if (await checkWeb(name)) break;
            }
            await sleep(START_POLL_INTERVAL);
        }
        if (poll_gen[name] === gen && service_status.value[name] === "running" && isWebService(name)) {
            await checkWeb(name);
        }
    } finally {
        if (poll_gen[name] === gen) starting.value[name] = false;
    }
}

function cancelWait(name: string) {
    poll_gen[name] = (poll_gen[name] ?? 0) + 1;
    starting.value[name] = false;
}

// 關鍵狀態：記錄目前哪一個項目正在被編輯 (null 表示沒有項目在編輯)
const editingName = ref<string | null>(null)

// 切換編輯狀態的函數
const toggleEdit = (name: string) => {
    if (editingName.value === name) {
        // 如果點擊的是同一個，則關閉
        editingName.value = null
    } else {
        // 否則，打開點擊的這一個 (這也會自動關閉原本打開的另一個)
        editingName.value = name
    }
}

function fix_info(obj: ServiceInfo) {
    if (!obj.activate_info.docker) {
        obj.activate_info.docker = {
            "image": "Ubuntu"
        }
    }
    if (!obj.present_info.http) {
        obj.present_info.http = {
            "hostname": "host.docker.internal",
            "port": 8080
        }
    }
    if (!obj.activate_info.docker_compose) {
        obj.activate_info.docker_compose = {
            "filepath": "docker-compose.yml"
        }
    }
}
async function loadStatus(){
    const res0 = await axios.get("/api/services/status");
    const table0: Record<string, string> = {};
    for (let service of res0.data.services) {
        table0[service.service_name] = service.status;
    }
    service_status.value = table0;
}

async function loadData() {
    await auth.load();
    if (auth.role == "unauthorized") {
        await router.push("/login");
        return;
    }
    const res = await axios.get("/api/services");
    services.value = res.data.services;
    const out = [];
    const table: Record<string, ServiceInfo> = {};
    for (let service of services.value) {
        out.push(service.service_name);
        fix_info(service.info);
        table[service.service_name] = service.info;
    }
    names.value = out;
    service_table.value = table
    await loadStatus();
    await checkAllWeb();
}

onMounted(async () => {
    await loadData();
});

onUnmounted(() => {
    unmounted = true;
});

async function handleStart(name: string) {
    cancelWait(name);
    starting.value[name] = true;
    try {
        const res = await axios.post("/api/services/on", {name: name});
        if (res.status === 200) {
            show_modal("成功", res.data.message);
            await waitUntilReady(name);
        } else {
            starting.value[name] = false;
            await show_modal("失敗", "Error " + res.status);
        }
    } catch (e) {
        starting.value[name] = false;
        await show_modal("失敗", (e as Error).message);
    }
}

async function handleStop(name: string) {
    try {
        cancelWait(name);
        const res = await axios.post("/api/services/off", {name: name});
        if (res.status === 200) {
            await show_modal("成功", res.data.message);
            await loadStatus();
            web_ok.value[name] = undefined;
        } else {
            await show_modal("失敗", "Error " + res.status);
        }
    } catch (e) {
        await show_modal("失敗", (e as Error).message);
    }
}

async function handleRemove(name: string) {
    try {
        cancelWait(name);
        const res = await axios.post("/api/services/remove", {name: name});
        if (res.status === 200) {
            await show_modal("成功", res.data.message);
            await loadStatus();
            web_ok.value[name] = undefined;
        } else {
            await show_modal("失敗", "Error " + res.status);
        }
    } catch (e) {
        await show_modal("失敗", (e as Error).message);
    }
}

</script>

