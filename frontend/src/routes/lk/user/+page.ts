import { getCookie } from "$lib/utils/utilCookie";
import { BASE_URL } from "../../../config";

type Event = {
  event_id: number;
  event_name: string;
  date: string;
};

export const load = async () => {
  // Логируем полученный токен
  const authToken = getCookie("auth_token");
  console.log("Auth token:", authToken);

  if (!authToken) {
    // Логируем ошибку, если токен отсутствует
    console.error("Auth token is missing");
    return {
      events: [],
      error: "Auth token is missing. Please log in.",
      loading: false,  // Возвращаем loading как false, если токен отсутствует
    };
  }

  let loading = true;

  try {
    // Логируем информацию перед отправкой запроса
    console.log("Fetching events from API...");

    const response = await fetch(`${BASE_URL}/user_events`, {
      method: "GET",
      headers: {
        Authorization: `${authToken}`,
        "Content-Type": "application/json",
      },
    });

    // Логируем статус ответа от сервера
    console.log("Response status:", response.status);

    if (!response.ok) {
      const errorMessage = `Ошибка при загрузке мероприятий. Статус: ${response.status}`;
      console.error(errorMessage);
      throw new Error(errorMessage);
    }

    const events: Event[] = await response.json();
    
    // Логируем полученные данные
    console.log("Events fetched:", events);

    return {
      events,
      error: null, // Нет ошибки, если данные загружены успешно
      loading: false, // Устанавливаем loading в false, когда запрос завершен
    };
  } catch (err) {
    // Логируем ошибку в случае сбоя запроса
    console.error("Error while fetching events:", err);

    const error =
      err instanceof Error
        ? err.message
        : "Неизвестная ошибка при загрузке мероприятий";
    
    return {
      events: [],
      error,
      loading: false, // Устанавливаем loading в false, если произошла ошибка
    };
  }
};
