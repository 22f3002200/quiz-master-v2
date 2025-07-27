<template>
    <div>
        <div
            class="modal fade"
            :class="{ show: show }"
            :style="{ display: show ? 'block' : 'none' }"
            tabindex="-1"
            @click.self="$emit('close')"
        >
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <slot name="header">Default Header</slot>
                        </h5>
                        <button
                            type="button"
                            class="btn-close"
                            @click="$emit('close')"
                        ></button>
                    </div>
                    <div class="modal-body">
                        <slot name="body">Default Body</slot>
                    </div>
                    <div class="modal-footer">
                        <slot name="footer">
                            <BaseButton
                                color="secondary"
                                @click="$emit('close')"
                            >
                                Close
                            </BaseButton>
                            <BaseButton color="primary"
                                >Save changes</BaseButton
                            >
                        </slot>
                    </div>
                </div>
            </div>
        </div>
        <div
            v-if="show"
            class="modal-backdrop fade show"
        ></div>
    </div>
</template>

<script setup>
defineProps({
    show: {
        type: Boolean,
        required: true,
    },
});
defineEmits(["close"]);
</script>

<style scoped>
.modal-content {
    background-color: var(--background);
    color: var(--text);
}
.modal-header {
    border-bottom: 1px solid var(--primary5);
    color: var(--primary);
}
.modal-footer {
    border-top: 1px solid var(--primary5);
}
.modal.show {
    backdrop-filter: blur(3px);
}
</style>
