<template>
    <BaseModal
        :show="show"
        @close="$emit('close')"
    >
        <template #header>Chapter Details</template>
        <template #body>
            <div v-if="chapter">
                <p><strong>ID:</strong> {{ chapter.id }}</p>
                <p><strong>Name:</strong> {{ chapter.name }}</p>
                <p><strong>Description:</strong> {{ chapter.description }}</p>
                <p><strong>Subject ID:</strong> {{ chapter.subject_id }}</p>
                <p>
                    <strong>Created At:</strong>
                    {{ new Date(chapter.created_at).toLocaleString() }}
                </p>
            </div>
            <div v-else>
                <p>No chapter details available.</p>
            </div>
        </template>
        <template #footer>
            <BaseButton
                color="secondary"
                @click="$emit('close')"
                >Close</BaseButton
            >
        </template>
    </BaseModal>
</template>

<script setup>
import BaseModal from "@/components/base/BaseModal.vue";
import BaseButton from "@/components/base/BaseButton.vue";

defineProps({
    show: Boolean,
    chapter: Object,
});

defineEmits(["close"]);
</script>
