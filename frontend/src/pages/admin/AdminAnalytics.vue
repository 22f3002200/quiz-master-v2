<template>
    <AdminLayout>
        <div class="container-xxl p-4">
            <h2
                class="mb-4 fw-bold"
                style="color: var(--primary)"
            >
                Analytics Overview
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
                <div class="card-box p-4 rounded-3 mb-4">
                    <h4 class="fw-bold mb-3">Quiz Performance</h4>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead>
                                <tr>
                                    <th>Quiz Title</th>
                                    <th>Total Attempts</th>
                                    <th>Average Score</th>
                                    <th>Max Score</th>
                                    <th>Min Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="quiz in quizPerformance"
                                    :key="quiz.quiz_id"
                                >
                                    <td>{{ quiz.quiz_title }}</td>
                                    <td>{{ quiz.total_attempts }}</td>
                                    <td>{{ quiz.average_score.toFixed(2) }}</td>
                                    <td>{{ quiz.max_score }}</td>
                                    <td>{{ quiz.min_score }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="card-box p-4 rounded-3">
                    <h4 class="fw-bold mb-3">User Performance</h4>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead>
                                <tr>
                                    <th>User</th>
                                    <th>Total Attempts</th>
                                    <th>Average Score</th>
                                    <th>Max Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="user in userPerformance"
                                    :key="user.user_id"
                                >
                                    <td>
                                        {{ user.full_name }} ({{ user.email }})
                                    </td>
                                    <td>{{ user.total_attemps }}</td>
                                    <td>{{ user.average_score.toFixed(2) }}</td>
                                    <td>{{ user.max_score }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import AdminLayout from "@/components/admin/AdminLayout.vue";

const quizPerformance = ref([]);
const userPerformance = ref([]);
const loading = ref(true);

const fetchAnalyticsData = async () => {
    try {
        const [quizRes, userRes] = await Promise.all([
            api.get("/api/admin/analytics/quiz-performance"),
            api.get("/api/admin/analytics/user-performance"),
        ]);
        quizPerformance.value = quizRes.data;
        userPerformance.value = userRes.data;
    } catch (error) {
        console.error("Failed to fetch analytics data:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(fetchAnalyticsData);
</script>

<style scoped>
@import "../../assets/subjects.css";

.container-xxl {
    margin-left: 15px;
}
</style>
