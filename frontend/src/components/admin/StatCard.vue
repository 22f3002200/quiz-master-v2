<template>
    <div class="card h-100 border-0 shadow-sm stat-card">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <h6 class="card-subtitle text-muted fw-semibold">
                    {{ title }}
                </h6>
                <i :class="[icon, 'fs-4 icon-bg']"></i>
            </div>
            <h2
                class="card-title fw-bold mt-2"
                style="color: var(--primary)"
            >
                {{ value }}
            </h2>
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: String,
    value: String,
    icon: String,
});
</script>

<style scoped>
.stat-card {
    background-color: #ffffff;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}
.icon-bg {
    color: var(--secondary);
}
</style>
