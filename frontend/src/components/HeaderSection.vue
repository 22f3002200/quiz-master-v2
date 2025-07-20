<template>
    <header class="bg-white shadow-sm sticky-top">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center py-3">
                <h2 class="text-primary fw-bold mb-0">QuizMaster</h2>
                <nav class="d-none d-md-flex gap-4 align-items-center">
                    <template v-if="!user">
                        <a
                            href="/#features"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Features</a
                        >
                        <a
                            href="/#how-it-works"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >How It Works</a
                        >
                        <a
                            href="/#categories"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Categories</a
                        >
                        <router-link
                            to="/login"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Login</router-link
                        >
                        <router-link
                            to="/register"
                            class="btn gradient btn-primary"
                            >Sign Up</router-link
                        >
                    </template>
                    <template v-else-if="isAdmin">
                        <router-link
                            to="/admin/dashboard"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Dashboard</router-link
                        >
                        <router-link
                            to="/admin/subjects"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Subjects</router-link
                        >
                        <router-link
                            to="/admin/quizzes"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Quizzes</router-link
                        >
                        <router-link
                            to="/admin/users"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Users</router-link
                        >
                        <button
                            @click="handleLogout"
                            class="btn btn-link text-secondary text-decoration-none hover-text-primary"
                        >
                            Logout
                        </button>
                    </template>
                    <template v-else>
                        <a
                            href="/#features"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Features</a
                        >
                        <a
                            href="/#how-it-works"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >How It Works</a
                        >
                        <a
                            href="/#categories"
                            class="text-secondary text-decoration-none hover-text-primary"
                            >Categories</a
                        >
                        <button
                            @click="handleLogout"
                            class="btn btn-link text-secondary text-decoration-none hover-text-primary"
                        >
                            Logout
                        </button>
                    </template>
                </nav>
                <button
                    class="btn d-md-none"
                    @click="isMenuOpen = !isMenuOpen"
                >
                    <i :class="isMenuOpen ? 'bi-x-lg' : 'bi-list'"></i>
                </button>
            </div>
        </div>

        <div
            v-if="isMenuOpen"
            class="d-md-none bg-white shadow-sm px-3 pt-2 pb-3"
        ></div>
    </header>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";

const isMenuOpen = ref(false);
const router = useRouter();
const { user, isAdmin, logout } = useAuth();

const handleLogout = () => {
    logout();
    router.push("/login");
};
</script>
