<template>
    <UserLayout>
        <div class="container py-5">
            <div class="card shadow-sm border-0 rounded-4 p-4">
                <div
                    class="d-flex justify-content-between align-items-center mb-4"
                >
                    <h2 class="fw-bold text-center mb-0">
                        <i class="bi bi-person-circle me-2"></i>My Profile
                    </h2>
                </div>

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

                <div v-else-if="user">
                    <div class="row mb-3">
                        <div class="col-md-6 mb-3">
                            <label class="text-muted text-uppercase small"
                                >Full Name</label
                            >
                            <div
                                class="fw-semibold fs-5 d-flex align-items-center"
                            >
                                {{ user.full_name }}
                                <i
                                    class="bi bi-pencil ms-2 text-primary-light"
                                    @click="openEditModal"
                                ></i>
                            </div>
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="text-muted text-uppercase small"
                                >Email</label
                            >
                            <div class="fw-semibold fs-5">{{ user.email }}</div>
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="text-muted text-uppercase small"
                                >Qualification</label
                            >
                            <div
                                class="fw-semibold fs-5 d-flex align-items-center"
                            >
                                {{ user.qualification }}
                                <i
                                    class="bi bi-pencil ms-2 text-primary-light"
                                    @click="openEditModal"
                                ></i>
                            </div>
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="text-muted text-uppercase small"
                                >Date of Birth</label
                            >
                            <div
                                class="fw-semibold fs-5 d-flex align-items-center"
                            >
                                {{ new Date(user.dob).toLocaleDateString() }}
                                <i
                                    class="bi bi-pencil ms-2 text-primary-light"
                                    @click="openEditModal"
                                ></i>
                            </div>
                        </div>
                    </div>
                </div>

                <div
                    v-else
                    class="text-center py-5 text-danger"
                >
                    <i class="bi bi-exclamation-circle fs-1 mb-2"></i>
                    <p class="mb-0">Could not retrieve user profile.</p>
                </div>
            </div>
        </div>

        <div
            class="modal fade"
            id="editProfileModal"
            tabindex="-1"
            aria-labelledby="editProfileModalLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5
                            class="modal-title"
                            id="editProfileModalLabel"
                        >
                            Edit Profile
                        </h5>
                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                        ></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="updateUserProfile">
                            <div class="mb-3">
                                <label
                                    for="fullName"
                                    class="form-label"
                                    >Full Name</label
                                >
                                <input
                                    type="text"
                                    class="form-control"
                                    id="fullName"
                                    v-model="editableUser.full_name"
                                />
                            </div>
                            <div class="mb-3">
                                <label
                                    for="qualification"
                                    class="form-label"
                                    >Qualification</label
                                >
                                <input
                                    type="text"
                                    class="form-control"
                                    id="qualification"
                                    v-model="editableUser.qualification"
                                />
                            </div>
                            <div class="mb-3">
                                <label
                                    for="dob"
                                    class="form-label"
                                    >Date of Birth</label
                                >
                                <input
                                    type="date"
                                    class="form-control"
                                    id="dob"
                                    v-model="editableUser.dob"
                                />
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                        >
                            Close
                        </button>
                        <button
                            type="button"
                            class="btn btn-primary"
                            @click="updateUserProfile"
                        >
                            Save changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";
import { Modal } from "bootstrap";

const user = ref(null);
const editableUser = ref({
    full_name: "",
    qualification: "",
    dob: "",
});
const loading = ref(true);
let editModal = null;

const fetchUserProfile = async () => {
    try {
        loading.value = true;
        const response = await api.get("/api/auth/profile");
        user.value = response.data.user;
    } catch (error) {
        console.error("Failed to fetch user profile:", error);
    } finally {
        loading.value = false;
    }
};

const openEditModal = () => {
    if (user.value) {
        editableUser.value.full_name = user.value.full_name;
        editableUser.value.qualification = user.value.qualification;
        // Format date for the input field
        editableUser.value.dob = new Date(user.value.dob)
            .toISOString()
            .split("T")[0];
    }
    editModal.show();
};

const updateUserProfile = async () => {
    try {
        const response = await api.put("/api/auth/profile", editableUser.value);
        user.value = response.data.user;
        editModal.hide();
    } catch (error) {
        console.error("Failed to update profile:", error);
        // Handle error display to the user
    }
};

onMounted(() => {
    fetchUserProfile();
    editModal = new Modal(document.getElementById("editProfileModal"));
});
</script>

<style scoped>
@import "../../assets/subjects.css";

.card {
    background-color: var(--static);
}

h2,
i {
    color: var(--primary);
}

label {
    font-weight: 600;
}

.text-primary-light {
    color: var(--primary-light);
    cursor: pointer;
    transition: color 0.2s ease-in-out;
}

.text-primary-light:hover {
    color: var(--primary);
}
</style>
