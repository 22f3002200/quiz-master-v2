<!-- components/HeroSection.vue -->
<template>
    <section class="gradient text-white py-5">
        <div class="container py-5">
            <div class="row align-items-center">
                <div class="col-md-6 mb-4 mb-md-0">
                    <h1 class="display-4 fw-bold mb-3">
                        Challenge Your Knowledge with Interactive Quizzes
                    </h1>
                    <p class="lead mb-4">
                        Create, share, and take quizzes on any topic. Perfect
                        for learning, teaching, or just having fun with friends.
                    </p>
                    <div class="d-flex flex-column flex-sm-row gap-3">
                        <button
                            class="btn btn-light text-primary fw-semibold px-4 py-2"
                        >
                            Get Started Free
                        </button>
                        <button
                            class="btn btn-outline-light d-flex align-items-center px-4 py-2"
                        >
                            Watch Demo
                            <i class="bi bi-arrow-right ms-2"></i>
                        </button>
                    </div>
                </div>
                <div class="col-md-6">
                    <div
                        class="p-4 bg-white text-dark rounded shadow position-relative"
                        style="transform: rotate(3deg)"
                    >
                        <div class="bg-light p-3 rounded mb-3">
                            <h5 class="text-primary fw-bold mb-3">
                                Pop Culture Quiz
                            </h5>
                            <div>
                                <div class="mb-2 p-2 bg-white border rounded">
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
.gradient {
    background: linear-gradient(
        90deg,
        rgba(42, 123, 155, 1) 0%,
        rgba(87, 100, 199, 1) 50%,
        rgba(83, 152, 237, 1) 100%
    );
}
</style>
