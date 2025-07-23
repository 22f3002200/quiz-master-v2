<template>
    <button
        :class="['btn', `btn-${color}`]"
        :disabled="disabled"
    >
        <span
            v-if="loading"
            class="spinner-border spinner-border-sm me-2"
        ></span>
        <slot></slot>
    </button>
</template>

<script setup>
defineProps({
    color: {
        type: String,
        default: "primary",
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    loading: {
        type: Boolean,
        default: false,
    },
});
</script>

<style scoped>
.btn {
    padding: 0.5em 2em;
    transition: transform ease 0.2s, box-shadow ease 0.2s;
    display: inline-block;
    z-index: 2;
    white-space: nowrap;
    color: var(--background);
}

.btn-primary {
    background-color: var(--primary);
}

.btn-primary:hover {
    background-color: var(--primary);
    color: var(--background);
    transform: translate(0, -3px);
    box-shadow: 0 20px 80px -10px var(--text);
}

.btn-secondary {
    background-color: var(--secondary);
    color: var(--text);
}

.btn-secondary:hover {
    box-shadow: 0 20px 80px -10px var(--text);
}
</style>
