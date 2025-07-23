<template>
    <header>
        <nav class="navbar navbar-expand-lg navbar-light shadow-sm py-2">
            <div class="container-xxl">
                <a
                    class="navbar-brand d-flex align-items-center gap-2"
                    href="#"
                >
                    <i
                        class="bi bi-hourglass-split fs-3"
                        style="color: var(--primary)"
                    ></i>
                    <router-link
                        to="/"
                        class="h4 mb-0 fw-bold"
                        style="color: var(--primary); text-decoration: none"
                    >
                        QuizMaster
                    </router-link>
                </a>
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
                            v-for="link in links"
                            :key="link.id"
                            class="nav-item"
                        >
                            <a
                                :key="link.id"
                                :class="link.class"
                                :href="link.href"
                                >{{ link.field }}</a
                            >
                        </li>
                    </ul>
                    <span class="d-flex"
                        ><div class="d-flex align-items-end ms-auto gap-2">
                            <router-link
                                v-for="button in buttons"
                                :key="button.id"
                                :to="button.to"
                                :class="button.class"
                                >{{ button.text }}</router-link
                            >
                        </div></span
                    >
                </div>
            </div>
        </nav>
    </header>
</template>

<script>
import "../assets/global.css";

export default {
    data() {
        return {
            links: [
                {
                    id: "features",
                    type: "nav-item",
                    class: "nav-link",
                    href: "/#features",
                    field: "Features",
                },
                {
                    id: "how-it-works",
                    class: "nav-link",
                    href: "/#how-it-works",
                    field: "How It Works",
                },
                {
                    id: "categories",
                    class: "nav-link",
                    href: "/#categories",
                    field: "Categories",
                },
            ],

            buttons: [
                {
                    id: "login",
                    to: "/login",
                    class: ["btn", "login"],
                    text: "Login",
                },
                {
                    id: "register",
                    to: "/register",
                    class: ["btn", "signup"],
                    text: "Sign up",
                },
            ],
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
.btn.signup {
    background-color: var(--primary);
    color: var(--background);
}

.btn.login {
    background-color: var(--secondary);
    color: var(--text);
}

.btn.login:hover,
.btn.signup:hover {
    box-shadow: 0 20px 80px -10px var(--text);
}
</style>
