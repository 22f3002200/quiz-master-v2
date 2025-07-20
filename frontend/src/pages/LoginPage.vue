<template>
    <div class="auth-container">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6 col-lg-5">
                    <div class="auth-card p-4">
                        <div class="brand-logo">
                            <i class="fas fa-shield-alt"></i> SecureApp
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

                        <div v-if="currentView === 'login'">
                            <h4 class="text-center mb-4">Welcome Back</h4>
                            <form @submit.prevent="login">
                                <div class="mb-3">
                                    <label
                                        for="email"
                                        class="form-label"
                                        >Email</label
                                    >
                                    <input
                                        type="email"
                                        class="form-control"
                                        id="email"
                                        v-model="loginForm.email"
                                        required
                                    />
                                </div>
                                <div class="mb-3">
                                    <label
                                        for="password"
                                        class="form-label"
                                        >Password</label
                                    >
                                    <input
                                        type="password"
                                        class="form-control"
                                        id="password"
                                        v-model="loginForm.password"
                                        required
                                    />
                                </div>
                                <button
                                    type="submit"
                                    class="btn btn-primary w-100"
                                    :disabled="loading"
                                >
                                    <span
                                        v-if="loading"
                                        class="spinner-border spinner-border-sm me-2"
                                    ></span>
                                    Sign In
                                </button>
                            </form>
                            <div class="text-center mt-3">
                                <p>
                                    Don't have an account?
                                    <a
                                        href="#"
                                        @click="currentView = 'register'"
                                        class="text-primary"
                                        >Sign up</a
                                    >
                                </p>
                            </div>
                        </div>

                        <div v-if="currentView === 'register'">
                            <h4 class="text-center mb-4">Create Account</h4>
                            <form @submit.prevent="register">
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
                                        v-model="registerForm.full_name"
                                        required
                                    />
                                </div>
                                <div class="mb-3">
                                    <label
                                        for="email"
                                        class="form-label"
                                        >Email</label
                                    >
                                    <input
                                        type="email"
                                        class="form-control"
                                        id="email"
                                        v-model="registerForm.email"
                                        required
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
                                        v-model="registerForm.qualification"
                                        required
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
                                        v-model="registerForm.dob"
                                        required
                                    />
                                </div>
                                <div class="mb-3">
                                    <label
                                        for="password"
                                        class="form-label"
                                        >Password</label
                                    >
                                    <input
                                        type="password"
                                        class="form-control"
                                        id="password"
                                        v-model="registerForm.password"
                                        required
                                    />
                                </div>
                                <button
                                    type="submit"
                                    class="btn btn-primary w-100"
                                    :disabled="loading"
                                >
                                    <span
                                        v-if="loading"
                                        class="spinner-border spinner-border-sm me-2"
                                    ></span>
                                    Create Account
                                </button>
                            </form>
                            <div class="text-center mt-3">
                                <p>
                                    Already have an account?
                                    <a
                                        href="#"
                                        @click="currentView = 'login'"
                                        class="text-primary"
                                        >Sign in</a
                                    >
                                </p>
                            </div>
                        </div>

                        <div v-if="currentView === 'dashboard'">
                            <h4 class="text-center mb-4">Dashboard</h4>
                            <div class="text-center">
                                <p>Welcome, {{ user.full_name }}!</p>
                                <p>Email: {{ user.email }}</p>
                                <button
                                    @click="logout"
                                    class="btn btn-outline-danger"
                                >
                                    Logout
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "LandingPage",
    data() {
        return {
            currentView: "login", // 'login', 'register', 'dashboard'
            loading: false,
            message: "",
            messageType: "",
            user: null,
            loginForm: {
                email: "",
                password: "",
            },
            registerForm: {
                full_name: "",
                email: "",
                qualification: "",
                dob: "",
                password: "",
            },
        };
    },
    mounted() {
        // Check if user is already logged in
        const token = localStorage.getItem("access_token");
        if (token) {
            this.getProfile();
        }
    },
    methods: {
        async login() {
            this.loading = true;
            this.message = "";

            try {
                const response = await axios.post(
                    "http://localhost:5000/auth/login",
                    this.loginForm
                );

                // Store tokens
                localStorage.setItem(
                    "access_token",
                    response.data.access_token
                );
                localStorage.setItem(
                    "refresh_token",
                    response.data.refresh_token
                );

                this.user = response.data.user;
                this.currentView = "dashboard";
                this.message = "Login successful!";
                this.messageType = "success";
            } catch (error) {
                this.message = error.response?.data?.msg || "Login failed";
                this.messageType = "error";
            } finally {
                this.loading = false;
            }
        },

        async register() {
            this.loading = true;
            this.message = "";

            try {
                const response = await axios.post(
                    "http://localhost:5000/auth/register",
                    this.registerForm
                );

                // Store tokens
                localStorage.setItem(
                    "access_token",
                    response.data.access_token
                );
                localStorage.setItem(
                    "refresh_token",
                    response.data.refresh_token
                );

                this.user = response.data.user;
                this.currentView = "dashboard";
                this.message = "Registration successful!";
                this.messageType = "success";
            } catch (error) {
                this.message =
                    error.response?.data?.msg || "Registration failed";
                this.messageType = "error";
            } finally {
                this.loading = false;
            }
        },

        async getProfile() {
            try {
                const token = localStorage.getItem("access_token");
                const response = await axios.get(
                    "http://localhost:5000/auth/profile",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                this.user = response.data.user;
                this.currentView = "dashboard";
            } catch (error) {
                // Token might be expired, clear it
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                this.currentView = "login";
            }
        },

        logout() {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            this.user = null;
            this.currentView = "login";
            this.message = "Logged out successfully";
            this.messageType = "success";
        },
    },
};
</script>
