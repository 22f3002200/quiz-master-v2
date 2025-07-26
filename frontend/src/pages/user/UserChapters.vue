<template>
    <UserLayout>
        <div class="container py-4">
            <div class="card-box p-4 rounded-3">
                <h2 class="fw-bold mb-4">Explore Chapters</h2>

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
                    <p>No chapters found for the selected subject.</p>
                </div>
                <div
                    v-else
                    class="table-responsive"
                >
                    <table class="table table-hover align-middle">
                        <thead>
                            <tr>
                                <th scope="col">CHAPTER</th>
                                <th scope="col">SUBJECT</th>
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
                                <td>
                                    {{ getSubjectName(chapter.subject_id) }}
                                </td>
                                <td class="text-end">
                                    <BaseButton
                                        size="sm"
                                        class="btn-outline-info details"
                                        style="padding: 0.5em 1em"
                                        color="primary5"
                                        @click="openDetailsModal(chapter)"
                                    >
                                        <i class="bi bi-eye"></i>
                                    </BaseButton>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <DetailsModal
                :show="isDetailsModalVisible"
                :item="detailedItem"
                title="Chapter Details"
                :fields="chapterFields"
                @close="closeDetailsModal"
            />
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import DetailsModal from "@/components/admin/DetailsModal.vue";

const chapters = ref([]);
const subjects = ref([]);
const loading = ref(true);
const isDetailsModalVisible = ref(false);
const detailedItem = ref(null);
const selectedSubject = ref(null);

const getSubjectName = (subjectId) => {
    const subject = subjects.value.find((s) => s.id === subjectId);
    return subject ? subject.name : "N/A";
};

const chapterFields = [
    { key: "subject_name", label: "Subject Name" },
    { key: "name", label: "Chapter Name" },
    { key: "description", label: "Description" },
];

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

const openDetailsModal = (chapter) => {
    detailedItem.value = {
        ...chapter,
        subject_name: getSubjectName(chapter.subject_id),
    };
    isDetailsModalVisible.value = true;
};

const closeDetailsModal = () => {
    isDetailsModalVisible.value = false;
};
</script>

<style scoped>
@import "../../assets/subjects.css";
</style>
