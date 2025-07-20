<!-- components/Header.vue -->
<template>
    <header class="bg-white shadow-sm sticky-top">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center py-3">
                <h2 class="text-primary fw-bold mb-0">QuizMaster</h2>
                <nav class="d-none d-md-flex gap-4 align-items-center">
                    <a
                        href="#features"
                        class="text-secondary text-decoration-none hover-text-primary"
                        >Features</a
                    >
                    <a
                        href="#how-it-works"
                        class="text-secondary text-decoration-none hover-text-primary"
                        >How It Works</a
                    >
                    <a
                        href="#categories"
                        class="text-secondary text-decoration-none hover-text-primary"
                        >Categories</a
                    >
                    <a
                        href="#"
                        class="text-secondary text-decoration-none hover-text-primary"
                        >Pricing</a
                    >
                    <button class="btn gradient btn-primary">
                        Sign Up Free
                    </button>
                </nav>
                <button
                    class="btn d-md-none"
                    @click="isMenuOpen = !isMenuOpen"
                >
                    <i :class="isMenuOpen ? 'bi-x-lg' : 'bi-list'"></i>
                </button>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div
            v-if="isMenuOpen"
            class="d-md-none bg-white shadow-sm px-3 pt-2 pb-3"
        >
            <a
                href="#features"
                class="d-block py-2 text-secondary"
                @click="isMenuOpen = false"
                >Features</a
            >
            <a
                href="#how-it-works"
                class="d-block py-2 text-secondary"
                @click="isMenuOpen = false"
                >How It Works</a
            >
            <a
                href="#categories"
                class="d-block py-2 text-secondary"
                @click="isMenuOpen = false"
                >Categories</a
            >
            <a
                href="#"
                class="d-block py-2 text-secondary"
                @click="isMenuOpen = false"
                >Pricing</a
            >
            <button class="btn btn-primary w-100 mt-3">Sign Up Free</button>
        </div>
    </header>
</template>

<script setup>
import { ref } from "vue";
const isMenuOpen = ref(false);
</script>
