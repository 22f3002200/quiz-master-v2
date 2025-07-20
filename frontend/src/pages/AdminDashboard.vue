<template>
    <div class="admin-dashboard bg-light py-5">
        <div class="container">
            <h1 class="fw-bold text-dark mb-4">Admin Dashboard</h1>
            <div class="row g-4">
                <div class="col-md-6 col-lg-3">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body text-center">
                            <i
                                class="bi bi-journal-bookmark fs-1 text-primary"
                            ></i>
                            <h5 class="card-title fw-semibold mt-3">
                                Subjects
                            </h5>
                            <p class="card-text text-secondary">
                                Manage course subjects
                            </p>
                            <a
                                href="#"
                                class="btn btn-outline-primary"
                                >Go to Subjects</a
                            >
                        </div>
                    </div>
                </div>

                <div class="col-md-6 col-lg-3">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body text-center">
                            <i class="bi bi-collection fs-1 text-success"></i>
                            <h5 class="card-title fw-semibold mt-3">
                                Chapters
                            </h5>
                            <p class="card-text text-secondary">
                                Manage subject chapters
                            </p>
                            <a
                                href="#"
                                class="btn btn-outline-success"
                                >Go to Chapters</a
                            >
                        </div>
                    </div>
                </div>

                <div class="col-md-6 col-lg-3">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body text-center">
                            <i
                                class="bi bi-patch-question fs-1 text-warning"
                            ></i>
                            <h5 class="card-title fw-semibold mt-3">Quizzes</h5>
                            <p class="card-text text-secondary">
                                Manage quizzes
                            </p>
                            <a
                                href="#"
                                class="btn btn-outline-warning"
                                >Go to Quizzes</a
                            >
                        </div>
                    </div>
                </div>

                <div class="col-md-6 col-lg-3">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body text-center">
                            <i class="bi bi-people fs-1 text-danger"></i>
                            <h5 class="card-title fw-semibold mt-3">Users</h5>
                            <p class="card-text text-secondary">
                                Manage registered users
                            </p>
                            <a
                                href="#"
                                class="btn btn-outline-danger"
                                >Go to Users</a
                            >
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "AdminDashboard",
};
</script>

<style scoped>
.admin-dashboard {
    min-height: 65vh;
}
</style>
