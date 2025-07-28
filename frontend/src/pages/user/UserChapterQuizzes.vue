<template>
    <UserLayout>
        <div class="container-md p-4">
            <h2
                class="mb-4 fw-bold"
                style="color: var(--primary)"
            >
                Chapter Quizzes
            </h2>

            <div
                v-if="quizzes.length"
                class="row g-4"
            >
                <div
                    v-for="quiz in quizzes"
                    :key="quiz.id"
                    class="col-md-6 col-lg-4 card-box-subjects"
                    style="text-decoration: none"
                >
                    <div
                        class="border rounded overflow-hidden h-100 shadow-sm hover-shadow transition"
                    >
                        <!-- Top color bar -->
                        <div
                            class="w-100 d-block"
                            style="height: 4px"
                        ></div>

                        <div
                            class="p-4 d-flex flex-column justify-content-between h-100"
                        >
                            <!-- Icon and title -->
                            <div class="d-flex align-items-start mb-3">
                                <div
                                    class="p-2 rounded me-3 d-flex align-items-center justify-content-center"
                                    style="min-width: 42px; height: 42px"
                                >
                                    <i class="fs-5 bi bi-pencil-square"></i>
                                </div>
                                <div>
                                    <h5 class="fw-semibold mb-1">
                                        {{ quiz.title }}
                                    </h5>
                                    <small>
                                        Duration: {{ quiz.duration }} mins<br />
                                        Total Marks: {{ quiz.total_marks }}
                                        <br />
                                        Scheduled:
                                        {{ formatDateTime(quiz.scheduled_at) }}
                                    </small>
                                </div>
                            </div>

                            <!-- Date badge -->
                            <div class="mb-3 d-flex flex-wrap gap-2">
                                <span class="badge"
                                    >Scheduled on:
                                    {{ formatDate(quiz.date_of_quiz) }}</span
                                >
                            </div>

                            <!-- Button -->
                            <BaseButton
                                :to="`/user/quiz/${quiz.id}`"
                                class="btn btn-primary w-100"
                            >
                                Start Quiz
                            </BaseButton>
                        </div>
                    </div>
                </div>
            </div>

            <div
                v-else
                class="text-center"
            >
                <p>No quizzes are available for this chapter.</p>
            </div>
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";
import BaseButton from "@/components/base/BaseButton.vue";

const route = useRoute();
const quizzes = ref([]);
const chapterId = parseInt(route.params.chapterId);
const subjectId = parseInt(route.params.subjectId);

console.log(route);

const fetchQuizzes = async () => {
    try {
        const response = await api.get(
            `/api/admin/subjects/${subjectId}/chapters/${chapterId}/quizzes`
        );

        quizzes.value = response.data;
    } catch (error) {
        console.error("Failed to fetch chapter quizzes:", error);
    }
};

const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString();
};

const formatDateTime = (dateTimeStr) => {
    return new Date(dateTimeStr).toLocaleString();
};

onMounted(fetchQuizzes);
</script>

<style scoped>
.border {
    background-color: var(--primary5);
}

.d-block {
    background-color: var(--primary);
}

h2,
h5 {
    color: var(--primary);
}

small {
    color: var(--primary);
}

.badge {
    background-color: var(--secondary);
    color: var(--text);
}

.btn {
    background-color: var(--static);
    border: none;
}

.btn:hover {
    background-color: var(--secondary);
    transform: translate(0, -3px);
}

i {
    color: var(--primary);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.container-md {
    margin-left: 15px;
}
</style>
