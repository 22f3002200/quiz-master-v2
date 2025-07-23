<template>
    <div class="mb-3">
        <label
            :for="id"
            class="form-label fw-semibold"
            style="color: var(--background)"
            >{{ label }}</label
        >
        <div class="position-relative">
            <input
                :type="showPassword ? 'text' : type"
                class="form-control pe-5"
                :id="id"
                :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value)"
                :placeholder="placeholder"
                :required="required"
            />

            <!-- Eye icon inside input -->
            <i
                v-if="type === 'password'"
                :class="['bi', showPassword ? 'bi-eye-slash' : 'bi-eye']"
                class="toggle-password"
                @click="togglePassword"
            ></i>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
defineProps({
    id: String,
    label: String,
    type: {
        type: String,
        default: "text",
    },
    modelValue: String,
    placeholder: String,
    required: {
        type: Boolean,
        default: false,
    },
});

const showPassword = ref(false);

function togglePassword() {
    showPassword.value = !showPassword.value;
}
</script>

<style scoped>
input {
    background-color: var(--background);
    border: 1px solid var(--primary);
    transition: box-shadow 0.3s ease, border 0.3s ease;
}

input:focus {
    outline: none;
    box-shadow: 0 0 0.3em var(--text);
    border: 1px solid var(--primary);
}

.toggle-password {
    position: absolute;
    top: 50%;
    right: 1rem;
    transform: translateY(-50%);
    cursor: pointer;
    color: var(--primary);
    font-size: 1.1rem;
}
</style>
