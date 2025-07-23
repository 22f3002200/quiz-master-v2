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
                                <i class="bi bi-person-plus-fill fs-2"></i
                                >{{ title }}
                            </h2>
                            <p class="">
                                {{ greet }}
                            </p>
                        </div>

                        <!-- Alert for success or error messages -->
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

                        <!-- Registration Form -->
                        <form @submit.prevent="registerUser">
                            <FormInput
                                v-for="field in fields"
                                :key="field.id"
                                :label="field.label"
                                :type="field.type"
                                v-model="form[field.model]"
                                :placeholder="field.placeholder"
                                required
                            />

                            <!-- Qualification Dropdown -->
                            <div class="mb-3">
                                <label
                                    for="qualification"
                                    class="form-label fw-semibold"
                                    >Qualification</label
                                >
                                <select
                                    id="qualification"
                                    class="form-select"
                                    v-model="form.qualification"
                                    required
                                >
                                    <option
                                        disabled
                                        value=""
                                    >
                                        Please select one
                                    </option>
                                    <option
                                        v-for="qual in qualifications"
                                        :key="qual"
                                        :value="qual"
                                    >
                                        {{ qual }}
                                    </option>
                                </select>
                            </div>
                            <BaseButton
                                type="submit"
                                color="primary"
                                class="w-100 py-2 fw-semibold gradient-btn"
                                :loading="loading"
                            >
                                Sign up
                            </BaseButton>
                        </form>

                        <div class="text-center mt-4">
                            <p class="">
                                Already have an account?
                                <router-link
                                    to="/login"
                                    class="text-decoration-none fw-semibold link"
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
// import { useAuth } from "@/composables/useAuth";
import FormInput from "@/components/base/FormInput.vue";
import BaseButton from "@/components/base/BaseButton.vue";

export default {
    components: {
        FormInput,
        BaseButton,
    },
    data() {
        return {
            title: "QuizMaster",
            greet: "Join us today! Create your account to get started.",
            loading: false,
            message: "",
            messageType: "",
            form: {
                full_name: "",
                email: "",
                qualification: "",
                dob: "",
                password: "",
            },

            qualifications: [
                "High School",
                "Bachelor's Degree",
                "Master's Degree",
                "PhD",
                "Other",
            ],
            fields: [
                {
                    id: "full_name",
                    label: "Full name",
                    type: "text",
                    model: "full_name",
                    placeholder: "Enter your full name",
                },
                {
                    id: "email",
                    label: "Email",
                    type: "email",
                    model: "email",
                    placeholder: "Enter your email",
                },
                {
                    id: "password",
                    label: "Password",
                    type: "password",
                    model: "password",
                    placeholder: "Create a password",
                },
                {
                    id: "dob",
                    label: "Date of Birth",
                    type: "date",
                    model: "dob",
                },
            ],
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
                console.error("Error response:", err.response);
                this.message =
                    err.response?.data?.msg ||
                    "Registration failed. Please try again.";
                this.messageType = "error";
                // Clear the message after 5 seconds
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
/* Reusing styles from LoginPage.vue for consistency */
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

/* Custom styles for the select dropdown to match FormInput */
.form-select {
    background-color: var(--background);
    border: 1px solid var(--primary);
    color: var(--text);
    transition: box-shadow 0.3s ease, border 0.3s ease;
}

.form-select:focus {
    outline: none;
    box-shadow: 0 0 0.3em var(--text);
    border: 1px solid var(--primary);
    background-color: var(--background);
}

/* Styling for dropdown options */
.form-select option {
    background: var(--background);
    color: var(--text);
}
</style>
