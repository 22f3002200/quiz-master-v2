<template>
    <nav
        class="navbar navbar-expand-lg navbar-light bg-gradient-primary px-4 py-2 shadow-sm"
    >
        <div class="container-fluid">
            <a
                class="navbar-brand d-flex align-items-center"
                href="/"
            >
                <!-- Optional: Add an emoji or SVG icon -->
                <i
                    class="bi bi-question-diamond-fill me-2 text-warning fs-4"
                ></i>
                <span class="fw-bold text-white">Quizzy</span>
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
                class="collapse navbar-collapse justify-content-end"
                id="navbarNav"
            >
                <ul class="navbar-nav gap-2">
                    <li
                        class="nav-item"
                        v-if="!loggedIn"
                    >
                        <router-link
                            to="/login"
                            class="nav-link text-white fw-medium hover-underline-animation"
                        >
                            Login
                        </router-link>
                    </li>
                    <li
                        class="nav-item"
                        v-if="!loggedIn"
                    >
                        <router-link
                            to="/register"
                            class="nav-link text-white fw-medium hover-underline-animation"
                        >
                            Register
                        </router-link>
                    </li>
                    <li
                        class="nav-item"
                        v-if="loggedIn"
                    >
                        <router-link
                            to="/profile"
                            class="nav-link text-white fw-medium hover-underline-animation"
                        >
                            Profile
                        </router-link>
                    </li>
                    <li
                        class="nav-item"
                        v-if="loggedIn"
                    >
                        <button
                            class="btn btn-outline-light btn-sm rounded-pill px-3 fw-medium"
                            @click="logout"
                        >
                            Logout
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
