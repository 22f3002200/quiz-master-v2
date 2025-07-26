<template>
    <AdminLayout>
        <div class="container py-4">
            <div class="card-box p-4 rounded-3">
                <div
                    class="d-flex justify-content-between align-items-center mb-4"
                >
                    <h2 class="fw-bold mb-0">Users</h2>
                    <BaseButton
                        @click="openAddModal"
                        class="btn-primary"
                    >
                        <i class="bi bi-plus-lg me-2"></i>Add New User
                    </BaseButton>
                </div>

                <div
                    v-if="loading"
                    class="text-center"
                >
                    <div
                        class="spinner-border"
                        role="status"
                    >
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div
                    v-else-if="users.length === 0"
                    class="text-center py-5"
                >
                    <p>No users found. Add a new one to get started!</p>
                </div>
                <div
                    v-else
                    class="table-responsive"
                >
                    <table class="table table-hover align-middle">
                        <thead>
                            <tr>
                                <th scope="col">NAME</th>
                                <th scope="col">EMAIL</th>
                                <th scope="col">QUALIFICATION</th>
                                <th scope="col">ACTIVE</th>
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
                                v-for="user in users"
                                :key="user.id"
                            >
                                <td>{{ user.full_name }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ user.qualification }}</td>
                                <td>
                                    <span
                                        :class="[
                                            'badge',
                                            user.active
                                                ? 'bg-success'
                                                : 'bg-danger',
                                        ]"
                                        >{{ user.active ? "Yes" : "No" }}</span
                                    >
                                </td>
                                <td class="text-end">
                                    <div
                                        class="d-flex justify-content-end gap-2"
                                    >
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-info details"
                                            style="padding: 0.5em 1em"
                                            color="primary5"
                                            @click="openDetailsModal(user)"
                                        >
                                            <i class="bi bi-eye"></i>
                                        </BaseButton>
                                        <BaseButton
                                            size="sm"
                                            class="btn-outline-success edit"
                                            style="padding: 0.5em 1em"
                                            color="primary5"
                                            @click="openEditModal(user)"
                                        >
                                            <i class="bi bi-pencil"></i>
                                        </BaseButton>
                                        <BaseButton
                                            size="sm"
                                            style="padding: 0.5em 1em"
                                            class="btn-outline-danger delete"
                                            color="primary5"
                                            @click="deleteUser(user.id)"
                                            ><i class="bi bi-trash"></i>
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
                    isEditing ? "Edit User" : "Add New User"
                }}</template>
                <template #body>
                    <form @submit.prevent="handleUserSubmit">
                        <div class="mb-3">
                            <label
                                for="userName"
                                class="form-label fw-semibold"
                                >Full Name</label
                            >
                            <input
                                type="text"
                                class="form-control"
                                id="userName"
                                v-model="currentUser.full_name"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="userEmail"
                                class="form-label fw-semibold"
                                >Email</label
                            >
                            <input
                                type="email"
                                class="form-control"
                                id="userEmail"
                                v-model="currentUser.email"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="userQualification"
                                class="form-label fw-semibold"
                                >Qualification</label
                            >
                            <input
                                type="text"
                                class="form-control"
                                id="userQualification"
                                v-model="currentUser.qualification"
                            />
                        </div>
                        <div class="form-check mb-3">
                            <input
                                class="form-check-input"
                                type="checkbox"
                                id="userActive"
                                v-model="currentUser.active"
                            />
                            <label
                                class="form-check-label"
                                for="userActive"
                            >
                                Active
                            </label>
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
                        @click="handleUserSubmit"
                        :loading="isSubmitting"
                        >{{
                            isEditing ? "Save Changes" : "Add User"
                        }}</BaseButton
                    >
                </template>
            </BaseModal>
            <DetailsModal
                :show="isDetailsModalVisible"
                :item="detailedItem"
                title="User Details"
                :fields="userFields"
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
import AdminLayout from "@/components/admin/AdminLayout.vue";
import DetailsModal from "@/components/admin/DetailsModal.vue";

const users = ref([]);
const loading = ref(true);
const isModalVisible = ref(false);
const isDetailsModalVisible = ref(false);
const isEditing = ref(false);
const isSubmitting = ref(false);
const currentUser = ref({
    id: null,
    full_name: "",
    email: "",
    qualification: "",
    active: true,
});
const detailedItem = ref(null);

const userFields = [
    { key: "id", label: "ID" },
    { key: "full_name", label: "Full Name" },
    { key: "email", label: "Email" },
    { key: "qualification", label: "Qualification" },
    { key: "active", label: "Active" },
    { key: "created_at", label: "Created At", isDate: true },
];

const fetchUsers = async () => {
    try {
        loading.value = true;
        const response = await api.get("/api/admin/users");
        users.value = response.data;
    } catch (error) {
        console.error("Failed to fetch users:", error);
    } finally {
        loading.value = false;
    }
};

onMounted(fetchUsers);

const openAddModal = () => {
    isEditing.value = false;
    currentUser.value = {
        id: null,
        full_name: "",
        email: "",
        qualification: "",
        active: true,
    };
    isModalVisible.value = true;
};

const openEditModal = (user) => {
    isEditing.value = true;
    currentUser.value = { ...user };
    isModalVisible.value = true;
};

const openDetailsModal = (user) => {
    detailedItem.value = user;
    isDetailsModalVisible.value = true;
};

const closeModal = () => {
    isModalVisible.value = false;
};

const closeDetailsModal = () => {
    isDetailsModalVisible.value = false;
};

const handleUserSubmit = async () => {
    isSubmitting.value = true;
    try {
        if (isEditing.value) {
            // Update existing user
            await api.put(
                `/api/admin/users/${currentUser.value.id}`,
                currentUser.value
            );
        } else {
            // Add new user
            await api.post("/api/admin/users", currentUser.value);
        }
        await fetchUsers(); // Refresh the list
        closeModal();
    } catch (error) {
        console.error("Failed to save user:", error);
    } finally {
        isSubmitting.value = false;
    }
};

const deleteUser = async (id) => {
    if (confirm("Are you sure you want to delete this user?")) {
        try {
            await api.delete(`/api/admin/users/${id}`);
            await fetchUsers(); // Refresh the list
        } catch (error) {
            console.error("Failed to delete user:", error);
        }
    }
};
</script>

<style scoped>
@import "../../assets/subjects.css";
</style>
