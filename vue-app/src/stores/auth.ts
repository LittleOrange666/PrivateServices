import {defineStore} from "pinia";
import {ref} from "vue";
import axios from "axios";

type Role = "admin" | "user" | "unauthorized"

export const useAuthStore = defineStore('auth', () => {
    const name = ref<string>("");
    const role = ref<Role>("unauthorized");
    const loaded = ref<boolean>(false);
    async function load(){
        if (loaded.value) return;
        loaded.value = true;
        try{
            const res = await axios.get("/api/verify");
            if (res.status === 200) {
                name.value = res.data.user;
                role.value = res.data.role;
            }
        }catch(e){
            console.error(e);
        }
    }

    return {
        name,
        role,
        load,
        loaded
    }
});