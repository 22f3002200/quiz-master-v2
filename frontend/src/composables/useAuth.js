import { ref, computed } from "vue";

const user = ref(null);

try {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
        user.value = JSON.parse(storedUser);
    }
} catch (error) {
    console.error("Failed to parse user from localStorage", error);
    user.value = null;
}

export function useAuth() {
    const setUser = (userData) => {
        user.value = userData;
        if (userData) {
            localStorage.setItem("user", JSON.stringify(userData));
        } else {
            localStorage.removeItem("user");
            localStorage.removeItem("access_token");
        }
    };

    const isAdmin = computed(() => {
        return (
            user.value && user.value.roles && user.value.roles.includes("admin")
        );
    });

    const logout = () => {
        setUser(null);
    };

    return {
        user,
        setUser,
        isAdmin,
        logout,
    };
}
