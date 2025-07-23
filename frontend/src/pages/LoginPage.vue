<template>
    <div
        class="min-vh-100 d-flex align-items-center justify-content-center gradient"
    >
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-6 col-lg-5">
                    <div class="card-box rounded shadow p-5">
                        <div class="text-center mb-4">
                            <h2
                                class="fw-bold mb-2 d-flex align-items-center justify-content-center gap-2"
                            >
                                <i class="bi bi-box-arrow-in-right fs-2"></i
                                >{{ title }}
                            </h2>
                            <p class="">
                                {{ greet }}
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

                        <form @submit.prevent="loginUser">
                            <FormInput
                                v-for="field in inputFields"
                                :key="field.id"
                                :id="field.id"
                                :label="field.label"
                                :type="field.type"
                                v-model="form[field.id]"
                                :placeholder="field.placeholder"
                                required
                            />

                            <BaseButton
                                type="submit"
                                color="primary"
                                class="w-100 py-2 fw-semibold gradient-btn"
                                :loading="loading"
                            >
                                Sign In
                            </BaseButton>
                        </form>

                        <div class="text-center mt-4">
                            <p class="">
                                Don't have an account?
                                <router-link
                                    to="/register"
                                    class="text-decoration-none fw-semibold link"
                                >
                                    Sign Up
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
import { useAuth } from "../composables/useAuth";
import FormInput from "../components/base/FormInput.vue";
import BaseButton from "../components/base/BaseButton.vue";

export default {
    props: {
        title: {
            type: String,
            required: true,
        },
    },
    components: {
        FormInput,
        BaseButton,
    },
    data() {
        return {
            greet: "Welcome back! Please sign in to continue.",
            loading: false,
            message: "",
            messageType: "",
            form: {
                email: "",
                password: "",
            },

            inputFields: [
                {
                    id: "email",
                    label: "Email Address",
                    type: "email",
                    model: "email",
                    placeholder: "Enter your email",
                },
                {
                    id: "password",
                    label: "Password",
                    type: "password",
                    model: "password",
                    placeholder: "Enter your password",
                },
            ],
        };
    },
    methods: {
        async loginUser() {
            console.log("Form data:", this.form);
            this.loading = true;
            this.message = "";
            const { setUser } = useAuth();
            try {
                const res = await api.post("/api/auth/login", this.form);
                const { user, access_token } = res.data;

                // Set items in local storage
                localStorage.setItem("user", JSON.stringify(user));
                localStorage.setItem("access_token", access_token);

                // Update app's state
                setUser(user);

                // Redirect based on user role
                if (res.data.user.role === "admin") {
                    this.$router.push("/admin/dashboard");
                } else {
                    this.$router.push("/user/dashboard");
                }
            } catch (err) {
                console.error("Error response:", err.response);
                this.message = err.response?.data?.msg || "Login failed";
                this.messageType = "error";
                setTimeout(() => {
                    this.message = "";
                }, 5000);
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>

<style scoped>
div.card-box {
    background: linear-gradient(160deg, var(--primary), var(--accent));
}

h2,
p,
label {
    color: var(--background);
}

.gradient {
    background: var(--background);
}

.gradient-btn {
    background: linear-gradient(190deg, var(--primary), var(--accent));
    border: 1px solid var(--background);
    transition: transform 0.2s ease;
}

.gradient-btn:hover {
    transform: translateY(-1px);
    border: 1px solid var(--primary);
}

.link {
    color: var(--background);
}
</style>
