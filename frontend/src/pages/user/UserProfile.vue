<template>
    <UserLayout>
        <div class="container py-4">
            <div class="card-box p-4 rounded-3 shadow-lg">
                <h2 class="fw-bold mb-4">My Profile</h2>
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
                    v-else-if="user"
                    class="table-responsive"
                >
                    <table class="table table-hover align-middle">
                        <tbody>
                            <tr>
                                <th scope="row">Full Name</th>
                                <td>{{ user.full_name }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Email</th>
                                <td>{{ user.email }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Qualification</th>
                                <td>{{ user.qualification }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Date of Birth</th>
                                <td>
                                    {{
                                        new Date(user.dob).toLocaleDateString()
                                    }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div
                    v-else
                    class="text-center py-5"
                >
                    <p>Could not retrieve user profile.</p>
                </div>
            </div>
        </div>
    </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/api";
import UserLayout from "@/components/user/UserLayout.vue";

const user = ref(null);
const loading = ref(true);

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

onMounted(fetchUserProfile);
</script>

<style scoped>
@import "../../assets/subjects.css";
</style>
