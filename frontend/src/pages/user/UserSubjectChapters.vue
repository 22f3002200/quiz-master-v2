<template>
    <UserLayout>
        <div class="container-md p-4">
            <h2
                class="mb-4 fw-bold"
                style="color: var(--primary)"
            >
                Chapters in {{ subjectName }}
            </h2>

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
                v-else-if="chapters.length === 0"
                class="text-center py-5"
            >
                <p>No chapters found under this subject.</p>
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
                                </div>
                            </div>

                            <!-- Description -->
                            <p class="mb-3 text-truncate">
                                {{ chapter.description }}
                            </p>

                            <!-- Button -->
                            <BaseButton
                                size="sm"
                                class="btn btn-primary w-100"
                                @click="openDetailsModal(chapter)"
                            >
                                View Details
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
import { useRoute } from "vue-router";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import DetailsModal from "@/components/admin/DetailsModal.vue";

const chapters = ref([]);
const loading = ref(true);
const subjectName = ref("Subject");
const isDetailsModalVisible = ref(false);
const detailedItem = ref(null);

const chapterFields = [
    { key: "name", label: "Chapter Name" },
    { key: "description", label: "Description" },
];

const route = useRoute();
const subjectId = parseInt(route.params.subjectId);

const fetchChapters = async () => {
    try {
        loading.value = true;
        const response = await api.get(
            `/api/admin/subjects/${subjectId}/chapters`
        );
        chapters.value = response.data;
    } catch (error) {
        console.error("Failed to fetch chapters:", error);
    } finally {
        loading.value = false;
    }
};

const fetchSubjectName = async () => {
    try {
        const response = await api.get("/api/admin/subjects");
        const subject = response.data.find((s) => s.id === subjectId);
        subjectName.value = subject ? subject.name : "Unknown Subject";
    } catch (err) {
        console.error("Error fetching subject name", err);
    }
};

const openDetailsModal = (chapter) => {
    detailedItem.value = chapter;
    isDetailsModalVisible.value = true;
};

const closeDetailsModal = () => {
    isDetailsModalVisible.value = false;
};

onMounted(async () => {
    await fetchSubjectName();
    await fetchChapters();
});
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

p,
small {
    color: var(--text);
}

.btn {
    background-color: var(--primary);
    color: var(--background);
}

.btn:hover {
    transform: translate(0, -3px);
    box-shadow: 0 20px 80px -10px var(--text);
}

i {
    color: var(--primary);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
