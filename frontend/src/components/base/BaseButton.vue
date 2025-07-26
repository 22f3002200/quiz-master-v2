<template>
    <component
        :is="tag"
        :to="to"
        :class="['btn', `btn-${color}`]"
        :type="tag === 'button' ? 'button' : undefined"
        :disabled="disabled"
        @click="$emit('click', '$event')"
    >
        <span
            v-if="loading"
            class="spinner-border spinner-border-sm me-2"
        ></span>
        <slot></slot>
    </component>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
    to: String,
    color: {
        type: String,
        default: "",
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
defineEmits(["click"]);

const tag = computed(() => (props.to ? "router-link" : "button"));
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
    background-color: var(--primary) !important;
    border-color: var(--primary) !important;
    color: var(--background) !important;
}

.btn-primary:hover {
    background-color: var(--primary);
    border-color: var(--primary);
    color: var(--background);
    transform: translate(0, -3px);
    box-shadow: 0 20px 80px -10px var(--text);
}

.btn-primary:active {
    background-color: var(--primary);
    border-color: var(--primary);
    color: var(--text);
}

.btn-secondary {
    background-color: var(--secondary);
    color: var(--text);
}

.btn-secondary:hover {
    background-color: var(--secondary);
    box-shadow: 0 20px 80px -10px var(--text);
}
</style>
