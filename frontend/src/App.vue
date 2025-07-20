<template>
    <div class="min-vh-100 bg-light">
        <HeaderSection />
        <main>
            <router-view />
        </main>
        <FooterSection />
    </div>
</template>

<script setup>
import HeaderSection from "./components/HeaderSection.vue";
import FooterSection from "./components/FooterSection.vue";
</script>
