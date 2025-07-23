<template>
    <footer class="py-5">
        <div class="container text-center">
            <div class="d-flex justify-content-center gap-4 mb-4">
                <a
                    v-for="link in links"
                    :key="link.id"
                    :href="link.href"
                    class=""
                    >{{ link.field }}</a
                >
            </div>
            <div class="d-flex justify-content-center gap-4 mb-4">
                <a
                    v-for="social in socials"
                    :key="social.id"
                    :href="social.href"
                    class=""
                    ><i :class="social.i_class"></i
                ></a>
            </div>
            <p class="">&copy; 2025 QuizMaster. All rights reserved.</p>
        </div>
    </footer>
</template>

<script>
export default {
    data() {
        return {
            links: [
                {
                    id: "about-us",
                    href: "#",
                    field: "About us",
                },
                {
                    id: "contact",
                    href: "#",
                    field: "Contact",
                },
                {
                    id: "privacy-policy",
                    href: "#",
                    field: "Privacy Policy",
                },
                {
                    id: "terms-of-service",
                    href: "#",
                    field: "Terms of Service",
                },
            ],

            socials: [
                {
                    id: "x",
                    href: "#",
                    i_class: ["bi", "bi-twitter-x", "fs-4"],
                },
                {
                    id: "instagra,",
                    href: "#",
                    i_class: ["bi", "bi-instagram", "fs-4"],
                },
            ],
        };
    },
};
</script>

<style scoped>
footer {
    background-color: var(--text5);
}
a {
    color: var(--text);
    text-decoration: none;
}

i.bi {
    color: var(--primary);
}
</style>
