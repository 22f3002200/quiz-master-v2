<template>
    <div class="card h-100 border-0 shadow-sm">
        <div class="card-body">
            <h5
                class="card-title fw-bold"
                style="color: var(--primary)"
            >
                Quiz Performance
            </h5>
            <p class="card-text text-muted small">
                Overview of quiz attempts, average, maximum, and minimum scores.
            </p>
            <div
                v-if="loading"
                class="text-center py-5"
            >
                <div
                    class="spinner-border text-primary"
                    role="status"
                >
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <div
                v-else-if="chartData.labels.length"
                class="chart-container mt-3"
            >
                <Bar
                    :data="chartData"
                    :options="chartOptions"
                />
            </div>
            <div
                v-else
                class="text-center py-5"
            >
                <p class="text-muted">No quiz performance data available.</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Bar } from "vue-chartjs";
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
} from "chart.js";
import api from "@/utils/api";

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
);

const loading = ref(true);
const chartData = ref({
    labels: [],
    datasets: [],
});

// To store user names for tooltips
const performanceData = ref([]);

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                color: "#6c757d",
            },
        },
        x: {
            ticks: {
                color: "#6c757d",
            },
        },
    },
    plugins: {
        legend: {
            labels: {
                color: "#495057",
            },
        },
        tooltip: {
            callbacks: {
                label: function (context) {
                    let label = context.dataset.label || "";
                    const value = context.parsed.y;
                    const dataIndex = context.dataIndex;
                    const datasetLabel = context.dataset.label;
                    const quizPerformance = performanceData.value[dataIndex];

                    label = `${datasetLabel}: ${value}`;

                    if (
                        datasetLabel === "Maximum Score" &&
                        quizPerformance.max_score_user
                    ) {
                        label += ` (${quizPerformance.max_score_user})`;
                    } else if (
                        datasetLabel === "Minimum Score" &&
                        quizPerformance.min_score_user
                    ) {
                        label += ` (${quizPerformance.min_score_user})`;
                    }

                    return label;
                },
            },
        },
    },
};

const fetchQuizPerformance = async () => {
    try {
        const response = await api.get("/api/admin/analytics/quiz-performance");
        performanceData.value = response.data;

        console.log(performanceData.value);

        if (performanceData.value.length) {
            chartData.value = {
                labels: performanceData.value.map((d) => d.quiz_title),
                datasets: [
                    {
                        label: "Maximum Score",
                        backgroundColor: "rgba(40, 167, 69, 0.7)",
                        borderColor: "rgba(40, 167, 69, 1)",
                        borderWidth: 1,
                        data: performanceData.value.map((d) => d.max_score),
                    },
                    {
                        label: "Average Score",
                        backgroundColor: "rgba(43, 73, 85, 0.7)",
                        borderColor: "rgba(43, 73, 85, 1)",
                        borderWidth: 1,
                        data: performanceData.value.map((d) => d.average_score),
                    },
                    {
                        label: "Minimum Score",
                        backgroundColor: "rgba(220, 53, 69, 0.7)",
                        borderColor: "rgba(220, 53, 69, 1)",
                        borderWidth: 1,
                        data: performanceData.value.map((d) => d.min_score),
                    },
                    {
                        label: "Total Attempts",
                        backgroundColor: "rgba(136, 191, 211, 0.7)",
                        borderColor: "rgba(136, 191, 211, 1)",
                        borderWidth: 1,
                        data: performanceData.value.map(
                            (d) => d.total_attempts
                        ),
                    },
                ],
            };
        }
    } catch (error) {
        console.error("Failed to fetch quiz performance data:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(fetchQuizPerformance);
</script>

<style scoped>
.chart-container {
    position: relative;
    height: 320px;
}
</style>
