<template>
    <div class="container py-4">
        <div class="card-box p-4 rounded-3">
            <div class="d-flex align-items-center mb-4">
                <h2 class="fw-bold mb-0">Available Subjects</h2>
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
                v-else-if="subjects.length === 0"
                class="text-center py-5"
            >
                <p>No subjects are available at the moment.</p>
            </div>

            <div
                v-else
                class="table-responsive"
            >
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th scope="col">SUBJECT NAME</th>
                            <th scope="col">DESCRIPTION</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="subject in subjects"
                            :key="subject.id"
                        >
                            <td>{{ subject.name }}</td>
                            <td>{{ subject.description }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";

const subjects = ref([]);
const loading = ref(true);

const fetchSubjects = async () => {
    try {
        loading.value = true;

        const response = await api.get("/api/admin/subjects");
        subjects.value = response.data;
    } catch (error) {
        console.error("Failed to fetch subjects:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(fetchSubjects);
</script>

<style scoped>
@import "../../assets/subjects.css";
</style>
