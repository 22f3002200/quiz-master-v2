<template>
    <UserLayout>
        <div class="container-md p-4">
            <h2
                class="mb-4 fw-bold"
                style="color: var(--primary)"
            >
                Subjects
            </h2>

            <div
                v-if="subjects.length"
                class="row g-4"
            >
                <router-link
                    :to="`/user/subjects/${subject.id}/chapters`"
                    v-for="subject in subjects"
                    :key="subject.id"
                    class="col-md-6 col-lg-4 card-box-subjects"
                    style="text-decoration: none"
                >
                    <div
                        class="border rounded overflow-hidden h-100 shadow-sm hover-shadow transition"
                    >
                        <div class="position-relative">
                            <!-- Info button -->
                            <button
                                type="button"
                                class="btn btn-sm btn-light position-absolute top-0 end-0 m-2"
                                @click.stop.prevent="openDetailsModal(subject)"
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
                                    <i
                                        class="fs-5 bi bi-journal-bookmark-fill"
                                    ></i>
                                </div>
                                <div>
                                    <h5 class="fw-semibold mb-1">
                                        {{ subject.name }}
                                    </h5>
                                    <small
                                        >{{ subject.quiz_count }} quiz<span
                                            v-if="subject.quiz_count !== 1"
                                            >zes</span
                                        >
                                        available</small
                                    >
                                </div>
                            </div>

                            <!-- Difficulty tags -->
                            <div class="mb-3 d-flex flex-wrap gap-2">
                                <span class="badge">Beginner</span>
                                <span class="badge">Intermediate</span>
                                <span class="badge">Advanced</span>
                            </div>

                            <!-- Button -->
                            <BaseButton
                                :to="`/user/quizzes/subjects/${subject.id}`"
                                class="btn btn-primary w-100"
                            >
                                Browse Quiz
                            </BaseButton>
                        </div>
                    </div>
                </router-link>
                <DetailsModal
                    :show="isDetailsModalVisible"
                    :item="detailedItem"
                    title="Subject Details"
                    :fields="subjectFields"
                    @close="closeDetailsModal"
                    class="i-button"
                />
            </div>

            <div
                v-else
                class="text-center"
            >
                <p>No subjects are available at the moment.</p>
            </div>
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import DetailsModal from "@/components/admin/DetailsModal.vue";

const subjects = ref([]);
const isDetailsModalVisible = ref(false);
const detailedItem = ref(null);

const subjectFields = [
    {
        key: "name",
        label: "Name",
    },
    {
        key: "description",
        label: "Description",
    },
];

const fetchSubjects = async () => {
    try {
        const response = await api.get("/api/admin/subjects");
        subjects.value = response.data;
    } catch (error) {
        console.error("Failed to fetch subjects:", error);
    }
};

const openDetailsModal = (subject) => {
    detailedItem.value = subject;
    isDetailsModalVisible.value = true;
};

const closeDetailsModal = () => {
    isDetailsModalVisible.value = false;
};

onMounted(fetchSubjects);
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
</style>
