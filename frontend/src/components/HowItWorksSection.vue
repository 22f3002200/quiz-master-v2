<!-- components/HowItWorks.vue -->
<template>
    <section
        id="how-it-works"
        class="py-5"
    >
        <div class="container text-center mb-5">
            <h2 class="fw-bold text-dark mb-3">How QuizMaster Works</h2>
            <p class="lead text-secondary">
                Getting started is easy. Follow these simple steps to begin your
                quiz journey.
            </p>
        </div>

        <div class="container position-relative">
            <div
                class="d-none d-md-block position-absolute top-50 start-0 end-0 translate-middle-y bg-primary"
                style="height: 2px; z-index: 0"
            ></div>
            <div class="row text-center z-1 position-relative">
                <div
                    class="col-md-4 mb-4"
                    v-for="(step, index) in steps"
                    :key="index"
                >
                    <div
                        class="bg-white p-4 rounded shadow-sm h-100 d-flex flex-column align-items-center"
                    >
                        <div
                            class="bg-primary bg-opacity-25 rounded-circle d-flex align-items-center justify-content-center mb-3"
                            style="width: 64px; height: 64px"
                        >
                            <i
                                :class="step.icon"
                                class="fs-4 text-primary"
                            ></i>
                        </div>
                        <h5 class="fw-semibold text-dark mb-2">
                            {{ step.title }}
                        </h5>
                        <p class="text-secondary">{{ step.description }}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
const steps = [
    {
        icon: "bi-person-add",
        title: "Sign up",
        description: "Sign up to see pre-made quizzes.",
    },
    {
        icon: "bi-play-circle",
        title: "Play Anywhere",
        description:
            "Take quizzes on any device, anytime. Perfect for learning on the go or during downtime.",
    },

    {
        icon: "bi-award",
        title: "Track Progress",
        description:
            "See your improvement over time with detailed statistics and performance insights.",
    },
];
</script>

<style scoped>
#how-it-works {
    background-color: #f8f8f8;
}

div.container {
    max-width: 1050px;
}
</style>
