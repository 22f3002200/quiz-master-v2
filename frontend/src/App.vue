<template>
    <div class="min-vh-100">
        <HeaderSection v-if="!$route.meta.hideLayout" />
        <main>
            <router-view :title="title" />
        </main>
        <FlashMessage
            :message="flash.message"
            :type="flash.type"
        />
        <FooterSection v-if="!$route.meta.hideLayout" />
    </div>
</template>

<script>
import HeaderSection from "./components/HeaderSection.vue";
import FooterSection from "./components/FooterSection.vue";
import FlashMessage from "./components/base/FlashMessage.vue";

export default {
    components: { HeaderSection, FooterSection, FlashMessage },
    data() {
        return {
            title: "QuizMaster",
            flash: {
                message: "",
                type: "",
            },
        };
    },
    created() {
        this.emitter.on("flash", (data) => {
            this.flash.message = data.message;
            this.flash.type = data.type;
        });
    },
};
</script>

<style scoped>
main {
    min-height: 100vh;
    background-color: var(--background);
}
</style>
