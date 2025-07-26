<template>
    <AdminLayout>
        <div
            class="container-xxl p-4 justify-content-center align-items-center"
        >
            <h2
                class="mb-4 fw-bold"
                style="color: var(--primary)"
            >
                Dashboard
            </h2>

            <div class="row g-4 mb-4">
                <div
                    class="col-sm-6 col-xl-3"
                    v-for="stat in stats"
                    :key="stat.title"
                >
                    <StatCard
                        :title="stat.title"
                        :value="stat.value"
                        :icon="stat.icon"
                    />
                </div>
            </div>

            <div class="row g-4 mb-4">
                <div class="col-12">
                    <QuizPerformanceChart />
                </div>
            </div>

            <div class="row g-4">
                <div class="col-md-6">
                    <RecentActivityTable
                        title="Recent Users"
                        :items="recentUsers"
                        :headers="userHeaders"
                        view-all-path="/admin/users"
                    />
                </div>
                <div class="col-md-6">
                    <RecentActivityTable
                        title="Recent Quizzes"
                        :items="recentQuizzes"
                        :headers="quizHeaders"
                        view-all-path="/admin/quizzes"
                    />
                </div>
            </div>
        </div>
    </AdminLayout>
</template>

<script setup>
import AdminLayout from "@/components/admin/AdminLayout.vue";
import StatCard from "@/components/admin/StatCard.vue";
import QuizPerformanceChart from "@/components/admin/QuizPerformanceChart.vue";
import RecentActivityTable from "@/components/admin/RecentActivityTable.vue";

import { ref } from "vue";

// --- Mock Data (Replace with API calls) ---

// Data for the summary stat cards
const stats = ref([
    { title: "Total Users", value: "150,040", icon: "bi-people-fill" },
    { title: "Total Quizzes", value: "300", icon: "bi-patch-question-fill" },
    { title: "Total Subjects", value: "12", icon: "bi-journal-bookmark-fill" },
    { title: "Total Attempts", value: "42,530", icon: "bi-check-circle-fill" },
]);

// Data for the recent users table
const recentUsers = ref([
    { id: 1, name: "John Doe", email: "john.doe@example.com" },
    { id: 2, name: "Jane Smith", email: "jane.smith@example.com" },
    { id: 3, name: "Peter Jones", email: "peter.jones@example.com" },
]);
const userHeaders = ref([
    { text: "Name", key: "name" },
    { text: "Email", key: "email" },
]);

// Data for the recent quizzes table
const recentQuizzes = ref([
    { id: 1, title: "Modern History", subject: "History" },
    { id: 2, title: "Web Development Basics", subject: "Technology" },
    { id: 3, title: "Advanced Algebra", subject: "Mathematics" },
]);
const quizHeaders = ref([
    { text: "Title", key: "title" },
    { text: "Subject", key: "subject" },
]);
</script>

<style scoped>
div.container-xxl {
    margin-left: 15px;
}
</style>
