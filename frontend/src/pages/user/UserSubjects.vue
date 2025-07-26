<template>
    <UserLayout>
        <div class="container-xxl p-4">
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
                <div
                    v-for="subject in subjects"
                    :key="subject.id"
                    class="col-md-6 col-lg-4"
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

                            <!-- Difficulty tags (optional placeholder) -->
                            <div class="mb-3 d-flex flex-wrap gap-2">
                                <span class="badge">Beginner</span>
                                <span class="badge">Intermediate</span>
                                <span class="badge">Advanced</span>
                            </div>

                            <!-- Button -->
                            <router-link
                                :to="`/user/quizzes/subject/${subject.id}`"
                                class="btn w-100"
                            >
                                View Quizzes
                            </router-link>
                        </div>
                    </div>
                </div>
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

const subjects = ref([]);

const fetchSubjects = async () => {
    try {
        const response = await api.get("/api/admin/subjects");
        subjects.value = response.data;
    } catch (error) {
        console.error("Failed to fetch subjects:", error);
    }
};

onMounted(fetchSubjects);
</script>

<style scoped>
/* Reuse the design styles */
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
    background-color: var(--primary);
    color: var(--background);
}

.btn:hover {
    background-color: var(--primary);
    color: var(--background);
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

.container-xxl {
    margin-left: 15px;
}
</style>
