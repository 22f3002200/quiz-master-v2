<template>
    <AdminLayout>
        <div class="container py-4">
            <div class="card-box p-4 rounded-3">
                <div
                    class="d-flex justify-content-between align-items-center mb-4"
                >
                    <h2 class="fw-bold mb-0">Questions for {{ quizTitle }}</h2>
                    <BaseButton
                        @click="openAddModal"
                        class="btn-primary"
                    >
                        <i class="bi bi-plus-lg me-2"></i>Add New Question
                    </BaseButton>
                </div>

                <!-- Marks Toggle -->
                <div
                    class="form-check form-switch mb-3 d-flex align-items-center gap-2 ps-0"
                >
                    <input
                        class="form-check-input"
                        type="checkbox"
                        id="uniformMarksToggle"
                        v-model="uniformMarks"
                    />
                    <label
                        class="form-check-label"
                        for="uniformMarksToggle"
                        >Set same marks for all questions</label
                    >
                </div>

                <!-- Negative Toggle -->
                <div
                    class="form-check form-switch mb-3 d-flex align-items-center gap-2 ps-0"
                >
                    <input
                        class="form-check-input"
                        type="checkbox"
                        id="negativeMarkingToggle"
                        v-model="enableNegativeMarking"
                    />
                    <label
                        class="form-check-label"
                        for="negativeMarkingToggle"
                        >Enable Negative Marking</label
                    >
                </div>

                <!-- Marks + Negative Input Row -->
                <div
                    v-if="uniformMarks"
                    class="mb-3 d-flex align-items-end gap-3 flex-wrap"
                >
                    <div>
                        <label
                            for="uniformMarksValue"
                            class="form-label fw-semibold"
                            >Marks for each question</label
                        >
                        <input
                            type="number"
                            class="form-control"
                            id="uniformMarksValue"
                            v-model="uniformMarksValue"
                            min="1"
                        />
                    </div>

                    <div v-if="enableNegativeMarking">
                        <label
                            for="uniformNegativeMarksValue"
                            class="form-label fw-semibold"
                            >Negative Marks</label
                        >
                        <input
                            type="number"
                            class="form-control"
                            id="uniformNegativeMarksValue"
                            v-model="uniformNegativeMarksValue"
                            min="0"
                            step="0.1"
                        />
                    </div>
                </div>

                <!-- Loading / No Questions / Table -->
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
                    v-else-if="questions.length === 0"
                    class="text-center py-5"
                >
                    <p>
                        No questions found for this quiz. Add a new one to get
                        started!
                    </p>
                </div>
                <div
                    v-else
                    class="table-responsive"
                >
                    <table class="table table-hover align-middle">
                        <thead>
                            <tr>
                                <th scope="col">STATEMENT</th>
                                <th scope="col">OPTIONS</th>
                                <th
                                    v-if="!uniformMarks"
                                    scope="col"
                                >
                                    MARKS
                                </th>
                                <th
                                    v-if="!uniformMarks"
                                    scope="col"
                                >
                                    NEGATIVE
                                </th>
                                <th
                                    scope="col"
                                    class="text-end"
                                >
                                    ACTIONS
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="question in questions"
                                :key="question.id"
                            >
                                <td>{{ question.statement }}</td>
                                <td>
                                    <ul class="list-unstyled mb-0">
                                        <li
                                            v-for="(option, index) in [
                                                question.option1,
                                                question.option2,
                                                question.option3,
                                                question.option4,
                                            ]"
                                            :key="index"
                                            :class="{
                                                'fw-bold text-success':
                                                    index + 1 ===
                                                    question.correct_option,
                                            }"
                                        >
                                            {{ option }}
                                        </li>
                                    </ul>
                                </td>
                                <td v-if="!uniformMarks">
                                    {{ question.marks }}
                                </td>
                                <td v-if="!uniformMarks">
                                    {{
                                        question.negative_marks > 0
                                            ? `-${question.negative_marks}`
                                            : 0
                                    }}
                                </td>
                                <td class="text-end">
                                    <div
                                        class="d-flex justify-content-end gap-2"
                                    >
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-success edit"
                                            @click="openEditModal(question)"
                                        >
                                            <i class="bi bi-pencil"></i>
                                        </BaseButton>
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-danger delete"
                                            @click="deleteQuestion(question.id)"
                                        >
                                            <i class="bi bi-trash"></i>
                                        </BaseButton>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Modal -->
            <BaseModal
                :show="isModalVisible"
                @close="closeModal"
            >
                <template #header>{{
                    isEditing ? "Edit Question" : "Add New Question"
                }}</template>
                <template #body>
                    <form @submit.prevent="handleQuestionSubmit">
                        <div class="mb-3">
                            <label
                                for="questionStatement"
                                class="form-label fw-semibold"
                                >Question Statement</label
                            >
                            <textarea
                                class="form-control"
                                id="questionStatement"
                                rows="3"
                                v-model="currentQuestion.statement"
                                required
                            ></textarea>
                        </div>
                        <div
                            class="mb-3"
                            v-for="n in 4"
                            :key="n"
                        >
                            <label
                                :for="'option' + n"
                                class="form-label fw-semibold"
                                >Option {{ n }}</label
                            >
                            <input
                                type="text"
                                class="form-control"
                                :id="'option' + n"
                                v-model="currentQuestion['option' + n]"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="correctOption"
                                class="form-label fw-semibold"
                                >Correct Option</label
                            >
                            <select
                                class="form-select"
                                id="correctOption"
                                v-model.number="currentQuestion.correct_option"
                                required
                            >
                                <option
                                    disabled
                                    value=""
                                >
                                    Please select correct option:
                                </option>
                                <option
                                    v-for="n in 4"
                                    :value="n"
                                    :key="n"
                                >
                                    Option {{ n }}
                                </option>
                            </select>
                        </div>
                        <div
                            v-if="!uniformMarks"
                            class="mb-3"
                        >
                            <label
                                for="questionMarks"
                                class="form-label fw-semibold"
                                >Marks</label
                            >
                            <input
                                type="number"
                                class="form-control"
                                id="questionMarks"
                                v-model.number="currentQuestion.marks"
                                min="1"
                            />
                        </div>
                        <div
                            v-if="!uniformMarks"
                            class="mb-3"
                        >
                            <label
                                for="questionNegativeMarks"
                                class="form-label fw-semibold"
                                >Negative Marks</label
                            >
                            <input
                                type="number"
                                class="form-control"
                                id="questionNegativeMarks"
                                v-model.number="currentQuestion.negative_marks"
                                min="0"
                                step="0.1"
                            />
                        </div>
                    </form>
                </template>
                <template #footer>
                    <BaseButton
                        color="secondary"
                        @click="closeModal"
                        >Cancel</BaseButton
                    >
                    <BaseButton
                        color="primary"
                        @click="handleQuestionSubmit"
                        :loading="isSubmitting"
                    >
                        {{ isEditing ? "Save Changes" : "Add Question" }}
                    </BaseButton>
                </template>
            </BaseModal>
        </div>
    </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import api from "@/utils/api";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseModal from "@/components/base/BaseModal.vue";
