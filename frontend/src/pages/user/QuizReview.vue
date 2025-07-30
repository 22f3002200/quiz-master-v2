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
                v-else-if="reviewData"
                class="card-box p-4 rounded-3"
            >
                <h2 class="fw-bold mb-2">
                    {{ reviewData.quiz_title }} - Review
                </h2>
                <hr />
                <div
                    v-for="(question, index) in reviewData.questions"
                    :key="question.id"
                    class="mb-4"
                >
                    <p>
                        <strong>Question {{ index + 1 }}:</strong>
                        {{ question.statement }}
                    </p>

                    <p class="text-muted small">
                        Correct Answer: +{{ question.marks_for_correct }} |
                        Incorrect Answer: -{{
                            question.negative_marks_for_incorrect
                        }}
                        <span class="float-end">
                            <strong>Marks Awarded:</strong>
                            <span
                                :class="
                                    question.marks_awarded > 0
                                        ? 'text-success'
                                        : 'text-danger'
                                "
                            >
                                {{ question.marks_awarded }}
                            </span>
                        </span>
                    </p>

                    <ul class="list-group">
                        <li
                            v-for="(option, optionIndex) in question.options"
                            :key="optionIndex"
                            class="list-group-item"
                            :class="getOptionClass(question, optionIndex + 1)"
                        >
                            {{ option }}
                            <span
                                v-if="optionIndex + 1 === question.user_answer"
                                class="badge bg-primary rounded-pill ms-2"
                            >
                                Your Answer
                            </span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";

const route = useRoute();
const scoreId = route.params.scoreId;
const reviewData = ref(null);
const loading = ref(true);

const fetchReviewData = async () => {
    try {
        const response = await api.get(`/api/scores/${scoreId}/review`);
        reviewData.value = response.data;
    } catch (error) {
        console.error("Failed to fetch review data:", error);
    } finally {
        loading.value = false;
    }
};

const getOptionClass = (question, option) => {
    if (option === question.correct_option) {
        return "list-group-item-success";
    } else if (option === question.user_answer) {
        return "list-group-item-danger";
    }
    return "";
};

onMounted(fetchReviewData);
</script>

<style scoped>
@import "../../assets/subjects.css";
</style>
