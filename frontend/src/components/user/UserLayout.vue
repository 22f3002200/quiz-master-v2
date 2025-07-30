<template>
    <div class="d-flex user-layout min-vh-100">
        <SideBar :nav-links="userNavLinks" />
        <main class="flex-grow-1 main-content">
            <slot></slot>
        </main>
    </div>
</template>

<script setup>
import SideBar from "@/components/admin/SideBar.vue";

const userNavLinks = [
    { text: "Dashboard", to: "/user/dashboard", icon: "bi-grid-1x2-fill" },
    {
        text: "Subjects",
        to: "/user/subjects",
        icon: "bi-journal-bookmark-fill",
    },
    { text: "Chapters", to: "/user/chapters", icon: "bi-collection-fill" },
    { text: "Quizzes", to: "/user/quizzes", icon: "bi-patch-question-fill" },
    { text: "Profile", to: "/user/profile", icon: "bi-person-fill" },
];
</script>

<style scoped>
.user-layout {
    background-color: var(--background);
    justify-content: center;
}
.main-content {
    background-color: var(--background);
    width: calc(100% - 250px); /* Adjust based on sidebar width */
}
</style>
