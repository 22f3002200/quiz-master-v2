import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/pages/HomePage.vue";
import LoginPage from "@/pages/LoginPage.vue";
import RegisterPage from "@/pages/RegisterPage.vue";
// import AdminDashboard from "@/pages/AdminDashboard.vue";

const routes = [
    { path: "/", name: "Quiz Master", component: HomePage },
    { path: "/login", name: "Quiz Master - Login", component: LoginPage },
    {
        path: "/register",
        name: "Quiz Master - Register",
        component: RegisterPage,
    },
    // {
    //     path: "/admin/dashboard",
    //     name: "Admin Dashboard",
    //     component: AdminDashboard,
    // },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
