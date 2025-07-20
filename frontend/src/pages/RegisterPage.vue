<template>
    <div class="container mt-5">
        <h2>Register</h2>
        <form @submit.prevent="registerUser">
            <input
                v-model="form.full_name"
                class="form-control my-2"
                placeholder="Full Name"
                required
            />
            <input
                v-model="form.email"
                type="email"
                class="form-control my-2"
                placeholder="Email"
                required
            />
            <input
                v-model="form.password"
                type="password"
                class="form-control my-2"
                placeholder="Password"
                required
            />
            <input
                v-model="form.qualification"
                class="form-control my-2"
                placeholder="Qualification"
            />
            <input
                v-model="form.dob"
                type="date"
                class="form-control my-2"
            />
            <button
                type="submit"
                class="btn btn-success"
            >
                Register
            </button>
        </form>
    </div>
</template>

<script>
import api from "../utils/api";

export default {
    data() {
        return {
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
            try {
                const res = await api.post("/register", this.form);
                localStorage.setItem("access_token", res.data.access_token);
                this.$router.push("/profile");
            } catch (err) {
                alert(err.response?.data?.msg || "Registration failed");
            }
        },
    },
};
</script>
