<script setup lang="ts">
// 定義雙向綁定的 model，類型為字串陣列
const model = defineModel<string[]>({ default: () => [] });
interface Props{
    title: string;
}
defineProps<Props>();

// 新增項目的方法
const addItem = () => {
    model.value.push('');
};

// 刪除項目的方法
const removeItem = (index: number) => {
    model.value.splice(index, 1);
};
</script>

<template>
    <div class="w-full max-w-md p-4 bg-white rounded-xl shadow-sm border border-slate-200">
        <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-slate-800">{{ title }}</h3>
            <button
                @click="addItem"
                class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-1"
            >
                <span class="text-lg">+</span> 新增
            </button>
        </div>

        <TransitionGroup
            tag="ul"
            name="list"
            class="space-y-3"
        >
            <li
                v-for="(_, index) in model"
                :key="index"
                class="flex items-center gap-2 group"
            >
                <div class="grow">
                    <input
                        v-model="model[index]"
                        type="text"
                        placeholder="請輸入內容..."
                        class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                    />
                </div>

                <button
                    @click="removeItem(index)"
                    class="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    title="刪除"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            </li>
        </TransitionGroup>

        <div v-if="model.length === 0" class="py-8 text-center text-slate-400 italic border-2 border-dashed border-slate-100 rounded-lg">
            目前沒有任何項目
        </div>
    </div>
</template>

<style scoped>
/* 簡單的列表過渡動畫 */
.list-enter-active,
.list-leave-active {
    transition: all 0.3s ease;
}
.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateX(20px);
}
</style>