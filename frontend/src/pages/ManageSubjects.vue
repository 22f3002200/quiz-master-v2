<template>
    <div class="container py-4">
        <div class="card-box p-4 rounded-3 shadow-sm">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="fw-bold mb-0">Manage Subjects</h2>
                <BaseButton @click="openAddModal">
                    <i class="bi bi-plus-lg me-2"></i>Add New Subject
                </BaseButton>
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
                <p>No subjects found. Add a new one to get started!</p>
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
                            v-for="subject in subjects"
                            :key="subject.id"
                        >
                            <td>{{ subject.name }}</td>
                            <td>{{ subject.description }}</td>
                            <td class="text-end">
                                <a
                                    href="#"
                                    class="text-primary me-3"
                                    @click.prevent="openEditModal(subject)"
                                    >Edit</a
                                >
                                <a
                                    href="#"
                                    class="text-danger"
                                    @click.prevent="deleteSubject(subject.id)"
                                    >Delete</a
                                >
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
                isEditing ? "Edit Subject" : "Add New Subject"
            }}</template>
            <template #body>
                <form @submit.prevent="handleSubjectSubmit">
                    <div class="mb-3">
                        <label
                            for="subjectName"
                            class="form-label fw-semibold"
                            >Subject Name</label
                        >
                        <input
                            type="text"
                            class="form-control"
                            id="subjectName"
                            v-model="currentSubject.name"
                            required
                        />
                    </div>
                    <div class="mb-3">
                        <label
                            for="subjectDescription"
                            class="form-label fw-semibold"
                            >Description</label
                        >
                        <textarea
                            class="form-control"
                            id="subjectDescription"
                            rows="3"
                            v-model="currentSubject.description"
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
                    @click="handleSubjectSubmit"
                    :loading="isSubmitting"
                    >{{
                        isEditing ? "Save Changes" : "Add Subject"
                    }}</BaseButton
                >
            </template>
        </BaseModal>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseModal from "@/components/base/BaseModal.vue";

const subjects = ref([]);
const loading = ref(true);
const isModalVisible = ref(false);
const isEditing = ref(false);
const isSubmitting = ref(false);
const currentSubject = ref({ id: null, name: "", description: "" });

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

const openAddModal = () => {
    isEditing.value = false;
    currentSubject.value = { id: null, name: "", description: "" };
    isModalVisible.value = true;
};

const openEditModal = (subject) => {
    isEditing.value = true;
    currentSubject.value = { ...subject };
    isModalVisible.value = true;
};

const closeModal = () => {
    isModalVisible.value = false;
};

const handleSubjectSubmit = async () => {
    isSubmitting.value = true;
    try {
        if (isEditing.value) {
            // Update existing subject
            await api.put(
                `/api/admin/subjects/${currentSubject.value.id}`,
                currentSubject.value
            );
        } else {
            // Add new subject
            await api.post("/api/admin/subjects", currentSubject.value);
        }
        await fetchSubjects(); // Refresh the list
        closeModal();
    } catch (error) {
        console.error("Failed to save subject:", error);
    } finally {
        isSubmitting.value = false;
    }
};

const deleteSubject = async (id) => {
    if (confirm("Are you sure you want to delete this subject?")) {
        try {
            await api.delete(`/api/admin/subjects/${id}`);
            await fetchSubjects(); // Refresh the list
        } catch (error) {
            console.error("Failed to delete subject:", error);
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 1000px;
}
.card-box {
    background-color: white;
    border: 1px solid var(--primary5);
}
h2 {
    color: var(--primary);
}
.table thead th {
    color: var(--accent);
    font-weight: 600;
    border-bottom: 2px solid var(--primary);
}
.table tbody td {
    color: var(--text);
}
.table-hover tbody tr:hover {
    background-color: var(--primary5);
}
a {
    text-decoration: none;
    font-weight: 500;
}
.form-control,
.form-select {
    background-color: white;
    border: 1px solid var(--secondary);
}
.form-control:focus,
.form-select:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 0.25rem var(--primary5);
}
.form-label {
    color: var(--primary);
}
</style>
