// frontend/src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/pages/HomePage.vue";
import LoginPage from "@/pages/LoginPage.vue";
import RegisterPage from "@/pages/RegisterPage.vue";
import AdminDashboard from "@/pages/AdminDashboard.vue";

const routes = [
    { path: "/", name: "Quiz Master", component: HomePage },
    {
        path: "/login",
        name: "Quiz Master - Login",
        component: LoginPage,
        props: { title: "QuizMaster" },
        meta: { guest: true },
    },
    {
        path: "/register",
        name: "Quiz Master - Register",
        component: RegisterPage,
        meta: { guest: true },
    },
    {
        path: "/admin/dashboard",
        name: "Admin Dashboard",
        component: AdminDashboard,
        meta: { requiresAuth: true, isAdmin: true },
    },
];

const scrollBehavior = function (to, from, savedPosition) {
    if (to.hash) {
        return {
            el: to.hash,
            behavior: "smooth",
        };
    } else if (savedPosition) {
        return savedPosition;
    } else {
        return { top: 0 };
    }
};

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior,
});

router.beforeEach((to, from, next) => {
    // Get user and admin status directly from localStorage
    const accessToken = localStorage.getItem("access_token");
    let user = null;
    let isAdmin = false;

    try {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            user = JSON.parse(storedUser);
            isAdmin = user && user.roles && user.roles.includes("admin");
        }
    } catch (e) {
        console.error(
            "Error parsing user from localStorage in router guard",
            e
        );
    }

    const isLoggedIn = !!accessToken && !!user;

    // Special handling for the root path "/"
    if (to.path === "/") {
        if (isLoggedIn && isAdmin) {
            // If an admin is logged in and navigates to "/", send them to the dashboard
            return next("/admin/dashboard");
        }
    }

    // If a logged-in user tries to visit guest pages (login/register), redirect them
    if (to.meta.guest && isLoggedIn) {
        return next(isAdmin ? "/admin/dashboard" : "/");
    }

    // Protect admin routes
    if (to.meta.isAdmin && !isAdmin) {
        return next("/");
    }

    // Protect general authenticated routes
    if (to.meta.requiresAuth && !isLoggedIn) {
        return next("/login");
    }

    // Otherwise, allow navigation
    return next();
});

export default router;
