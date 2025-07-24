<template>
    <aside class="sidebar">
        <div class="user-profile d-flex align-items-center mb-4">
            <i class="bi bi-person-circle fs-2 me-2"></i>
            <span class="fs-5 fw-semibold">Coolest User</span>
        </div>
        <ul class="nav nav-pills flex-column mb-auto">
            <li
                v-for="link in navLinks"
                :key="link.to"
                class="nav-item"
            >
                <router-link
                    :to="link.to"
                    class="nav-link d-flex align-items-center"
                    active-class="active"
                >
                    <i :class="[link.icon, 'me-2', 'fs-5']"></i>
                    {{ link.text }}
                </router-link>
            </li>
        </ul>
    </aside>
</template>

<script setup>
defineProps({
    navLinks: Array,
});
</script>

<style scoped>
.sidebar {
    height: 100%;
    width: 20%;
    border-radius: 10px;
    background-color: var(--static);
    padding: 1em;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.5em;
}

.user-profile {
    color: var(--primary);
}

.nav-link {
    color: var(--text);
    font-weight: 500;
    transition: background-color 0.2s, color 0.2s;
}

.nav-link:hover {
    background-color: var(--primary5);
    color: var(--primary);
}

.nav-link.active {
    background-color: var(--primary);
    color: var(--background);
}

.nav-link.active i {
    color: var(--background);
}
</style>
