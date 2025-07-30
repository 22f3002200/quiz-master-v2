<template>
    <div class="search-bar position-relative d-flex align-items-center gap-2">
        <div class="input-group">
            <input
                v-model="term"
                @input="onSearch"
                @keydown.down.prevent="navigate(1)"
                @keydown.up.prevent="navigate(-1)"
                @keydown.enter="goToSelected"
                type="text"
                class="form-control"
                placeholder="Search..."
            />
            <button
                class="btn btn-outline-secondary"
                @click="showFilters = !showFilters"
            >
                <i class="bi bi-funnel"></i>
            </button>
        </div>

        <div
            v-if="showFilters"
            class="filter-dropdown shadow rounded p-2 position-absolute bg-white"
            style="top: 100%; z-index: 1000"
        >
            <div
                v-for="area in areas"
                :key="area"
                class="form-check"
            >
                <input
                    class="form-check-input"
                    type="checkbox"
                    :id="area"
                    v-model="selectedAreas"
                    :value="area"
                />
                <label
                    class="form-check-label"
                    :for="area"
                >
                    {{ capitalize(area) }}
                </label>
            </div>
        </div>

        <ul
            v-if="results.length"
            class="list-group position-absolute w-100"
            style="top: 100%; z-index: 1000"
        >
            <li
                v-for="(item, index) in results"
                :key="item.id + item.type"
                class="list-group-item list-group-item-action"
                :class="{ active: index === selectedIndex }"
                @click="goToResult(item)"
                @mouseover="selectedIndex = index"
            >
                {{ item.name || item.title }} ({{ item.type }})
            </li>
        </ul>
    </div>
</template>

<script>
import { useAuth } from "@/composables/useAuth";
import api from "@/utils/api";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
    setup() {
        const term = ref("");
        const results = ref([]);
        const selectedIndex = ref(-1);
        const areas = ["subject", "chapter", "quizzes"];
        const selectedAreas = ref([...areas]);
        const showFilters = ref(false);
        const router = useRouter();
        const { user } = useAuth();

        const onSearch = async () => {
            if (term.value.trim().length < 2) {
                results.value = [];
                return;
            }

            const response = await api.get("/api/admin/search", {
                params: {
                    term: term.value,
                    area: selectedAreas.value.join(","),
                },
            });

            const combined = [
                ...(response.data.subjects || []),
                ...(response.data.chapters || []),
                ...(response.data.quizzes || []),
            ];
            results.value = combined;
        };

        const goToResult = (item) => {
            const highlight = encodeURIComponent(term.value);
            const userRole = user.value ? user.value.role : null;

            if (userRole === "admin") {
                if (item.type === "subject") {
                    router.push(
                        `/admin/subjects?highlight=${highlight}&id=${item.id}`
                    );
                } else if (item.type === "chapter") {
                    router.push(
                        `/admin/chapters?highlight=${highlight}&id=${item.id}`
                    );
                } else if (item.type === "quiz") {
                    router.push(
                        `/admin/quizzes?highlight=${highlight}&id=${item.id}`
                    );
                }
            } else if (userRole === "user") {
                if (item.type === "subject") {
                    router.push(`/user/subjects/${item.id}/chapters`);
                } else if (item.type === "chapter") {
                    router.push(
                        `/user/subjects/${item.subject_id}/chapters/${item.id}/quizzes`
                    );
                } else if (item.type === "quiz") {
                    router.push(`/user/quiz/${item.id}`);
                }
            }
            clearSearch();
        };

        const clearSearch = () => {
            term.value = "";
            results.value = [];
            selectedIndex.value = -1;
        };

        const navigate = (dir) => {
            selectedIndex.value =
                (selectedIndex.value + dir + results.value.length) %
                results.value.length;
        };

        const goToSelected = () => {
            if (
                selectedIndex.value >= 0 &&
                results.value[selectedIndex.value]
            ) {
                goToResult(results.value[selectedIndex.value]);
            }
        };

        const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

        return {
            term,
            results,
            areas,
            selectedAreas,
            showFilters,
            selectedIndex,
            onSearch,
            goToResult,
            navigate,
            goToSelected,
            capitalize,
        };
    },
};
</script>

<style scoped>
.filter-dropdown {
    width: 200px;
}

input[type="text"] {
    min-width: 300px;
}

.list-group-item.active {
    background-color: var(--primary);
    color: white;
}
</style>
