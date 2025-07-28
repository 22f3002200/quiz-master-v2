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

            <div
                v-if="loading"
                class="text-center"
            >
                <div
                    class="spinner-border text-primary"
                    role="status"
                >
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

            <div v-else>
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
        </div>
    </AdminLayout>
</template>

<script setup>
import AdminLayout from "@/components/admin/AdminLayout.vue";
import StatCard from "@/components/admin/StatCard.vue";
import QuizPerformanceChart from "@/components/admin/QuizPerformanceChart.vue";
import RecentActivityTable from "@/components/admin/RecentActivityTable.vue";
import { ref, onMounted } from "vue";
import api from "@/utils/api"; // Import the API utility

// --- Refs for dynamic data ---
const stats = ref([]);
const recentUsers = ref([]);
const recentQuizzes = ref([]);
const loading = ref(true);

// --- Table Headers ---
const userHeaders = ref([
    { text: "Name", key: "full_name" },
    { text: "Email", key: "email" },
]);

const quizHeaders = ref([
    { text: "Title", key: "title" },
    { text: "Subject", key: "subject_name" },
]);

// --- Fetch data from API ---
const fetchDashboardData = async () => {
    try {
        const response = await api.get("/api/admin/dashboard/summary");
        const data = response.data;

        // Update stats cards
        stats.value = [
            {
                title: "Total Users",
                value: data.totals.users.toLocaleString(),
                icon: "bi-people-fill",
            },
            {
                title: "Total Quizzes",
                value: data.totals.quizzes.toLocaleString(),
                icon: "bi-patch-question-fill",
            },
            {
                title: "Total Subjects",
                value: data.totals.subjects.toLocaleString(),
                icon: "bi-journal-bookmark-fill",
            },
            {
                title: "Total Attempts",
                value: data.totals.quiz_attempt.toLocaleString(),
                icon: "bi-check-circle-fill",
            },
        ];

        // Update recent users and quizzes tables
        recentUsers.value = data.recent_users;
        recentQuizzes.value = data.recent_quizzes;
    } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
        // Optionally, set an error state to show a message to the user
    } finally {
        loading.value = false;
    }
};

// --- Fetch data when component is mounted ---
onMounted(fetchDashboardData);
</script>

<style scoped>
div.container-xxl {
    margin-left: 15px;
}
</style>
