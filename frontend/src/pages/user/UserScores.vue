<template>
    <UserLayout>
        <div class="container py-4">
            <div class="card-box p-4 rounded-3">
                <h2 class="fw-bold mb-4">My Scores</h2>
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
                <div
                    v-else-if="scores.length === 0"
                    class="text-center py-5"
                >
                    <p>You have not attempted any quizzes yet.</p>
                </div>
                <div
                    v-else
                    class="table-responsive"
                >
                    <table class="table table-hover align-middle">
                        <thead>
                            <tr>
                                <th scope="col">QUIZ</th>
                                <th scope="col">SUBJECT</th>
                                <th scope="col">CHAPTER</th>
                                <th scope="col">SCORE</th>
                                <th scope="col">DATE</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="score in scores"
                                :key="score.id"
                            >
                                <td>{{ score.quiz_title }}</td>
                                <td>{{ score.subject_name }}</td>
                                <td>{{ score.chapter_name }}</td>
                                <td>{{ score.total_score }}</td>
                                <td>
                                    {{
                                        new Date(
                                            score.timestamp
                                        ).toLocaleDateString()
                                    }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";

const scores = ref([]);
const loading = ref(true);

const fetchScores = async () => {
    try {
        const response = await api.get("/api/my-scores");
        scores.value = response.data;
    } catch (error) {
        console.error("Failed to fetch scores:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(fetchScores);
</script>

<style scoped>
@import "../../assets/subjects.css";
div.container {
    margin-left: 15px;
}
</style>
