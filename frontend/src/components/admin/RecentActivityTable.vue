<template>
    <div class="card h-100 border-0 shadow-sm">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5
                    class="card-title fw-bold mb-0"
                    style="color: var(--primary)"
                >
                    {{ title }}
                </h5>
                <router-link
                    :to="viewAllPath"
                    class="btn btn-sm"
                    style="
                        background-color: var(--primary5);
                        color: var(--primary);
                    "
                >
                    View All
                </router-link>
            </div>
            <div class="table-responsive">
                <table class="table table-borderless table-hover">
                    <thead>
                        <tr>
                            <th
                                v-for="header in headers"
                                :key="header.key"
                                class="text-muted small text-uppercase"
                            >
                                {{ header.text }}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="item in items"
                            :key="item.id"
                        >
                            <td
                                v-for="header in headers"
                                :key="header.key"
                                class="align-middle"
                            >
                                {{ item[header.key] }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: String,
    items: Array,
    headers: Array,
    viewAllPath: String,
});
</script>

<style scoped>
.table {
    margin-bottom: 0;
}
thead th {
    font-weight: 600;
}
tbody td {
    color: var(--text);
}
.table-hover tbody tr:hover {
    background-color: var(--primary5);
}
</style>
