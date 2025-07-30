<template>
    <aside
        class="sidebar"
        :class="sidebarClass"
    >
        <div
            v-if="user"
            class="user-profile d-flex align-items-center mb-4"
        >
            <i class="bi bi-person-circle fs-2 me-2"></i>
            <span class="fs-5 fw-semibold">{{ user.full_name }}</span>
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
                    <i :class="[link.icon, 'icon', 'me-2', 'fs-5']"></i>
                    <span class="link-text">{{ link.text }}</span>
                </router-link>
            </li>

            <li
                class="nav-item"
                v-if="user && user.role === 'admin'"
            >
                <button
                    class="nav-link d-flex align-items-center w-100 text-start"
                    @click="exportCsv"
                >
                    <i
                        class="bi bi-file-earmark-arrow-down-fill icon me-2 fs-5"
                    />
                    <span class="link-text">Export CSV</span>
                </button>
            </li>

            <li class="nav-item">
                <button
                    class="nav-link d-flex align-items-center w-100 text-start"
                    @click="logout"
                >
                    <i class="bi bi-box-arrow-right icon me-2 fs-5" />
                    <span class="link-text">Logout</span>
                </button>
            </li>
        </ul>
    </aside>
</template>

<script setup>
import { useAuth } from "@/composables/useAuth";
import { computed } from "vue";
import api from "@/utils/api";

const { logout } = useAuth();
defineProps({
    navLinks: Array,
});

const { user } = useAuth();

const sidebarClass = computed(() =>
    user.value ? "sidebar--mobile-hidden" : ""
);

const exportCsv = async () => {
    try {
        const response = await api.post("/api/admin/export-csv");
        if (response.data.url) {
            console.log("downloading...");
        } else {
            alert(
                "Error exporting CSV: " +
                    (response.data.error || "Unknown error")
            );
        }
    } catch (error) {
        console.error("Failed to export CSV:", error);
        alert("Failed to export CSV. Please check the console for details.");
    }
};
</script>

<style scoped>
.sidebar {
    height: 100%;
    width: 250px;
    border-radius: 10px;
    background-color: var(--static);
    padding: 1em;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.5em;
    margin: 3.8em 0 0 2em;
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
    background-color: var(--primary) !important;
    color: var(--background);
}

.nav-link.active i {
    color: var(--background);
}

@media (max-width: 950px) {
    .sidebar {
        width: 70px;
        padding: 1em 0.5em;
    }

    .link-text,
    .user-profile span {
        display: none;
    }

    .user-profile {
        justify-content: center;
    }
}
</style>
