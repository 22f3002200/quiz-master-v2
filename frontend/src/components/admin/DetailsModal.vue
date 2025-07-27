<template>
    <BaseModal
        :show="show"
        @close="$emit('close')"
    >
        <template #header>{{ title }}</template>
        <template #body>
            <div v-if="item">
                <div
                    v-for="field in fields"
                    :key="field.key"
                    class="mb-2"
                >
                    <p v-if="item[field.key]">
                        <strong>{{ field.label }}:</strong>
                        {{
                            field.isDate
                                ? formatToIST(item[field.key], {
                                      showTime: field.key !== "date_of_quiz",
                                  })
                                : item[field.key]
                        }}
                    </p>
                </div>
            </div>
            <div v-else>
                <p>No details available.</p>
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
import { formatToIST } from "@/utils/dateFormatter";

defineProps({
    show: Boolean,
    title: {
        type: String,
        default: "Details",
    },
    item: Object,
    fields: {
        type: Array,
        required: true,
    },
});

defineEmits(["close"]);
</script>
