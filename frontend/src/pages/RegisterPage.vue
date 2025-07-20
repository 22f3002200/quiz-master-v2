<template>
    <div
        class="min-vh-100 d-flex align-items-center justify-content-center gradient"
    >
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-6 col-lg-5">
                    <div class="bg-white rounded shadow p-5">
                        <div class="text-center mb-4">
                            <h2 class="text-primary fw-bold mb-2">
                                QuizMaster
                            </h2>
                            <p class="text-secondary">
                                Create your account to start your quiz journey.
                            </p>
                        </div>

                        <div
                            v-if="message"
                            class="alert"
                            :class="
                                messageType === 'error'
                                    ? 'alert-danger'
                                    : 'alert-success'
                            "
                        >
                            {{ message }}
                        </div>

                        <form @submit.prevent="registerUser">
                            <div class="mb-3">
                                <label
                                    for="fullName"
                                    class="form-label fw-semibold text-dark"
                                    >Full Name</label
                                >
                                <input
                                    type="text"
                                    class="form-control"
                                    id="fullName"
                                    v-model="form.full_name"
                                    placeholder="Enter your full name"
                                    required
                                />
                            </div>
                            <div class="mb-3">
                                <label
                                    for="email"
                                    class="form-label fw-semibold text-dark"
                                    >Email Address</label
                                >
                                <input
                                    type="email"
                                    class="form-control"
                                    id="email"
                                    v-model="form.email"
                                    placeholder="Enter your email"
                                    required
                                />
                            </div>
                            <div class="mb-3">
                                <label
                                    for="qualification"
                                    class="form-label fw-semibold text-dark"
                                    >Qualification</label
                                >
                                <input
                                    type="text"
                                    class="form-control"
                                    id="qualification"
                                    v-model="form.qualification"
                                    placeholder="Your highest qualification"
                                />
                            </div>
                            <div class="mb-3">
                                <label
                                    for="dob"
                                    class="form-label fw-semibold text-dark"
                                    >Date of Birth</label
                                >
                                <input
                                    type="date"
                                    class="form-control"
                                    id="dob"
                                    v-model="form.dob"
                                />
                            </div>
                            <div class="mb-4">
                                <label
                                    for="password"
                                    class="form-label fw-semibold text-dark"
                                    >Password</label
                                >
                                <input
                                    type="password"
                                    class="form-control"
                                    id="password"
                                    v-model="form.password"
                                    placeholder="Create a secure password"
                                    required
                                />
                            </div>
                            <button
                                type="submit"
                                class="btn btn-primary w-100 py-2 fw-semibold gradient-btn"
                                :disabled="loading"
                            >
                                <span
                                    v-if="loading"
                                    class="spinner-border spinner-border-sm me-2"
                                ></span>
                                Create Account
                            </button>
                        </form>

                        <div class="text-center mt-4">
                            <p class="text-secondary">
                                Already have an account?
                                <router-link
                                    to="/login"
                                    class="text-primary text-decoration-none fw-semibold hover-text-primary"
                                >
                                    Sign In
                                </router-link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from "../utils/api";

export default {
    data() {
        return {
            loading: false,
            message: "",
            messageType: "",
            form: {
                full_name: "",
                email: "",
                password: "",
                qualification: "",
                dob: "",
            },
        };
    },
    methods: {
        async registerUser() {
            this.loading = true;
            this.message = "";
            try {
                const res = await api.post("/api/auth/register", this.form);
                localStorage.setItem("access_token", res.data.access_token);
                this.$router.push("/"); // Redirect to home or a profile page
                this.message = "Registration successful!";
                this.messageType = "success";
            } catch (err) {
                this.message = err.response?.data?.msg || "Registration failed";
                this.messageType = "error";
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>

<style scoped>
.gradient {
    background: linear-gradient(
        90deg,
        rgba(42, 123, 155, 1) 0%,
        rgba(87, 100, 199, 1) 50%,
        rgba(83, 152, 237, 1) 100%
    );
}

.gradient-btn {
    background: linear-gradient(
        90deg,
        rgba(42, 123, 155, 1) 0%,
        rgba(87, 100, 199, 1) 50%,
        rgba(83, 152, 237, 1) 100%
    );
    border: none;
    transition: transform 0.2s ease;
}

.gradient-btn:hover {
    transform: translateY(-1px);
}

.hover-text-primary:hover {
    text-decoration: underline !important;
}
</style>
