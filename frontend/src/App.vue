<template>
    <div class="min-vh-100">
        <HeaderSection v-if="!$route.meta.hideLayout" />
        <main>
            <router-view :title="title" />
        </main>
        <FooterSection v-if="!$route.meta.hideLayout" />
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
    background-color: var(--background);
}
</style>
