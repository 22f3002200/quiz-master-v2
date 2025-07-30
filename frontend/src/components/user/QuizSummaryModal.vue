<template>
    <div
        v-if="show"
        class="modal fade show"
        style="display: block"
        tabindex="-1"
    >
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Quiz Summary</h5>
                    <button
                        type="button"
                        class="btn-close"
                        @click="close"
                    ></button>
                </div>
                <div class="modal-body">
                    <ul class="list-group">
                        <li
                            class="list-group-item d-flex justify-content-between align-items-center"
                        >
                            Total Questions
                            <span class="badge bg-primary rounded-pill">{{
                                summary.total_questions
                            }}</span>
                        </li>
                        <li
                            class="list-group-item d-flex justify-content-between align-items-center"
                        >
                            Correct Answers
                            <span class="badge bg-success rounded-pill">{{
                                summary.correct_count
                            }}</span>
                        </li>
                        <li
                            class="list-group-item d-flex justify-content-between align-items-center"
                        >
                            Incorrect Answers
                            <span class="badge bg-danger rounded-pill">{{
                                summary.wrong_count
                            }}</span>
                        </li>
                        <li
                            class="list-group-item d-flex justify-content-between align-items-center"
                        >
                            Unattempted
                            <span class="badge bg-secondary rounded-pill">{{
                                summary.unattempted_count
                            }}</span>
                        </li>
                        <li
                            class="list-group-item d-flex justify-content-between align-items-center"
                        >
                            <strong>Total Score</strong>
                            <strong>{{ summary.total_score }}</strong>
                        </li>
                    </ul>
                </div>
                <div class="modal-footer">
                    <button
                        type="button"
                        class="btn btn-primary"
                        @click="close"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

defineProps({
    show: Boolean,
    summary: Object,
});

const emit = defineEmits(["close"]);

const close = () => {
    emit("close");
};
</script>

<style scoped>
.modal {
    background-color: rgba(0, 0, 0, 0.5);
}
</style>