import AdminLayout from "@/components/admin/AdminLayout.vue";

const route = useRoute();
const quizId = computed(() => route.params.quizId);
const quizTitle = ref("");
const questions = ref([]);
const loading = ref(true);
const isModalVisible = ref(false);
const isEditing = ref(false);
const isSubmitting = ref(false);
const uniformMarks = ref(true);
const uniformMarksValue = ref(4);
const enableNegativeMarking = ref(false);
const uniformNegativeMarksValue = ref(0);

const currentQuestion = ref({
    id: null,
    statement: "",
    option1: "",
    option2: "",
    option3: "",
    option4: "",
    correct_option: 1,
    marks: 4,
    negative_marks: 0,
});

const fetchQuizDetails = async () => {
    try {
        const response = await api.get(`/api/admin/quizzes`);
        quizTitle.value = response.data[0].title;
    } catch (error) {
        console.error("Failed to fetch quiz details:", error);
    }
};

const fetchQuestions = async () => {
    try {
        loading.value = true;
        const response = await api.get(
            `/api/admin/quizzes/${quizId.value}/questions`
        );
        questions.value = response.data;
    } catch (error) {
        console.error("Failed to fetch questions:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchQuizDetails();
    fetchQuestions();
});

const openAddModal = () => {
    isEditing.value = false;
    currentQuestion.value = {
        id: null,
        statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_option: 1,
        marks: uniformMarks.value ? uniformMarksValue.value : 4,
        negative_marks:
            uniformMarks.value && enableNegativeMarking.value
                ? uniformNegativeMarksValue.value
                : 0,
    };
    isModalVisible.value = true;
};

const openEditModal = (question) => {
    isEditing.value = true;
    currentQuestion.value = {
        ...question,
        negative_marks: question.negative_marks ?? 0,
    };
    isModalVisible.value = true;
};

const closeModal = () => {
    isModalVisible.value = false;
};

const handleQuestionSubmit = async () => {
    isSubmitting.value = true;
    if (uniformMarks.value) {
        currentQuestion.value.marks = uniformMarksValue.value;
        currentQuestion.value.negative_marks = enableNegativeMarking.value
            ? uniformNegativeMarksValue.value
            : 0;
    }

    try {
        if (isEditing.value) {
            await api.put(
                `/api/admin/questions/${currentQuestion.value.id}`,
                currentQuestion.value
            );
        } else {
            await api.post(
                `/api/admin/quizzes/${quizId.value}/questions`,
                currentQuestion.value
            );
        }
        await fetchQuestions();
        closeModal();
    } catch (error) {
        console.error("Failed to save question:", error);
    } finally {
        isSubmitting.value = false;
    }
};

const deleteQuestion = async (id) => {
    if (confirm("Are you sure you want to delete this question?")) {
        try {
            await api.delete(`/api/admin/questions/${id}`);
            await fetchQuestions();
        } catch (error) {
            console.error("Failed to delete question:", error);
        }
    }
};
</script>

<style scoped>
@import "../../assets/subjects.css";

.form-switch .form-check-input {
    width: 3em;
    height: 1.5em;
    background-color: var(--background);
    margin: 0 !important;
    padding-left: 0 !important;
}

.form-switch .form-check-input:checked {
    background-color: var(--primary);
}
</style>
