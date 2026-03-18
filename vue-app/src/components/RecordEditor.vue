<template>
    <div class="p-4 border rounded-lg bg-white shadow-sm max-w-2xl">
        <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-gray-700">{{ title }}</h3>
            <button
                @click="addItem"
                type="button"
                class="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors flex items-center gap-1"
            >
                <span class="text-lg">+</span> 新增項目
            </button>
        </div>

        <div class="space-y-3">
            <div v-if="isEmpty" class="text-center py-8 text-gray-400 border-2 border-dashed rounded-lg">
                目前沒有資料，請點擊上方按鈕新增
            </div>

            <div
                v-for="(value, key) in model"
                :key="key"
                class="flex gap-2 items-start animate-in fade-in duration-200"
            >
                <div class="flex-1">
                    <label class="block text-xs text-gray-500 mb-1">Key</label>
                    <input
                        type="text"
                        :value="key"
                        @change="(e) => updateKey(key, (e.target as HTMLInputElement).value)"
                        placeholder="鍵名"
                        class="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none text-sm font-mono bg-gray-50"
                    />
                </div>

                <div class="flex-[1.5]">
                    <label class="block text-xs text-gray-500 mb-1">Value</label>
                    <input
                        type="text"
                        v-model="model[key]"
                        placeholder="數值"
                        class="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none text-sm"
                    />
                </div>

                <div class="self-end pb-1">
                    <button
                        @click="removeItem(key)"
                        class="p-2 text-red-500 hover:bg-red-50 rounded-md transition-colors"
                        title="刪除項目"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <div class="mt-6 pt-4 border-t">
            <p class="text-xs font-semibold text-gray-400 uppercase mb-2">Data Preview:</p>
            <pre class="bg-gray-800 text-green-400 p-3 rounded text-xs overflow-auto">{{ model }}</pre>
        </div>
    </div>
</template>

<script setup lang="ts">
import {computed, onMounted} from 'vue';

// 定義 Model，類型為 Record<string, string>
const model = defineModel<Record<string, string>>({
    default: () => ({})
});
interface Props{
    title: string;
}
defineProps<Props>();

// 新增項目的處理邏輯
const addItem = () => {
    // 產生一個不重複的預設 Key
    let newKey = 'new_key';
    let counter = 1;
    while (newKey in model.value) {
        newKey = `new_key_${counter++}`;
    }
    model.value[newKey] = '';
};

// 刪除項目
const removeItem = (key: string) => {
    const { [key]: _, ...rest } = model.value;
    model.value = rest;
};

// 修改 Key 名稱 (因為物件的 Key 是唯一的，修改 Key 需要特殊處理)
const updateKey = (oldKey: string, newKey: string) => {
    if (oldKey === newKey || !newKey.trim()) return;

    // 如果新 Key 已存在，這裡選擇不覆蓋（或視需求調整）
    if (newKey in model.value) {
        alert('Key 已存在');
        return;
    }

    const value = model.value[oldKey] as string;
    const { [oldKey]: _, ...rest } = model.value;

    // 重新建立物件以觸發反應性並維持順序（非必要，但對 UX 較好）
    model.value = { ...rest, [newKey]: value };
};

// 檢查是否為空
const isEmpty = computed(() => Object.keys(model.value).length === 0);
</script>

