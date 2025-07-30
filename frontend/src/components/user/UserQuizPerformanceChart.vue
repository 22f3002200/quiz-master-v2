<template>
    <div class="card h-100 border-0 shadow-sm">
        <div class="card-body">
            <h5
                class="card-title fw-bold"
                style="color: var(--primary)"
            >
                My Quiz Performance
            </h5>
            <p class="card-text text-muted small">
                Overview of your scores in attempted quizzes.
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
                <Line
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
import { Line } from "vue-chartjs";
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
} from "chart.js";
import api from "@/utils/api";

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement
);

const loading = ref(true);
const chartData = ref({
    labels: [],
    datasets: [],
});

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
    },
};

const fetchUserPerformance = async () => {
    try {
        const response = await api.get("/api/dashboard/performance");
        const performanceData = response.data;

        if (performanceData.length) {
            chartData.value = {
                labels: performanceData.map((d) =>
                    new Date(d.timestamp).toLocaleDateString()
                ),
                datasets: [
                    {
                        label: "My Score",
                        backgroundColor: "rgba(43, 73, 85, 0.7)",
                        borderColor: "rgba(43, 73, 85, 1)",
                        borderWidth: 2,
                        data: performanceData.map((d) => d.total_score),
                        fill: false,
                        tension: 0.1,
                    },
                ],
            };
        }
    } catch (error) {
        console.error("Failed to fetch user quiz performance data:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(fetchUserPerformance);
</script>

<style scoped>
.chart-container {
    position: relative;
    height: 320px;
}
</style>
