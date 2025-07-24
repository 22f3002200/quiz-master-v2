<template>
    <AdminLayout>
        <div class="container py-4">
            <div class="card-box p-4 rounded-3 shadow-lg">
                <div
                    class="d-flex justify-content-between align-items-center mb-4"
                >
                    <h2 class="fw-bold mb-0">Chapters</h2>
                    <BaseButton @click="openAddModal">
                        <i class="bi bi-plus-lg me-2"></i>Add New Chapter
                    </BaseButton>
                </div>

                <div class="mb-3">
                    <label
                        for="subjectFilter"
                        class="form-label fw-semibold"
                        >Filter by Subject</label
                    >
                    <select
                        id="subjectFilter"
                        class="form-select"
                        v-model="selectedSubject"
                        @change="fetchChapters"
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
                    v-else-if="chapters.length === 0"
                    class="text-center py-5"
                >
                    <p>
                        No chapters found for the selected subject. Add a new
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
                                <th scope="col">CHAPTER NAME</th>
                                <th scope="col">DESCRIPTION</th>
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
                                v-for="chapter in chapters"
                                :key="chapter.id"
                            >
                                <td>{{ chapter.name }}</td>
                                <td>{{ chapter.description }}</td>
                                <td class="text-end">
                                    <div
                                        class="d-flex justify-content-end gap-2"
                                    >
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-info details"
                                            style="padding: 0.5em 1em"
                                            color="primary5"
                                            @click="openDetailsModal(chapter)"
                                        >
                                            <i class="bi bi-eye"></i>
                                        </BaseButton>
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-success edit"
                                            style="padding: 0.5em 1em"
                                            color="primary5"
                                            @click="openEditModal(chapter)"
                                        >
                                            <i class="bi bi-pencil"></i>
                                        </BaseButton>
                                        <BaseButton
                                            size="sm"
                                            style="padding: 0.5em 1em"
                                            class="btn-outline-danger delete"
                                            color="primary5"
                                            @click="deleteChapter(chapter.id)"
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
                    isEditing ? "Edit Chapter" : "Add New Chapter"
                }}</template>
                <template #body>
                    <form @submit.prevent="handleChapterSubmit">
                        <div class="mb-3">
                            <label
                                for="chapterSubject"
                                class="form-label fw-semibold"
                                >Subject</label
                            >
                            <select
                                id="chapterSubject"
                                class="form-select"
                                v-model="currentChapter.subject_id"
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
                                for="chapterName"
                                class="form-label fw-semibold"
                                >Chapter Name</label
                            >
                            <input
                                type="text"
                                class="form-control"
                                id="chapterName"
                                v-model="currentChapter.name"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="chapterDescription"
                                class="form-label fw-semibold"
                                >Description</label
                            >
                            <textarea
                                class="form-control"
                                id="chapterDescription"
                                rows="3"
                                v-model="currentChapter.description"
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
                        @click="handleChapterSubmit"
                        :loading="isSubmitting"
                    >
                        {{ isEditing ? "Save Changes" : "Add Chapter" }}
                    </BaseButton>
                </template>
            </BaseModal>

            <ChapterDetailsModal
                :show="isDetailsModalVisible"
                :chapter="detailedChapter"
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
import ChapterDetailsModal from "@/components/admin/ChapterDetailsModal.vue";
import AdminLayout from "@/components/admin/AdminLayout.vue";

const chapters = ref([]);
const subjects = ref([]);
const loading = ref(true);
const isModalVisible = ref(false);
const isDetailsModalVisible = ref(false);
const isEditing = ref(false);
const isSubmitting = ref(false);
const currentChapter = ref({
    id: null,
    name: "",
    description: "",
    subject_id: "",
});
const detailedChapter = ref(null);
const selectedSubject = ref(null);

const fetchSubjects = async () => {
    try {
        const response = await api.get("/api/admin/subjects");
        subjects.value = response.data;
    } catch (error) {
        console.error("Failed to fetch subjects:", error);
    }
};

const fetchChapters = async () => {
    try {
        loading.value = true;
        let url = "/api/admin/chapters";
        if (selectedSubject.value) {
            url = `/api/admin/subjects/${selectedSubject.value}/chapters`;
        }
        const response = await api.get(url);
        chapters.value = response.data;
    } catch (error) {
        console.error("Failed to fetch chapters:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(async () => {
    await fetchSubjects();
    await fetchChapters();
});

const openAddModal = () => {
    isEditing.value = false;
    currentChapter.value = {
        id: null,
        name: "",
        description: "",
        subject_id: "",
    };
    isModalVisible.value = true;
};

const openEditModal = (chapter) => {
    isEditing.value = true;
    currentChapter.value = { ...chapter };
    isModalVisible.value = true;
};

const openDetailsModal = (chapter) => {
    detailedChapter.value = chapter;
    isDetailsModalVisible.value = true;
};

const closeModal = () => {
    isModalVisible.value = false;
};

const closeDetailsModal = () => {
    isDetailsModalVisible.value = false;
};

const handleChapterSubmit = async () => {
    isSubmitting.value = true;
    try {
        if (isEditing.value) {
            await api.put(
                `/api/admin/chapters/${currentChapter.value.id}`,
                currentChapter.value
            );
        } else {
            await api.post(
                `/api/admin/subjects/${currentChapter.value.subject_id}/chapters`,
                currentChapter.value
            );
        }
        await fetchChapters();
        closeModal();
    } catch (error) {
        console.error("Failed to save chapter:", error);
    } finally {
        isSubmitting.value = false;
    }
};

const deleteChapter = async (id) => {
    if (confirm("Are you sure you want to delete this chapter?")) {
        try {
            await api.delete(`/api/admin/chapters/${id}`);
            await fetchChapters();
        } catch (error) {
            console.error("Failed to delete chapter:", error);
        }
    }
};
</script>

<style scoped>
@import "../../assets/subjects.css";
.btn-outline-info.details {
    border-color: #0dcaf0;
}
.btn-outline-info.details:hover {
    background-color: #0dcaf0;
}
i.bi-eye {
    color: #0dcaf0;
}
.btn-outline-info.details:hover i.bi-eye {
    color: var(--background);
}
</style>
