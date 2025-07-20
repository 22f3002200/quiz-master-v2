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
                                Welcome back! Please sign in to your account.
                            </p>
                        </div>

                        <div
                            v-if="message"
                            :class="[
                                'alert',
                                messageType === 'error'
                                    ? 'alert-danger'
                                    : 'alert-success',
                            ]"
                        >
                            {{ message }}
                        </div>

                        <form @submit.prevent="login">
                            <div class="mb-3">
                                <label
                                    for="email"
                                    class="form-label fw-semibold text-dark"
                                >
                                    Email Address
                                </label>
                                <input
                                    type="email"
                                    class="form-control form-control-lg"
                                    id="email"
                                    v-model="loginForm.email"
                                    placeholder="Enter your email"
                                    required
                                />
                            </div>
                            <div class="mb-4">
                                <label
                                    for="password"
                                    class="form-label fw-semibold text-dark"
                                >
                                    Password
                                </label>
                                <input
                                    type="password"
                                    class="form-control form-control-lg"
                                    id="password"
                                    v-model="loginForm.password"
                                    placeholder="Enter your password"
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
                                Sign In
                            </button>
                        </form>

                        <div class="text-center mt-4">
                            <p class="text-secondary">
                                Don't have an account?
                                <router-link
                                    to="/register"
                                    class="text-primary text-decoration-none fw-semibold hover-text-primary"
                                >
                                    Create Account
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
    name: "LoginPage",
    data() {
        return {
            loading: false,
            message: "",
            messageType: "",
            loginForm: {
                email: "",
                password: "",
            },
        };
    },
    methods: {
        async login() {
            this.loading = true;
            this.message = "";

            try {
                const response = await api.post(
                    "/api/auth/login",
                    this.loginForm
                );

                // Store token
                localStorage.setItem(
                    "access_token",
                    response.data.access_token
                );

                this.message = "Login successful!";
                this.messageType = "success";

                const user = response.data.user;
                const isAdmin =
                    user && user.roles && user.roles.includes("admin");

                const redirectPath = isAdmin ? "/admin/dashboard" : "/";

                // Redirect to homepage after a short delay
                setTimeout(() => {
                    this.$router.push(redirectPath);
                }, 1000);
            } catch (error) {
                this.message = error.response?.data?.msg || "Login failed";
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

.form-control:focus {
    border-color: rgba(87, 100, 199, 0.5);
    box-shadow: 0 0 0 0.2rem rgba(87, 100, 199, 0.25);
}
</style>
