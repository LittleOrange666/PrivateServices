<template>
    <div class="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4 border border-slate-100">
        <div class="grid grid-cols-3 gap-4">
            <div class="col-span-2">
                <label class="block text-sm font-medium text-slate-600 mb-1">主機名稱 (Hostname)</label>
                <input
                        v-model="model.hostname"
                        type="text"
                        placeholder="localhost"
                        class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200"
                />
            </div>

            <div class="col-span-1">
                <label class="block text-sm font-medium text-slate-600 mb-1">連接埠</label>
                <input
                        :value="model.port"
                        @input="updatePort"
                        type="number"
                        placeholder="8080"
                        class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200"
                />
            </div>
        </div>

        <div class="mt-2 text-xs text-slate-400 italic">
            目前連線至: <span class="text-blue-500 font-mono">{{ model.hostname }}:{{ model.port }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import type {HttpInfo} from "@/utils/types.ts";

const model = defineModel<HttpInfo>({required: true});

const updatePort = (e: Event) => {
    const val = (e.target as HTMLInputElement).value;
    model.value.port = parseInt(val) || 0;
};
</script>