// +page.ts
import { getCookie } from "$lib/utils/utilCookie";
import { BASE_URL } from "../../../config";

type Event = {
  event_id: number;
  event_name: string;
  date: string;
};

export const load = async () => {
  const authToken = getCookie("auth_token");
  console.log("Auth token:", authToken);

  if (!authToken) {
    return {
      events: [],
      error: "Auth token is missing. Please log in.",
      loading: false,  // Return loading as false if no token
    };
  }

  let loading = true;

  try {
    const response = await fetch(`${BASE_URL}/user_events`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authToken}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Ошибка при загрузке мероприятий");
    }

    const events: Event[] = await response.json();
    console.log(events);
    return {
      events,
      error: null, // No error if data is fetched successfully
      loading: false, // Set loading to false when the request is completed
    };
  } catch (err) {
    const error =
      err instanceof Error
        ? err.message
        : "Неизвестная ошибка при загрузке мероприятий";
    return {
      events: [],
      error,
      loading: false, // Set loading to false if there is an error
    };
  }
};
