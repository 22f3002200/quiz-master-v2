<template>
    <div class="d-flex admin-layout min-vh-100">
        <SideBar :nav-links="adminNavLinks" />
        <main class="flex-grow-1 main-content">
            <slot></slot>
        </main>
    </div>
</template>

<script setup>
import SideBar from "@/components/admin/SideBar.vue";

const adminNavLinks = [
    { text: "Overview", to: "/admin/dashboard", icon: "bi-grid-1x2-fill" },
    { text: "Users", to: "/admin/users", icon: "bi-people-fill" },
    {
        text: "Subjects",
        to: "/admin/subjects",
        icon: "bi-journal-bookmark-fill",
    },
    {
        text: "Chapters",
        to: "/admin/Chapters",
        icon: "bi-collection-fill",
    },
    { text: "Quizzes", to: "/admin/quizzes", icon: "bi-patch-question-fill" },
    {
        text: "Analytics",
        to: "/admin/analytics",
        icon: "bi-bar-chart-line-fill",
    },
];
</script>

<style scoped>
.admin-layout {
    background-color: var(--background);
    justify-content: center;
}
.main-content {
    background-color: var(--background);
    width: calc(100% - 250px);
}
</style>
