<template>
    <div
        v-if="visible"
        :class="['alert', 'alert-dismissible', `alert-${type}`]"
        role="alert"
    >
        {{ message }}
        <button
            type="button"
            class="btn-close"
            @click="close"
        ></button>
    </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
    message: String,
    type: {
        type: String,
        default: "info", // Can be 'info', 'success', 'warning', or 'danger'
    },
});

const visible = ref(!!props.message);

watch(
    () => props.message,
    (newMessage) => {
        visible.value = !!newMessage;
        if (newMessage) {
            // Auto-hide the message after 5 seconds
            setTimeout(() => {
                close();
            }, 5000);
        }
    }
);

const close = () => {
    visible.value = false;
};
</script>

<style scoped>
.alert {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1050;
    min-width: 250px;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>
