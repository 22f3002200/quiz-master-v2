import router from "@/router";
import { ref } from "vue";

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

    const logout = () => {
        setUser(null);
        router.push("/login");
    };

    return {
        user,
        setUser,
        logout,
    };
}
