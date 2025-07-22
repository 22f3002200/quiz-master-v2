<template>
    <header>
        <nav
            class="navbar navbar-expand-lg fixed-top navbar-light bg-white shadow-sm py-2"
        >
            <div class="container-xxl">
                <a
                    class="navbar-brand d-flex align-items-center gap-2"
                    href="#"
                >
                    <i
                        class="bi bi-hourglass-split fs-3"
                        style="color: #3d98f4"
                    ></i>
                    <h2
                        class="h4 mb-0 fw-bold"
                        style="color: #3d98f4"
                    >
                        QuizMaster
                    </h2>
                </a>
                <button
                    class="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div
                    class="collapse navbar-collapse"
                    id="navbarNav"
                >
                    <ul class="navbar-nav ms-auto align-items-end">
                        <li class="nav-item">
                            <a
                                class="nav-link"
                                href="/#features"
                                >Features</a
                            >
                        </li>
                        <li class="nav-item">
                            <a
                                class="nav-link"
                                href="/#how-it-works"
                                >How it works</a
                            >
                        </li>
                        <li class="nav-item">
                            <a
                                class="nav-link"
                                href="/#categories"
                                >Categories</a
                            >
                        </li>
                    </ul>
                    <span class="d-flex"
                        ><div class="d-flex align-items-end ms-auto gap-2">
                            <a
                                href="#"
                                class="btn btn-light text-light"
                                >Login</a
                            >
                            <a
                                href="#"
                                class="btn btn-primary"
                                >Signup</a
                            >
                        </div></span
                    >
                </div>
            </div>
        </nav>
    </header>
</template>

<script setup></script>

<style scoped>
.nav-link {
    color: #64748b;
}
.nav-link:hover {
    color: #3d98f4;
}
.btn-primary {
    background-color: #3d98f4;
    border-color: #3d98f4;
}

.btn-light {
    background-color: #64748b;
    border-color: #e0f2f7;
}

.btn-light:hover {
    background-color: #5e708ade;
}
</style>
