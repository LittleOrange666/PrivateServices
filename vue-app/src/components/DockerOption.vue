<template>
    <div class="max-w-4xl mx-auto space-y-8 p-8 bg-slate-50 min-h-screen">
        <div class="border-b border-slate-200 pb-4">
            <h2 class="text-2xl font-bold text-slate-800">Docker 容器配置</h2>
            <p class="text-sm text-slate-500 mt-1">設定映像檔執行參數與系統資源限制</p>
        </div>

            <div class="space-y-4 bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                <h3 class="font-semibold text-slate-700 flex items-center gap-2">
                    <span class="w-2 h-5 bg-blue-500 rounded-full"></span> 基礎資訊
                </h3>

                <div class="space-y-3">
                    <div>
                        <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Image 映像檔</label>
                        <input v-model="model.image" type="text" placeholder="e.g. nginx:latest"
                               class="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
                    </div>

                    <div>
                        <EditableList title="命令參數 (Args)" v-model="model.command as string[]"/>
                   </div>

                    <div class="flex gap-4">
                        <div class="flex-1">
                            <label class="block text-xs font-bold text-slate-500 uppercase mb-1">工作目錄</label>
                            <input v-model="model.working_dir" type="text" placeholder="/app"
                                   class="form-input-custom"/>
                        </div>
                        <div class="flex-1">
                            <label class="block text-xs font-bold text-slate-500 uppercase mb-1">使用者</label>
                            <input v-model="model.user" type="text" placeholder="root" class="form-input-custom"/>
                        </div>
                    </div>

                    <div class="flex items-center gap-6 pt-2">
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input v-model="model.privileged" type="checkbox" class="w-4 h-4 text-blue-600 rounded"/>
                            <span class="text-sm text-slate-600">特權模式</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input v-model="model.remove" type="checkbox" class="w-4 h-4 text-blue-600 rounded"/>
                            <span class="text-sm text-slate-600">自動刪除 (--rm)</span>
                        </label>
                    </div>
                </div>
            </div>

            <div class="space-y-4 bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                <h3 class="font-semibold text-slate-700 flex items-center gap-2">
                    <span class="w-2 h-5 bg-emerald-500 rounded-full"></span> 資源限制
                </h3>
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-500 uppercase mb-1">記憶體限制
                            (mem_limit)</label>
                        <input v-model="model.mem_limit" type="text" placeholder="512m / 2g" class="form-input-custom"/>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-500 uppercase mb-1">CPU 核心 (Nano
                            CPUs)</label>
                        <input v-model.number="model.nano_cpus" type="number" step="0.1" class="form-input-custom"/>
                    </div>
                    <div><label class="block text-xs font-bold text-slate-500 uppercase mb-1">重啟策略</label>
                        <select
                            :value="model.restart_policy?.name || 'no'"
                            @change="(e) => {
                              const val = (e.target as HTMLSelectElement).value as RestartPolicyType;
                              model.restart_policy = { ...model.restart_policy, name: val };
                            }"
                            class="form-input-custom"
                        >
                            <option v-for="opt in restartOptions" :key="opt" :value="opt">{{ opt }}</option>
                        </select>
                    </div>
                </div>
            </div>

        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
            <div class="flex justify-between items-center mb-4">
                <h3 class="font-semibold text-slate-700">磁碟卷掛載 (Volumes)</h3>
                <button @click="addVolume"
                        class="px-3 py-1 bg-blue-50 text-blue-600 text-sm rounded-lg hover:bg-blue-100 transition">
                    + 新增掛載
                </button>
            </div>
            <div class="space-y-3">
                <div v-for="(vol, idx) in model.volumes" :key="idx"
                     class="flex gap-3 items-end bg-slate-50 p-3 rounded-lg border border-dashed border-slate-200">
                    <div class="flex-1">
                        <label class="text-[10px] font-bold text-slate-400 uppercase">路徑對應 (Bind)</label>
                        <input v-model="vol.bind" type="text" placeholder="/host:/container" class="form-input-sm"/>
                    </div>
                    <div class="w-24">
                        <label class="text-[10px] font-bold text-slate-400 uppercase">模式</label>
                        <select v-model="vol.mode" class="form-input-sm">
                            <option value="rw">RW</option>
                            <option value="ro">RO</option>
                        </select>
                    </div>
                    <button @click="removeVolume(idx)" class="p-2 text-red-400 hover:text-red-600">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path
                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <RecordEditor title="環境變數" v-model="model.environment as Record<string,string>" />
    </div>
</template>

<style scoped>
</style>

<script setup lang="ts">
import type {DockerInfo, RestartPolicyType} from '@/utils/types';
import RecordEditor from "@/components/RecordEditor.vue";
import EditableList from "@/components/EditableList.vue";

// 定義 Model
const model = defineModel<DockerInfo>({required: true});

// 輔助初始化邏輯 (確保數組存在)
const initArray = (key: keyof DockerInfo) => {
    if (!model.value[key]) (model.value as any)[key] = [];
};

// 操作方法
const addVolume = () => {
    initArray('volumes');
    model.value.volumes!.push({bind: '', mode: 'rw'});
};

const removeVolume = (index: number) => {
    model.value.volumes?.splice(index, 1);
};

const addDeviceRequest = () => {
    initArray('deviceRequests');
    model.value.deviceRequests!.push({driver: 'nvidia', count: 1, capabilities: [['gpu']]});
};

const restartOptions: RestartPolicyType[] = ['no', 'on-failure', 'unless-stopped', 'always'];
</script>

