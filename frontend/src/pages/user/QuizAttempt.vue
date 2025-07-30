<template>
    <div class="container py-4">
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

            <div class="row">
                <div class="col-md-9">
                    <div v-if="currentQuestion">
                        <div
                            class="d-flex align-items-center justify-content-between mb-3"
                        >
                            <span
                                class="badge bg-primary rounded-pill px-3 py-2 fs-6"
                            >
                                Question {{ currentQuestionIndex + 1 }}
                            </span>
                            <span class="text-muted">
                                {{ currentQuestionIndex + 1 }} of
                                {{ quiz.questions.length }}
                            </span>
                        </div>

                        <p class="fw-semibold">
                            <span v-html="highlightedStatement"></span>
                        </p>

                        <div class="list-group my-4">
                            <button
                                type="button"
                                class="list-group-item list-group-item-action"
                                v-for="(
                                    option, index
                                ) in currentQuestion.options"
                                :key="index"
                                @click="selectOption(index + 1)"
                                :class="{
                                    active:
                                        userAnswers[currentQuestionIndex] ===
                                        index + 1,
                                }"
                            >
                                {{ String.fromCharCode(65 + index) }}.
                                {{ option }}
                            </button>
                        </div>

                        <p class="text-muted">
                            Status:
                            <span
                                :class="{
                                    'text-success':
                                        userAnswers[currentQuestionIndex] !==
                                        null,
                                    'text-danger':
                                        userAnswers[currentQuestionIndex] ===
                                        null,
                                }"
                            >
                                {{
                                    userAnswers[currentQuestionIndex] !== null
                                        ? "Attempted"
                                        : "Unattempted"
                                }}
                            </span>
                        </p>

                        <div class="d-flex justify-content-between mt-4">
                            <BaseButton
                                class="btn-secondary"
                                @click="previousQuestion"
                                :disabled="currentQuestionIndex === 0"
                            >
                                Previous
                            </BaseButton>
                            <BaseButton
                                v-if="
                                    currentQuestionIndex <
                                    quiz.questions.length - 1
                                "
                                @click="nextQuestion"
                                class="btn-primary"
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
                </div>

                <div class="col-md-3 border-start">
                    <h6 class="mb-3">Questions</h6>
                    <div class="d-flex flex-wrap gap-2">
                        <button
                            v-for="(q, idx) in quiz.questions"
                            :key="'tracker-' + idx"
                            class="btn btn-sm"
                            :class="{
                                'btn-success': userAnswers[idx] !== null,
                                'btn-outline-secondary':
                                    userAnswers[idx] === null,
                            }"
                            @click="goToQuestion(idx)"
                        >
                            Q{{ idx + 1 }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div
            v-else
            class="text-center py-5"
        >
            <p>Could not load the quiz.</p>
        </div>
        <QuizSummaryModal
            :show="showSummary"
            :summary="quizSummary"
            @close="handleSummaryClose"
        />
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/utils/api";
import BaseButton from "@/components/base/BaseButton.vue";
import QuizSummaryModal from "@/components/user/QuizSummaryModal.vue";

const route = useRoute();
const router = useRouter();
const quiz = ref(null);
const loading = ref(true);
const currentQuestionIndex = ref(0);
const userAnswers = ref([]);
const timeLeft = ref(0);
let timer;

const quizSummary = ref(null);
const showSummary = ref(false);

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
onUnmounted(() => clearInterval(timer));

const currentQuestion = computed(() =>
    quiz.value ? quiz.value.questions[currentQuestionIndex.value] : null
);

const highlightedStatement = computed(() => {
    if (!currentQuestion.value?.statement) return "";

    const parts = currentQuestion.value.statement.split("**");
    if (parts.length < 3) return currentQuestion.value.statement;

    return `${parts[0]}<strong>${parts[1]}</strong>${parts[2]}`;
});

const progress = computed(() => {
    if (!quiz.value) return 0;
    const answered = userAnswers.value.filter((ans) => ans !== null).length;
    return (answered / quiz.value.questions.length) * 100;
});

const formattedTime = computed(() => {
    const mins = Math.floor(timeLeft.value / 60);
    const secs = timeLeft.value % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
});

const selectOption = (index) => {
    userAnswers.value[currentQuestionIndex.value] = index;
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

const goToQuestion = (index) => {
    currentQuestionIndex.value = index;
};

const submitQuiz = async () => {
    clearInterval(timer);
    const answers = {};
    quiz.value.questions.forEach((q, idx) => {
        if (userAnswers.value[idx] !== null) {
            answers[q.id] = userAnswers.value[idx];
        }
    });

    try {
        const response = await api.post(`/api/quizzes/${quizId}/submit`, {
            answers,
        });
        quizSummary.value = response.data.score;
        showSummary.value = true;
    } catch (error) {
        console.error("Quiz submission failed:", error);
    }
};

const handleSummaryClose = () => {
    showSummary.value = false;
    router.push("/user/dashboard");
};
</script>

<style scoped>
.progress-bar {
    background-color: var(--primary);
}

.list-group-item.active {
    background-color: var(--primary);
    border-color: var(--primary);
    color: white;
}

.badge {
    background-color: var(--secondary);
    color: var(--text);
}

.container {
    height: 100vh;
}

.card-box {
    box-shadow: none;
}

/* Tracker buttons */
.btn-outline-secondary {
    border-width: 2px;
}

.btn-success {
    border-width: 2px;
    color: white;
}
</style>
