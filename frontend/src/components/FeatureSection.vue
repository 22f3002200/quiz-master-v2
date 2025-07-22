<template>
    <section
        id="features"
        class="py-5 bg-white"
    >
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="fw-bold text-dark mb-3">
                    Elevate Your Quiz Experience
                </h2>
                <p class="lead text-secondary">
                    QuizMaster offers everything you need to create, share, and
                    enjoy interactive quizzes.
                </p>
            </div>

            <div class="row g-4 text-center">
                <div
                    class="col"
                    v-for="(feature, index) in features"
                    :key="index"
                >
                    <div
                        class="bg-light rounded p-4 h-100 shadow-sm d-flex flex-column align-items-center"
                    >
                        <div
                            class="bg-primary bg-opacity-25 rounded-circle d-flex align-items-center justify-content-center mb-3"
                            style="width: 64px; height: 64px"
                        >
                            <i
                                :class="feature.icon"
                                class="fs-4 text-primary"
                            ></i>
                        </div>
                        <h5 class="fw-semibold text-dark mb-2">
                            {{ feature.title }}
                        </h5>
                        <p class="text-secondary mb-0">
                            {{ feature.description }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
const features = [
    {
        icon: "bi-question-lg",
        title: "Thousands of Questions",
        description: "Access vast library of questions.",
    },
    {
        icon: "bi-trophy",
        title: "Leaderboards & Achievements",
        description: "Showcase your knowledge prowess.",
    },
    {
        icon: "bi-bar-chart",
        title: "Detailed Analytics",
        description: "Track your progress over time .",
    },
];
</script>

<style scoped>
#features {
    background-color: #f8fafc;
}

div.container {
    max-width: 1050px;
}
</style>
