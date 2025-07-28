<template>
    <AdminLayout>
        <div class="container py-4">
            <div class="card-box p-4 rounded-3">
                <div
                    class="d-flex justify-content-between align-items-center mb-4"
                >
                    <h2 class="fw-bold mb-0">Quizzes</h2>
                    <BaseButton
                        @click="openAddModal"
                        class="btn-primary"
                    >
                        <i class="bi bi-plus-lg me-2"></i>Add New Quiz
                    </BaseButton>
                </div>

                <div class="row mb-3">
                    <div class="col-md-6">
                        <label
                            for="subjectFilter"
                            class="form-label fw-semibold"
                            >Filter by Subject</label
                        >
                        <select
                            id="subjectFilter"
                            class="form-select"
                            v-model="selectedSubject"
                            @change="fetchChaptersAndQuizzes"
                        >
                            <option :value="null">All Subjects</option>
                            <option
                                v-for="subject in subjects"
                                :key="subject.id"
                                :value="subject.id"
                            >
                                {{ subject.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label
                            for="chapterFilter"
                            class="form-label fw-semibold"
                            >Filter by Chapter</label
                        >
                        <select
                            id="chapterFilter"
                            class="form-select"
                            v-model="selectedChapter"
                            @change="fetchQuizzes"
                            :disabled="!selectedSubject"
                        >
                            <option :value="null">All Chapters</option>
                            <option
                                v-for="chapter in chapters"
                                :key="chapter.id"
                                :value="chapter.id"
                            >
                                {{ chapter.name }}
                            </option>
                        </select>
                    </div>
                </div>

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
                    v-else-if="quizzes.length === 0"
                    class="text-center py-5"
                >
                    <p>
                        No quizzes found for the selected criteria. Add a new
                        one to get started!
                    </p>
                </div>
                <div
                    v-else
                    class="table-responsive"
                >
                    <table class="table table-hover align-middle">
                        <thead>
                            <tr>
                                <th scope="col">QUIZ TITLE</th>
                                <th scope="col">SUBJECT</th>
                                <th scope="col">CHAPTER</th>
                                <th scope="col">DURATION (MIN)</th>
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
                                v-for="quiz in quizzes"
                                :key="quiz.id"
                            >
                                <td class="title">
                                    <router-link
                                        :to="`/admin/quizzes/${quiz.id}/questions`"
                                        >{{ quiz.title }}</router-link
                                    >
                                </td>
                                <td>{{ getSubjectName(quiz.subject_id) }}</td>
                                <td>{{ getChapterName(quiz.chapter_id) }}</td>
                                <td>{{ quiz.duration }}</td>
                                <td class="text-end">
                                    <div
                                        class="d-flex justify-content-end gap-2"
                                    >
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-info details"
                                            style="padding: 0.5em 1em"
                                            color="primary5"
                                            @click="openDetailsModal(quiz)"
                                        >
                                            <i class="bi bi-eye"></i>
                                        </BaseButton>
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-success edit"
                                            style="padding: 0.5em 1em"
                                            color="primary5"
                                            @click="openEditModal(quiz)"
                                        >
                                            <i class="bi bi-pencil"></i>
                                        </BaseButton>
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-danger delete"
                                            style="padding: 0.5em 1em"
                                            color="primary5"
                                            @click="deleteQuiz(quiz.id)"
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

            <BaseModal
                :show="isModalVisible"
                @close="closeModal"
            >
                <template #header>{{
                    isEditing ? "Edit Quiz" : "Add New Quiz"
                }}</template>
                <template #body>
                    <form @submit.prevent="handleQuizSubmit">
                        <div class="mb-3">
                            <label
                                for="quizSubject"
                                class="form-label fw-semibold"
                                >Subject</label
                            >
                            <select
                                id="quizSubject"
                                class="form-select"
                                v-model="currentQuiz.subject_id"
                                @change="fetchChaptersForModal"
                                required
                            >
                                <option
                                    disabled
                                    value=""
                                >
                                    Please select a subject
                                </option>
                                <option
                                    v-for="subject in subjects"
                                    :key="subject.id"
                                    :value="subject.id"
                                >
                                    {{ subject.name }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label
                                for="quizChapter"
                                class="form-label fw-semibold"
                                >Chapter</label
                            >
                            <select
                                id="quizChapter"
                                class="form-select"
                                v-model="currentQuiz.chapter_id"
                                :disabled="!currentQuiz.subject_id"
                                required
                            >
                                <option
                                    disabled
                                    value=""
                                >
                                    Please select a chapter
                                </option>
                                <option
                                    v-for="chapter in modalChapters"
                                    :key="chapter.id"
                                    :value="chapter.id"
                                >
                                    {{ chapter.name }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label
                                for="quizTitle"
                                class="form-label title fw-semibold"
                                >Quiz Title</label
                            >
                            <input
                                type="text"
                                class="form-control"
                                id="quizTitle"
                                v-model="currentQuiz.title"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="quizDuration"
                                class="form-label fw-semibold"
                                >Duration (in minutes)</label
                            >
                            <input
                                type="number"
                                class="form-control"
                                id="quizDuration"
                                v-model.number="currentQuiz.duration"
                                required
                                min="1"
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="quizDate"
                                class="form-label fw-semibold"
                                >Date of Quiz</label
                            >
                            <input
                                type="date"
                                class="form-control"
                                id="quizDate"
                                v-model="currentQuiz.date_of_quiz"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="quizTime"
                                class="form-label fw-semibold"
                                >Scheduled Time</label
                            >
                            <input
                                type="time"
                                class="form-control"
                                id="quizTime"
                                v-model="currentQuiz.scheduled_at"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="quizRemarks"
                                class="form-label fw-semibold"
                                >Remarks</label
                            >
                            <textarea
                                class="form-control"
                                id="quizRemarks"
                                rows="3"
                                v-model="currentQuiz.remarks"
                            ></textarea>
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
                        @click="handleQuizSubmit"
                        :loading="isSubmitting"
                    >
                        {{ isEditing ? "Save Changes" : "Add Quiz" }}
                    </BaseButton>
                </template>
            </BaseModal>

            <DetailsModal
                :show="isDetailsModalVisible"
                :item="detailedItem"
                title="Quiz Details"
                :fields="quizFields"
                @close="closeDetailsModal"
            />
        </div>
    </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseModal from "@/components/base/BaseModal.vue";
import DetailsModal from "@/components/admin/DetailsModal.vue";
import AdminLayout from "@/components/admin/AdminLayout.vue";

const quizzes = ref([]);
const subjects = ref([]);
const chapters = ref([]);
const modalChapters = ref([]);
const loading = ref(true);
const isModalVisible = ref(false);
const isDetailsModalVisible = ref(false);
const isEditing = ref(false);
const isSubmitting = ref(false);
const detailedItem = ref(null);
const selectedSubject = ref(null);
const selectedChapter = ref(null);

const currentQuiz = ref({
    id: null,
    title: "",
    duration: 60,
    remarks: "",
    date_of_quiz: "",
    scheduled_at: "",
    subject_id: "",
    chapter_id: "",
});

const getSubjectName = (subjectId) => {
    const subject = subjects.value.find((s) => s.id === subjectId);
    return subject ? subject.name : "N/A";
};

const getChapterName = (chapterId) => {
    const allChapters = [...chapters.value, ...modalChapters.value];
    console.log(allChapters);
    const chapter = allChapters.find((c) => c.id === chapterId);
    return chapter ? chapter.name : "N/A";
};

const quizFields = [
    { key: "id", label: "ID" },
    { key: "title", label: "Title" },
    { key: "subject_name", label: "Subject" },
    { key: "chapter_name", label: "Chapter" },
    { key: "duration", label: "Duration (min)" },
    { key: "date_of_quiz", label: "Date of Quiz", isDate: true },
    { key: "scheduled_at", label: "Scheduled At", isDate: true },
    { key: "remarks", label: "Remarks" },
    { key: "created_at", label: "Created At", isDate: true },
];

const fetchSubjects = async () => {
    try {
        const response = await api.get("/api/admin/subjects");
        subjects.value = response.data;
    } catch (error) {
        console.error("Failed to fetch subjects:", error);
    }
};

const fetchChaptersAndQuizzes = async () => {
    selectedChapter.value = null;
    await fetchChaptersForFilter();
    await fetchQuizzes();
};

const fetchChaptersForFilter = async () => {
    if (!selectedSubject.value) {
        chapters.value = [];
        return;
    }
    try {
        const response = await api.get(
            `/api/admin/subjects/${selectedSubject.value}/chapters`
        );
        chapters.value = response.data;
    } catch (error) {
        console.error("Failed to fetch chapters for filter:", error);
    }
};

const fetchChaptersForModal = async () => {
    if (!currentQuiz.value.subject_id) {
        modalChapters.value = [];
        return;
    }
    try {
        const response = await api.get(
            `/api/admin/subjects/${currentQuiz.value.subject_id}/chapters`
        );
        modalChapters.value = response.data;
    } catch (error) {
        console.error("Failed to fetch chapters for modal:", error);
    }
};

const fetchQuizzes = async () => {
    try {
        loading.value = true;
        let url = "/api/admin/quizzes";
        if (selectedSubject.value && selectedChapter.value) {
            url = `/api/admin/subjects/${selectedSubject.value}/chapters/${selectedChapter.value}/quizzes`;
        } else if (selectedSubject.value) {
            url = `/api/admin/subjects/${selectedSubject.value}/quizzes`;
        }
        const response = await api.get(url);
        quizzes.value = response.data;
    } catch (error) {
        console.error("Failed to fetch quizzes:", error);
    } finally {
        loading.value = false;
    }
};

const fetchAllChapters = async () => {
    try {
        const response = await api.get("/api/admin/chapters");
        chapters.value = response.data;
    } catch (error) {
        console.error("Failed to fetch all chapters:", error);
    }
};

onMounted(async () => {
    await fetchSubjects();
    await fetchAllChapters();
    await fetchQuizzes();
});

const openAddModal = () => {
    isEditing.value = false;
    currentQuiz.value = {
        id: null,
        title: "",
        duration: 4,
        remarks: "",
        date_of_quiz: new Date().toISOString().slice(0, 10),
        scheduled_at: new Date().toISOString().slice(11, 16),
        subject_id: "",
        chapter_id: "",
    };
    isModalVisible.value = true;
};

const openEditModal = (quiz) => {
    isEditing.value = true;
    currentQuiz.value = {
        ...quiz,
        date_of_quiz: new Date(quiz.date_of_quiz).toISOString().slice(0, 10),
        scheduled_at: new Date(quiz.scheduled_at).toISOString().slice(0, 16),
    };
    fetchChaptersForModal();
    isModalVisible.value = true;
};

const openDetailsModal = (quiz) => {
    detailedItem.value = {
        ...quiz,
        subject_name: getSubjectName(quiz.subject_id),
        chapter_name: getChapterName(quiz.chapter_id),
    };
    isDetailsModalVisible.value = true;
};

const closeModal = () => {
    isModalVisible.value = false;
};

const closeDetailsModal = () => {
    isDetailsModalVisible.value = false;
};

const handleQuizSubmit = async () => {
    isSubmitting.value = true;
    try {
        const fullDateTime = new Date(
            `${currentQuiz.value.date_of_quiz}T${currentQuiz.value.scheduled_at}`
        );
        currentQuiz.value.scheduled_at = fullDateTime.toISOString();

        if (isEditing.value) {
            await api.put(
                `/api/admin/quizzes/${currentQuiz.value.id}`,
                currentQuiz.value
            );
        } else {
            await api.post(
                `/api/admin/subjects/${currentQuiz.value.subject_id}/chapters/${currentQuiz.value.chapter_id}/quizzes`,
                currentQuiz.value
            );
        }
        await fetchQuizzes();
        closeModal();
    } catch (error) {
        console.error("Failed to save quiz:", error);
    } finally {
        isSubmitting.value = false;
    }
};

const deleteQuiz = async (id) => {
    if (confirm("Are you sure you want to delete this quiz?")) {
        try {
            await api.delete(`/api/admin/quizzes/${id}`);
            await fetchQuizzes();
        } catch (error) {
            console.error("Failed to delete quiz:", error);
        }
    }
};
</script>

<style scoped>
@import "../../assets/subjects.css";

td.title a {
    color: var(--primary);
    text-decoration: none;
}
</style>
