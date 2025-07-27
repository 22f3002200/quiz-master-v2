import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/pages/HomePage.vue";
import LoginPage from "@/pages/LoginPage.vue";
import RegisterPage from "@/pages/RegisterPage.vue";
import AdminDashboard from "@/pages/admin/AdminDashboard.vue";
import AdminSubjects from "@/pages/admin/AdminSubjects.vue";
import AdminChapters from "@/pages/admin/AdminChapters.vue";
import AdminUsers from "@/pages/admin/AdminUsers.vue";
import AdminQuizzes from "@/pages/admin/AdminQuizzes.vue";
import AdminQuestions from "@/pages/admin/AdminQuestions.vue";
import UserDashboard from "@/pages/user/UserDashboard.vue";
import UserSubjects from "@/pages/user/UserSubjects.vue";
import UserChapters from "@/pages/user/UserChapters.vue";
import UserProfile from "@/pages/user/UserProfile.vue";
import UserSubjectChapters from "@/pages/user/UserSubjectChapters.vue";
import UserSubjectQuizzes from "@/pages/user/UserSubjectQuizzes.vue";
import UserChapterQuizzes from "@/pages/user/UserChapterQuizzes.vue";

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
    {
        path: "/admin/subjects",
        name: "Manage Subjects",
        component: AdminSubjects,
        meta: { requiresAuth: true, isAdmin: true },
    },
    {
        path: "/admin/chapters",
        name: "Manage Chapters",
        component: AdminChapters,
        meta: { requiresAuth: true, isAdmin: true },
    },
    {
        path: "/admin/quizzes",
        name: "Manage Quizzes",
        component: AdminQuizzes,
        meta: { requiresAuth: true, isAdmin: true },
    },
    {
        path: "/admin/quizzes/:quizId/questions",
        name: "Manage Questions",
        component: AdminQuestions,
        meta: { requiresAuth: true, isAdmin: true },
    },
    {
        path: "/admin/users",
        name: "View Users",
        component: AdminUsers,
        meta: { requiresAuth: true, isAdmin: true },
    },
    {
        path: "/user/dashboard",
        name: "User Dashboard",
        component: UserDashboard,
        meta: { requiresAuth: true, isUser: true },
    },
    {
        path: "/user/subjects",
        name: "View Subjects",
        component: UserSubjects,
        meta: { requiresAuth: true, isUser: true },
    },
    {
        path: "/user/chapters",
        name: "View Chapters",
        component: UserChapters,
        meta: { requiresAuth: true, isUser: true },
    },
    {
        path: "/user/subjects/:subjectId/chapters",
        name: "View Subject Chapters",
        component: UserSubjectChapters,
        meta: { requiresAuth: true, isUser: true },
    },
    {
        path: "/user/quizzes/subjects/:subjectId",
        name: "View Subject Quizzes",
        component: UserSubjectQuizzes,
        meta: { requiresAuth: true, isUser: true },
    },
    {
        path: "/user/subjects/:subjectId/chapters/:chapterId/quizzes",
        name: "View Chapter Quizzes",
        component: UserChapterQuizzes,
        meta: { requiresAuth: true, isUser: true },
    },
    {
        path: "/user/profile",
        name: "User Profile",
        component: UserProfile,
        meta: { requiresAuth: true, isUser: true },
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
    const accessToken = localStorage.getItem("access_token");
    const storedUser = localStorage.getItem("user");
    let user = null;

    try {
        if (storedUser) {
            user = JSON.parse(storedUser);
        }
    } catch (e) {
        // Clear invalid data if parsing fails
        localStorage.removeItem("user");
        localStorage.removeItem("access_token");
        console.error("Failed to parse user from localStorage:", e);
    }

    const isLoggedIn = !!accessToken && !!user;
    // Use a case-insensitive and safe check for roles
    const userRole = user ? (user.role || "").toLowerCase() : "";
    const isAdmin = userRole === "admin";
    const isUser = userRole === "user";

    // Redirect logged-in users from guest pages (like /login)
    if (to.meta.guest && isLoggedIn) {
        if (isAdmin) return next("/admin/dashboard");
        return next("/user/dashboard"); // Default for other logged-in users
    }

    // Block access to protected routes if not logged in
    if (to.meta.requiresAuth && !isLoggedIn) {
        return next("/login");
    }

    // Handle role-specific route access for logged-in users
    if (isLoggedIn) {
        // If a non-admin tries to access an admin-only route
        if (to.meta.isAdmin && !isAdmin) {
            return next("/user/dashboard"); // Redirect to their own dashboard
        }
        // If a non-user (i.e., an admin) tries to access a user-only route
        if (to.meta.isUser && !isUser) {
            return next("/admin/dashboard"); // Redirect to their own dashboard
        }
    }

    // If none of the above, allow navigation
    return next();
});

export default router;
