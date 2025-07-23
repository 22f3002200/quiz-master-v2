<!-- components/QuizCategories.vue -->
<template>
    <section
        id="categories"
        class="py-5"
    >
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="fw-bold mb-3">Explore Quiz Categories</h2>
                <p class="lead">
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
                            :class="['w-100', 'd-block']"
                            style="height: 4px"
                        ></div>

                        <div
                            class="p-4 d-flex flex-column justify-content-between h-100"
                        >
                            <!-- Icon and title -->
                            <div class="d-flex align-items-start mb-3">
                                <div
                                    :class="[
                                        'p-2 rounded me-3 d-flex align-items-center justify-content-center',
                                    ]"
                                    style="min-width: 42px; height: 42px"
                                >
                                    <i :class="['fs-5', category.icon]"></i>
                                </div>
                                <div>
                                    <h5 class="fw-semibold mb-1">
                                        {{ category.name }}
                                    </h5>
                                    <small class="">{{
                                        category.quizCount
                                    }}</small>
                                </div>
                            </div>

                            <!-- Difficulty tags -->
                            <div class="mb-3 d-flex flex-wrap gap-2">
                                <span class="badge">Beginner</span>
                                <span class="badge">Intermediate</span>
                                <span class="badge">Advanced</span>
                            </div>

                            <!-- Button -->
                            <button class="btn w-100">Browse Quizzes</button>
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
    },
    {
        icon: "bi-code-slash",
        name: "Technology",
        quizCount: "320+ quizzes",
    },
    {
        icon: "bi-globe",
        name: "Geography",
        quizCount: "280+ quizzes",
    },
    {
        icon: "bi-heart-fill",
        name: "Health",
        quizCount: "190+ quizzes",
    },
    {
        icon: "bi-music-note-beamed",
        name: "Music",
        quizCount: "210+ quizzes",
    },
    {
        icon: "bi-flask",
        name: "Science",
        quizCount: "380+ quizzes",
    },
];
</script>

<style scoped>
section {
    background-color: var(--background);
}

div.container {
    max-width: 1000px;
}

h2,
h5 {
    color: var(--primary);
}

p {
    color: var(--text);
}

div.border {
    background-color: var(--primary5);
}

div.d-block {
    background-color: var(--primary);
}

small {
    color: var(--primary);
}

span.badge {
    background-color: var(--secondary);
    color: var(--text);
}

.btn {
    background-color: var(--primary);
    color: var(--background);
}

.btn:hover {
    background-color: var(--primary);
    color: var(--background);
    transform: translate(0, -3px);
    box-shadow: 0 20px 80px -10px var(--text);
}

i {
    color: var(--primary);
}
</style>
