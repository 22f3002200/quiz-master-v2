<template>
    <header>
        <nav class="navbar navbar-expand-lg navbar-light shadow-sm py-2">
            <div class="container-xxl">
                <router-link
                    to="/"
                    class="navbar-brand d-flex align-items-center gap-2"
                >
                    <i
                        class="bi bi-hourglass-split fs-3"
                        style="color: var(--primary)"
                    ></i>
                    <span
                        class="h4 mb-0 fw-bold"
                        style="color: var(--primary)"
                    >
                        {{ title }}
                    </span>
                </router-link>

                <button
                    class="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div
                    class="collapse navbar-collapse"
                    id="navbarNav"
                >
                    <ul class="navbar-nav ms-auto align-items-end">
                        <li
                            v-for="link in visibleLinks"
                            :key="link.id"
                            class="nav-item"
                        >
                            <router-link
                                :to="link.to"
                                :class="link.class"
                                >{{ link.field }}</router-link
                            >
                        </li>
                    </ul>

                    <div class="d-flex align-items-end ms-auto gap-2">
                        <!-- Show login/signup buttons if user not logged in -->
                        <span class="d-flex ms-auto gap-2">
                            <template v-if="!user">
                                <router-link
                                    v-for="button in buttons"
                                    :key="button.id"
                                    :to="button.to"
                                    :class="['btn', button.class]"
                                >
                                    {{ button.text }}
                                </router-link>
                            </template>

                            <!-- Show logout if user is logged in -->
                            <template v-else>
                                <button
                                    @click="logout"
                                    class="btn btn-danger"
                                >
                                    Logout
                                </button>
                            </template>
                        </span>
                    </div>
                </div>
            </div>
        </nav>
    </header>
</template>

<script>
import { useAuth } from "@/composables/useAuth";
import { computed } from "vue";
export default {
    setup() {
        const { user, logout } = useAuth();

        const allLinks = [
            {
                // Guest Links
                id: "features",
                type: "nav-item",
                class: "nav-link",
                to: "/#features",
                field: "Features",
                showFor: "guest",
            },
            {
                id: "how-it-works",
                class: "nav-link",
                to: "/#how-it-works",
                field: "How It Works",
                showFor: "guest",
            },
            {
                id: "categories",
                class: "nav-link",
                to: "/#categories",
                field: "Categories",
                showFor: "guest",
            },
            {
                // Admin Links
                id: "admin-dashboard",
                class: "nav-link",
                to: "/admin/dashboard",
                field: "Dashboard",
                showFor: "admin",
            },
            {
                id: "admin-subjects",
                class: "nav-link",
                to: "/admin/subjects",
                field: "Subjects",
                showFor: "admin",
            },
            {
                id: "admin-quizzes",
                class: "nav-link",
                to: "/admin/quizzes",
                field: "Quizzes",
                showFor: "admin",
            },
            // User Links
            {
                id: "user-dashboard",
                class: "nav-link",
                to: "/user/dashboard",
                field: "Dashboard",
                showFor: "user",
            },
            {
                id: "user-subjects",
                class: "nav-link",
                to: "/user/subjects",
                field: "Subjects",
                showFor: "user",
            },
            {
                id: "user-quizzes",
                class: "nav-link",
                to: "/user/quizzes",
                field: "Quizzes",
                showFor: "user",
            },
        ];
        const buttons = [
            {
                id: "login",
                to: "/login",
                class: "login",
                text: "Login",
            },
            {
                id: "register",
                to: "/register",
                class: "signup",
                text: "Sign up",
            },
        ];
        const visibleLinks = computed(() => {
            if (!user.value) {
                return allLinks.filter((link) => link.showFor === "guest");
            } else if (user.value.role === "admin") {
                return allLinks.filter((link) => link.showFor === "admin");
            } else if (user.value.role === "user") {
                return allLinks.filter((link) => link.showFor === "user");
            }
            return [];
        });
        const isLoggedIn = computed(() => !!user.value);

        return {
            title: "QuizMaster",
            user,
            logout,
            buttons,
            visibleLinks,
            isLoggedIn,
        };
    },
};
</script>

<style scoped>
nav.navbar {
    background-color: var(--background);
}

.nav-link {
    color: var(--text) !important;
}
.nav-link:hover {
    color: var(--primary) !important;
}
.btn.signup,
.btn.signup:active {
    background-color: var(--primary);
    color: var(--background);
}

.btn.login,
.btn.login:active {
    background-color: var(--secondary);
    color: var(--text);
}

.btn.login:hover,
.btn.signup:hover {
    box-shadow: 0 4px 12px -2px var(--text);
}
</style>
