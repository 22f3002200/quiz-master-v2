<template>
    <div class="card h-100 border-0 shadow-sm">
        <div class="card-body">
            <h5
                class="card-title fw-bold"
                style="color: var(--primary)"
            >
                Quiz Performance
            </h5>
            <p class="card-text text-muted small">
                Overview of quiz attempts and average scores for the last 6
                months.
            </p>
            <div
                class="chart-placeholder mt-3 d-flex align-items-center justify-content-center"
            >
                <p class="text-muted">[Bar Chart Visualization Area]</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.chart-placeholder {
    min-height: 320px;
    background-color: var(--primary5);
    border-radius: 0.5rem;
}
</style>
