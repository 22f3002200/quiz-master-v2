<!-- components/HeroSection.vue -->
<template>
    <section class="background text-white py-5">
        <div class="container py-5">
            <div class="row align-items-center">
                <div class="col-md-6 mb-4 mb-md-0">
                    <h1 class="display-4 fw-bold mb-3 text-primary">
                        Challenge Your Knowledge with Interactive Quizzes
                    </h1>
                    <p class="lead mb-4 text-secondary fw-normal">
                        Create, share, and take quizzes on any topic. Perfect
                        for learning, teaching, or just having fun with friends.
                    </p>
                    <div class="d-flex flex-column flex-sm-row gap-3">
                        <router-link
                            to="/register"
                            class="btn btn-primary text-light fw-semibold px-4 py-2"
                        >
                            Get Started
                        </router-link>
                    </div>
                </div>
                <div class="col-md-6">
                    <div
                        class="p-4 bg-white text-dark rounded shadow-lg position-relative"
                        style="transform: rotate(3deg)"
                    >
                        <div class="bg-light p-3 rounded mb-3">
                            <h5 class="text-primary fw-bold mb-3">
                                Pop Culture Quiz
                            </h5>
                            <div>
                                <div class="mb-2 p-2 bg border rounded">
                                    Which actor played Iron Man in the Marvel
                                    movies?
                                </div>
                                <div class="d-grid gap-2">
                                    <div
                                        class="bg-primary text-white px-3 py-2 rounded"
                                    >
                                        Robert Downey Jr.
                                    </div>
                                    <div
                                        class="bg-light text-dark px-3 py-2 rounded"
                                    >
                                        Chris Evans
                                    </div>
                                    <div
                                        class="bg-light text-dark px-3 py-2 rounded"
                                    >
                                        Mark Ruffalo
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between">
                            <small class="text-muted">Question 3 of 10</small>
                            <button class="btn btn-primary btn-sm">Next</button>
                        </div>
                    </div>

                    <div
                        class="d-none d-md-block position-absolute bg-white p-4 rounded shadow"
                        style="
                            bottom: -30px;
                            right: -30px;
                            transform: rotate(-6deg);
                            width: 260px;
                            height: 130px;
                            z-index: -1;
                        "
                    >
                        <div class="bg-light w-100 h-100 rounded"></div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup></script>

<style scoped>
section.background {
    background-color: #f2f9ff;
}

div.container {
    max-width: 1050px;
}

div.bg {
    background-color: #f8f8f8;
}
</style>
