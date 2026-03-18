<template>
    <main class="grid min-h-screen place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8">
        <div class="text-center">
            <p class="text-base font-semibold text-indigo-600">404 Error</p>

            <h1 class="mt-4 text-3xl font-bold tracking-tight text-slate-900 sm:text-5xl">
                找不到頁面
            </h1>

            <p class="mt-6 text-base leading-7 text-slate-600">
                很抱歉，我們找不到您要求的頁面：
                <code
                        class="mx-1 rounded bg-slate-100 px-2 py-1 font-mono text-sm font-medium text-indigo-700 border border-slate-200">
                    {{ $route.path }}
                </code>
            </p>

            <p class="mt-2 text-slate-500 text-sm">
                該頁面可能已被移動、刪除，或網址輸入錯誤。
            </p>

            <div class="mt-10 flex items-center justify-center gap-x-6">
                <router-link
                        to="/"
                        class="rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-black shadow-lg hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 transition-all duration-200 active:scale-95"
                >
                    返回首頁
                </router-link>
            </div>
        </div>
    </main>
</template>