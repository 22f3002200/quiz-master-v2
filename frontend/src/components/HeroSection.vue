<!-- components/HeroSection.vue -->
<template>
    <section class="bg py-5">
        <div class="container py-5">
            <div class="row align-items-center">
                <div class="col-md-6 mb-4 mb-md-0">
                    <h1 class="display-4 fw-bold mb-3 heading">
                        Challenge Your Knowledge with Interactive Quizzes
                    </h1>
                    <p class="lead mb-4 description fw-normal">
                        Create, share, and take quizzes on any topic. Perfect
                        for learning, teaching, or just having fun with friends.
                    </p>
                    <div class="d-flex flex-column flex-sm-row gap-3">
                        <router-link
                            to="/register"
                            class="btn fw-semibold px-4 py-2"
                        >
                            Get Started
                        </router-link>
                    </div>
                </div>
                <div class="col-md-6">
                    <div
                        class="p-4 card-text rounded shadow-lg position-relative"
                        style="transform: rotate(3deg)"
                    >
                        <div class="p-3 rounded mb-3">
                            <h5 class="fw-bold mb-3">Pop Culture Quiz</h5>
                            <div>
                                <div class="mb-2 p-2 question-box rounded">
                                    Which actor played Iron Man in the Marvel
                                    movies?
                                </div>
                                <div class="d-grid gap-2">
                                    <div
                                        class="option correct px-3 py-2 rounded"
                                    >
                                        Robert Downey Jr.
                                    </div>
                                    <div class="option px-3 py-2 rounded">
                                        Chris Evans
                                    </div>
                                    <div class="option px-3 py-2 rounded">
                                        Mark Ruffalo
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between">
                            <small class="question">Question 3 of 10</small>
                            <button class="btn btn-sm">Next</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import "../assets/global.css";
</script>

<style scoped>
section,
.question-card {
    background-color: var(--background);
}

h1.heading,
h5 {
    color: var(--text);
}

div.question-box {
    border: 1px solid var(--primary);
}

p.description,
div.bg,
div.option,
small.question {
    color: var(--primary);
}

div.correct {
    background-color: var(--primary);
    color: var(--background);
}

.btn {
    padding: 0.5em 2em;
    background-color: var(--primary);
    transition: transform ease 0.2s, box-shadow ease 0.2s;
    display: inline-block;
    z-index: 2;
    white-space: nowrap;
    color: var(--background);
}

.btn:hover {
    background-color: var(--primary);
    color: var(--background);
    transform: translate(0, -3px);
    box-shadow: 0 20px 80px -10px var(--text);
}

.btn:active {
    box-shadow: 0 0 2em var(--secondary) !important;
    background-color: var(--primary) !important;
}
</style>
