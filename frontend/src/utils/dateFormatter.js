export function formatToIST(dateString, options = { showTime: true }) {
    if (!dateString) {
        return "N/A";
    }

    const date = new Date(dateString);

    return date.toLocaleString("en-IN", {
        timeZone: "Asia/Kolkata",
        year: "numeric",
        month: "long",
        day: "numeric",
        ...(options.showTime && {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        }),
    });
}
