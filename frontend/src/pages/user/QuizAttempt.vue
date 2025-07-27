<template>
    <UserLayout>
        <div class="container py-4">
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
                v-else-if="quiz"
                class="card-box p-4 rounded-3"
            >
                <h2 class="fw-bold mb-2">{{ quiz.title }}</h2>
                <p class="text-muted">Time Remaining: {{ formattedTime }}</p>

                <div class="progress mb-4">
                    <div
                        class="progress-bar"
                        role="progressbar"
                        :style="{ width: progress + '%' }"
                        :aria-valuenow="progress"
                        aria-valuemin="0"
                        aria-valuemax="100"
                    >
                        {{ Math.round(progress) }}%
                    </div>
                </div>

                <div v-if="currentQuestion">
                    <h5 class="fw-semibold mb-3">
                        {{ currentQuestion.statement }}
                    </h5>
                    <div class="list-group">
                        <button
                            type="button"
                            class="list-group-item list-group-item-action"
                            v-for="(option, index) in currentQuestion.options"
                            :key="index"
                            @click="selectOption(index + 1)"
                            :class="{
                                active:
                                    userAnswers[currentQuestionIndex] ===
                                    index + 1,
                            }"
                        >
                            {{ option }}
                        </button>
                    </div>
                </div>

                <div class="d-flex justify-content-between mt-4">
                    <BaseButton
                        @click="previousQuestion"
                        :disabled="currentQuestionIndex === 0"
                    >
                        Previous
                    </BaseButton>
                    <BaseButton
                        v-if="currentQuestionIndex < quiz.questions.length - 1"
                        @click="nextQuestion"
                    >
                        Next
                    </BaseButton>
                    <BaseButton
                        v-else
                        @click="submitQuiz"
                        color="primary"
                    >
                        Submit Quiz
                    </BaseButton>
                </div>
            </div>
            <div
                v-else
                class="text-center py-5"
            >
                <p>Could not load the quiz.</p>
            </div>
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";
import BaseButton from "@/components/base/BaseButton.vue";

const route = useRoute();
const router = useRouter();
const quiz = ref(null);
const loading = ref(true);
const currentQuestionIndex = ref(0);
const userAnswers = ref([]);
const timeLeft = ref(0);
let timer;

const quizId = route.params.quizId;

const fetchQuiz = async () => {
    try {
        const response = await api.get(`/api/quizzes/${quizId}`);
        quiz.value = {
            ...response.data,
            questions: response.data.questions.map((q) => ({
                ...q,
                options: [q.option1, q.option2, q.option3, q.option4],
            })),
        };
        userAnswers.value = new Array(quiz.value.questions.length).fill(null);
        timeLeft.value = quiz.value.duration * 60;
        startTimer();
    } catch (error) {
        console.error("Failed to fetch quiz:", error);
    } finally {
        loading.value = false;
    }
};

const startTimer = () => {
    timer = setInterval(() => {
        if (timeLeft.value > 0) {
            timeLeft.value--;
        } else {
            submitQuiz();
        }
    }, 1000);
};

onMounted(fetchQuiz);

onUnmounted(() => {
    clearInterval(timer);
});

const currentQuestion = computed(() => {
    return quiz.value ? quiz.value.questions[currentQuestionIndex.value] : null;
});

const progress = computed(() => {
    if (!quiz.value) return 0;
    const answeredCount = userAnswers.value.filter(
        (answer) => answer !== null
    ).length;
    return (answeredCount / quiz.value.questions.length) * 100;
});

const formattedTime = computed(() => {
    const minutes = Math.floor(timeLeft.value / 60);
    const seconds = timeLeft.value % 60;
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
});

const selectOption = (optionIndex) => {
    userAnswers.value[currentQuestionIndex.value] = optionIndex;
};

const nextQuestion = () => {
    if (currentQuestionIndex.value < quiz.value.questions.length - 1) {
        currentQuestionIndex.value++;
    }
};

const previousQuestion = () => {
    if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--;
    }
};

const submitQuiz = async () => {
    clearInterval(timer);
    const answers = {};
    quiz.value.questions.forEach((question, index) => {
        if (userAnswers.value[index] !== null) {
            answers[question.id] = userAnswers.value[index];
        }
    });

    try {
        await api.post(`/api/quizzes/${quizId}/submit`, { answers });
        // Redirect to a results page or dashboard
        router.push("/user/dashboard");
    } catch (error) {
        console.error("Failed to submit quiz:", error);
    }
};
</script>

<style scoped>
@import "../../assets/subjects.css";

.progress-bar {
    background-color: var(--primary);
}

.list-group-item.active {
    background-color: var(--primary);
    border-color: var(--primary);
}
</style>
