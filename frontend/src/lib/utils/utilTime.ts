import { error } from "@sveltejs/kit";

export function formatDateTime(isoDate: string) {
    const dateObj = new Date(isoDate);
    let error = "";
    if (isNaN(dateObj.getTime())) {
        error = "Некорректная дата";  // Return the error message directly
    }
    
    const options: Intl.DateTimeFormatOptions = {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    };
    
    const [formattedDate, formattedTime] = dateObj.toLocaleString("ru-RU", options).split(", ");
    return { formattedDate, formattedTime, error };  // Return as an object
}

