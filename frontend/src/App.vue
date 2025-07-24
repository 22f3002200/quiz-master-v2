<template>
    <div class="min-vh-100">
        <HeaderSection />
        <main>
            <router-view :title="title" />
        </main>
        <FooterSection />
    </div>
</template>

<script>
import HeaderSection from "./components/HeaderSection.vue";
import FooterSection from "./components/FooterSection.vue";

export default {
    components: { HeaderSection, FooterSection },
    data() {
        return {
            title: "QuizMaster",
        };
    },
};
</script>

<style scoped>
main {
    min-height: 100vh;
}
</style>
