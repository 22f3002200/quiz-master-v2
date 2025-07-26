<template>
    <UserLayout>
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
                <div class="col-12">
                    <RecentActivityTable
                        title="Recent Attempts"
                        :items="recentAttempts"
                        :headers="attemptHeaders"
                        view-all-path="/user/scores"
                    />
                </div>
            </div>
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";
import StatCard from "@/components/admin/StatCard.vue";
import QuizPerformanceChart from "@/components/admin/QuizPerformanceChart.vue";
import RecentActivityTable from "@/components/admin/RecentActivityTable.vue";

const stats = ref([]);
const recentAttempts = ref([]);

const attemptHeaders = ref([
    { text: "Quiz", key: "quiz_title" },
    { text: "Subject", key: "subject_name" },
    { text: "Score", key: "total_score" },
    { text: "Date", key: "timestamp" },
]);

const fetchDashboardStats = async () => {
    try {
        const response = await api.get("/api/dashboard/stats");
        const data = response.data;

        stats.value = [
            {
                title: "Total Quizzes Attempted",
                value: data.total_quizzes_attempted.toString(),
                icon: "bi-check-circle-fill",
            },
            {
                title: "Average Score",
                value: data.average_score.toFixed(2),
                icon: "bi-bar-chart-fill",
            },
            {
                title: "Best Score",
                value: data.best_score.toString(),
                icon: "bi-trophy-fill",
            },
            {
                title: "Available Quizzes",
                value: data.total_available_quizzes.toString(),
                icon: "bi-patch-question-fill",
            },
        ];

        recentAttempts.value = data.recent_attempts.map((attempt) => ({
            ...attempt,
            timestamp: new Date(attempt.timestamp).toLocaleDateString(),
        }));
    } catch (error) {
        console.error("Failed to fetch dashboard stats:", error);
    }
};

onMounted(fetchDashboardStats);
</script>

<style scoped>
div.container-xxl {
    margin-left: 15px;
}
</style>
