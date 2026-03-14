<template>
    <form @submit.prevent="handleLogin">
        <div class="mb-3 col-5 offset-2">
            <label for="user_id" class="form-label">User Id</label>
            <input type="text" class="form-control" id="user_id" v-model="username" placeholder="user id" required>
        </div>
        <div class="mb-3 col-5 offset-2">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" v-model="password" placeholder="Password"
                   required>
        </div>
        <div class="mb-3 col-5 offset-2">
            <button type="submit" class="btn btn-primary">登入</button>
        </div>
    </form>
</template>

<script setup lang="ts">
import {ref} from "vue";
import axios from "axios"
import {show_modal} from "@/utils/modal.ts";
import {useRouter} from "vue-router";

const username = ref('');
const password = ref('');
const router = useRouter();

async function handleLogin() {
    const params = new URLSearchParams();
    params.append('username', username.value);
    params.append('password', password.value);
    const res = await axios.post("/api/login",params);
    if (res.status === 200) {
        // 登入成功，導向首頁
        await show_modal("成功", "登入成功");
        await router.push("/");
    }else{
        await show_modal("失敗", res.data.detail);
    }
}
</script>

