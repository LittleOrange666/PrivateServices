<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
        <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
            <div class="text-center mb-10">
                <h1 class="text-3xl font-bold text-gray-800">登入</h1>
                <p class="text-gray-500 mt-2">請輸入您的帳號密碼以登入</p>
            </div>

            <form @submit.prevent="handleLogin" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700">帳號</label>
                    <input
                        v-model="username"
                        type="text"
                        required
                        class="mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                        placeholder="請輸入帳號"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700">密碼</label>
                    <input
                        v-model="password"
                        type="password"
                        required
                        class="mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                        placeholder="請輸入密碼"
                    />
                </div>

                <div v-if="errorMessage" class="text-red-500 text-sm bg-red-50 p-2 rounded">
                    {{ errorMessage }}
                </div>

                <button
                    type="submit"
                    :disabled="loading"
                    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg shadow-md transition duration-300 flex justify-center items-center"
                >
                    <span v-if="loading" class="animate-spin mr-2">🌀</span>
                    {{ loading ? '登入中...' : '立即登入' }}
                </button>
            </form>

            <div class="mt-6 text-center text-sm text-gray-400">
                &copy; 2026 Private Services
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import axios from "axios"
import {show_modal} from "@/utils/modal.ts";
import {useRouter} from "vue-router";

const username = ref('');
const password = ref('');
const loading = ref(false);
const errorMessage = ref('');
const router = useRouter();

async function handleLogin() {
    const params = new URLSearchParams();
    params.append('username', username.value);
    params.append('password', password.value);
    const res = await axios.post("/api/login", params);
    if (res.status === 200) {
        // 登入成功，導向首頁
        //await show_modal("成功", "登入成功");
        await router.push("/");
    } else {
        errorMessage.value = res.data.detail;
        //await show_modal("失敗", res.data.detail);
    }
}
</script>

