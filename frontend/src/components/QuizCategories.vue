<!-- components/QuizCategories.vue -->
<template>
    <section
        id="categories"
        class="py-5 bg-white"
    >
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="fw-bold text-dark mb-3">Explore Quiz Categories</h2>
                <p class="lead text-secondary">
                    Discover quizzes across a wide range of topics to challenge
                    yourself and expand your knowledge.
                </p>
            </div>

            <div class="row g-4">
                <div
                    v-for="(category, index) in categories"
                    :key="index"
                    class="col-sm-6 col-lg-4"
                >
                    <div
                        class="border rounded overflow-hidden h-100 shadow-sm hover-shadow transition"
                    >
                        <!-- Top color bar -->
                        <div
                            :class="['w-100', category.color, 'd-block']"
                            style="height: 4px"
                        ></div>

                        <div
                            class="p-4 d-flex flex-column justify-content-between h-100"
                        >
                            <!-- Icon and title -->
                            <div class="d-flex align-items-start mb-3">
                                <div
                                    :class="[
                                        category.color + '-light',
                                        'p-2 rounded me-3 d-flex align-items-center justify-content-center',
                                    ]"
                                    style="min-width: 42px; height: 42px"
                                >
                                    <i
                                        :class="[
                                            'fs-5',
                                            category.icon,
                                            category.color + '-text',
                                        ]"
                                    ></i>
                                </div>
                                <div>
                                    <h5 class="fw-semibold mb-1">
                                        {{ category.name }}
                                    </h5>
                                    <small class="text-muted">{{
                                        category.quizCount
                                    }}</small>
                                </div>
                            </div>

                            <!-- Difficulty tags -->
                            <div class="mb-3 d-flex flex-wrap gap-2">
                                <span class="badge bg-light text-dark"
                                    >Beginner</span
                                >
                                <span class="badge bg-light text-dark"
                                    >Intermediate</span
                                >
                                <span class="badge bg-light text-dark"
                                    >Advanced</span
                                >
                            </div>

                            <!-- Button -->
                            <button class="btn btn-light w-100">
                                Browse Quizzes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
const categories = [
    {
        icon: "bi-book",
        name: "Literature",
        quizCount: "450+ quizzes",
        color: "bg-primary",
    },
    {
        icon: "bi-code-slash",
        name: "Technology",
        quizCount: "320+ quizzes",
        color: "bg-purple",
    },
    {
        icon: "bi-globe",
        name: "Geography",
        quizCount: "280+ quizzes",
        color: "bg-success",
    },
    {
        icon: "bi-heart-fill",
        name: "Health",
        quizCount: "190+ quizzes",
        color: "bg-danger",
    },
    {
        icon: "bi-music-note-beamed",
        name: "Music",
        quizCount: "210+ quizzes",
        color: "bg-warning",
    },
    {
        icon: "bi-flask",
        name: "Science",
        quizCount: "380+ quizzes",
        color: "bg-info",
    },
];
</script>

<style scoped>
.bg-primary-light {
    background-color: rgba(13, 110, 253, 0.1);
}
.bg-purple-light {
    background-color: rgba(111, 66, 193, 0.1);
}
.bg-success-light {
    background-color: rgba(25, 135, 84, 0.1);
}
.bg-danger-light {
    background-color: rgba(220, 53, 69, 0.1);
}
.bg-warning-light {
    background-color: rgba(255, 193, 7, 0.1);
}
.bg-info-light {
    background-color: rgba(13, 202, 240, 0.1);
}

.bg-primary-text {
    color: #0d6efd;
}
.bg-purple-text {
    color: #6f42c1;
}
.bg-success-text {
    color: #198754;
}
.bg-danger-text {
    color: #dc3545;
}
.bg-warning-text {
    color: #ffc107;
}
.bg-info-text {
    color: #0dcaf0;
}
</style>
