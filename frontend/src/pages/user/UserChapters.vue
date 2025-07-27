<template>
    <UserLayout>
        <div class="container-md p-4">
            <h2
                class="mb-4 fw-bold"
                style="color: var(--primary)"
            >
                Chapters
            </h2>

            <!-- Filter Dropdown -->
            <div class="mb-4 dropdown">
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

            <!-- Cards -->
            <div
                v-if="loading"
                class="text-center py-5 chapters-card"
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
                class="row g-4"
            >
                <div
                    v-for="chapter in chapters"
                    :key="chapter.id"
                    class="col-md-6 col-lg-4 card-box-subjects"
                >
                    <div
                        class="border rounded overflow-hidden h-100 shadow-sm hover-shadow transition"
                    >
                        <div class="position-relative">
                            <!-- Info button -->
                            <button
                                type="button"
                                class="btn btn-sm btn-light position-absolute top-0 end-0 m-2"
                                @click.stop.prevent="openDetailsModal(chapter)"
                                title="View Subject Details"
                            >
                                <i class="bi bi-info-circle text-primary"></i>
                            </button>
                        </div>

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
                                    <i class="fs-5 bi bi-journal-richtext"></i>
                                </div>
                                <div>
                                    <h5 class="fw-semibold mb-1">
                                        {{ chapter.name }}
                                    </h5>
                                    <small>{{
                                        getSubjectName(chapter.subject_id)
                                    }}</small>
                                </div>
                            </div>

                            <!-- Description -->
                            <p class="mb-3 text-truncate">
                                {{ chapter.description }}
                            </p>

                            <!-- Button -->
                            <BaseButton
                                :to="`/user/subjects/${chapter.subject_id}/chapters/${chapter.id}/quizzes`"
                                size="sm"
                                class="btn btn-primary w-100"
                            >
                                Browse Quiz
                            </BaseButton>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Modal -->
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

p {
    color: var(--text);
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
    /* box-shadow: 0 20px 80px -10px var(--text); */
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

div.dropdown {
    width: fit-content;
}
</style>
