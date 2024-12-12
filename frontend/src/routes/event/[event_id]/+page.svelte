<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation"; // Добавлено
  import { page } from "$app/stores";
  import Icon from "$lib/components/Icon.svelte";
  import { BASE_URL } from "../../../config";
  import { getCookie } from "$lib/utils/utilCookie";
  import { formatDateTime } from "$lib/utils/utilTime";

  interface EventData {
    event_name: string;
    place: string;
    long_description: string;
    max_count_of_members: number;
    online_event_link?: string;
    format: string;
    tags: string;
    date: string; // ISO-строка с датой и временем
    is_active: boolean;
  }

  let eventInfo = {
    photo: "",
    title: "Название мероприятия",
    date: "",
    time: "",
    location: "",
    format: "",
    participants: "",
    maxCountOfMembers: 0,
    description: "",
    onlineLink: "",
  };

  let loading: boolean = true;
  let error: string = "";
  let isAuthorized: boolean = false;
  let showNotification: boolean = false;
  let notificationMessage: string = "";
  let notificationType: "success" | "error" = "error";

  function checkAuthorization() {
    const token = getCookie("auth_token");
    isAuthorized = !!token;
  }

  async function fetchEventImage(eventId: string) {
    const imageUrl = `${BASE_URL}/show_event_image/${eventId}`;
    try {
      const response = await fetch(imageUrl);
      if (response.ok) {
        return imageUrl;
      } else {
        console.warn("Изображение не найдено, используется placeholder");
        return "";
      }
    } catch (err) {
      console.error("Ошибка загрузки изображения:", err);
      return "";
    }
  }

  async function fetchRegisteredCount(eventId: string) {
    const API_URL = `${BASE_URL}/count_members/${eventId}`;
    try {
      const response = await fetch(API_URL);
      if (!response.ok) {
        throw new Error(
          `Ошибка загрузки количества участников: ${response.status}`
        );
      }
      const data = await response.json();
      const currentCount = typeof data === "number" ? data : 0;
      eventInfo.participants = `Участников: ${currentCount}/${eventInfo.maxCountOfMembers}`;
    } catch (err) {
      console.error("Ошибка получения количества участников:", err);
      eventInfo.participants = `Участников: неизвестно/${eventInfo.maxCountOfMembers}`;
    }
  }

  async function fetchEventData(eventId: string) {
    const API_URL = `${BASE_URL}/events/${eventId}`;
    try {
      const response = await fetch(API_URL);
      if (!response.ok) {
        throw new Error(`Ошибка загрузки данных: ${response.status}`);
      }
      const data: EventData = await response.json();

      const { formattedDate, formattedTime } = formatDateTime(data.date);
      const eventPhoto = await fetchEventImage(eventId);

      eventInfo = {
        photo: eventPhoto,
        title: data.event_name,
        date: formattedDate,
        time: formattedTime,
        location: data.place,
        format: `Формат мероприятия: ${data.format}`,
        participants: `Участников: 0/${data.max_count_of_members}`,
        maxCountOfMembers: data.max_count_of_members,
        description: data.long_description,
        onlineLink: data.online_event_link || "",
      };

      await fetchRegisteredCount(eventId);
    } catch (err) {
      console.error("Ошибка загрузки данных события:", err);
      error = (err as Error).message;
    } finally {
      loading = false;
    }
  }

  $: {
    const eventId = $page.params.event_id;
    if (eventId) {
      fetchEventData(eventId);
    } else {
      error = "Некорректный идентификатор события.";
      loading = false;
    }
  }

  onMount(() => {
    checkAuthorization();
  });

  async function register() {
    if (!isAuthorized) {
      notificationType = "error";
      showNotification = true;
      notificationMessage = "Для регистрации войдите в аккаунт.";
      return;
    }

    const token = getCookie("auth_token");
    if (!token) {
      notificationType = "error";
      showNotification = true;
      notificationMessage = "Ошибка авторизации. Повторите вход.";
      return;
    }

    const eventId = parseInt($page.params.event_id, 10);
    if (isNaN(eventId)) {
      notificationType = "error";
      showNotification = true;
      notificationMessage = "Ошибка: некорректный идентификатор события.";
      return;
    }

    const API_URL = `${BASE_URL}/add_member?event_id=${eventId}`;

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          Authorization: `${token}`,
        },
      });

      // Проверка на 401 ошибку
      if (response.status === 401) {
        notificationType = "error";
        showNotification = true;
        notificationMessage = "Для регистрации войдите в аккаунт.";
        return;
      }

      if (!response.ok) {
        throw new Error(`Ошибка регистрации: ${response.statusText}`);
      }

      const result = await response.json();
      notificationType = "success";
      showNotification = true;
      notificationMessage = "Вы успешно зарегистрировались на мероприятие!";

      await fetchRegisteredCount(String(eventId));
    } catch (err) {
      notificationType = "error";
      showNotification = true;
      notificationMessage = "Не удалось зарегистрироваться. Попробуйте позже.";
    }
  }

  function joinOnline() {
    if (eventInfo.onlineLink) {
      window.open(eventInfo.onlineLink, "_blank");
    } else {
      alert("Ссылка на онлайн встречу недоступна.");
    }
  }

  function closeNotification() {
    showNotification = false;
    notificationMessage = "";
  }
</script>
<div class="icon"><Icon id="logo" /></div>

{#if loading}
  <div class="loading">Загрузка...</div>
{:else if error}
  <div class="error">{error}</div>
{:else}
  <div class="page-background">
    <div class="event-page">
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <div class="close-btn" on:click={() => goto("/")}>×</div>
      <div class="header">
        {#if eventInfo.photo}
          <img src={eventInfo.photo} alt="Фото мероприятия" class="event-photo" />
        {:else}
          <div class="event-photo">540x270 Placeholder</div>
        {/if}
        <div class="event-details">
          <h1 class="event-title">{eventInfo.title}</h1>
          <div class="event-meta">
            <span>{eventInfo.location}</span>
            <span>{eventInfo.date}</span>
            <span>{eventInfo.time}</span>
          </div>
          <div>
            <div class="event-format">{eventInfo.format}</div>
            <div class="event-participants">{eventInfo.participants}</div>
          </div>
        </div>
      </div>

      <div class="description">{eventInfo.description}</div>

      <div class="buttons">
        <button class="register-btn" on:click={register}>Зарегистрироваться</button>

        {#if eventInfo.onlineLink.trim() !== ""}
          <button class="online-btn" on:click={joinOnline}>Онлайн встреча</button>
        {/if}
      </div>
    </div>
  </div>

  {#if showNotification}
    <div class="notification {notificationType}">
      <p>{notificationMessage}</p>
      <button on:click={closeNotification}>Закрыть</button>
    </div>
  {/if}
{/if}

<style>
  .page-background {
    background-color: #171615;
    background-image: url("/eventbackground.png");
    background-size: cover;
    min-height: 100vh;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    position: absolute;
    top: 0;
    left: 0;
  }

  .event-page {
    background-color: rgba(36, 36, 35, 0.8);
    color: white;
    padding: 30px;
    width: 85%;
    min-height: 60vh;
    margin-top: 90px;
    border-radius: 45px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    border: 1px solid #838383;
  }

  .header {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
    flex-wrap: nowrap;
    width: 100%;
    justify-content: flex-start;
    font-family: "Font Over";


  }

  .event-photo {
    width: 350px;
    height: 350px;
    object-fit: cover;
    border-radius: 15px;
    background-color: #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #888;
    font-size: 16px;
    font-weight: bold;
    text-align: center;
  
  }

  .event-details {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 10px;
    max-width: 600px;
    margin-left: 20px;
    text-align: left;
  }

  .event-title {
    font-size: 40px;
    font-weight: bold;
    margin: 0;
    margin-bottom: 15px;
    font-family: "Font Over";
  }

  .event-meta {
    display: flex;
    gap: 15px;
    font-size: 24px;
    color: #838383;
    font-family: 'Inter', sans-serif;
  }

  .event-participants{
    font-family: "Font Over";

  }
  .event-format,
  .event-participants {
    font-size: 24px;
    color: #838383;
    margin-bottom: 40px;
    font-family: 'Inter', sans-serif;
  }

  .description {
    background-color: rgba(20, 20, 20, 0.685);
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 28px;
    word-wrap: break-word;
    font-family: "Inter", sans-serif;
    max-height: none;
    flex-grow: 1;
    width: calc(
      100% -20px
    ); /* Равняется ширине контейнера минус ширина изображения + отступ */
    text-align: left;
  }

  .buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
    flex-wrap: wrap;
    gap: 10px;
    width: 100%;
  }

  
  .register-btn,
  .online-btn {
    background-color: transparent;
    color: white;
    border: 2px solid white;
    border-radius: 25px;
    padding: 15px 20px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    text-align: center;
    font-family: 'Inter', sans-serif;
    margin: 5px;
  }


  .online-btn:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }

  .notification {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 20px;
    border-radius: 10px;
    background-color: var(--notification-bg, #f44336);
    color: white;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    font-size: 16px;
  }

  .notification.success {
    --notification-bg: #4caf50;
  }

  .notification.error {
    --notification-bg: #f44336;
  }

  .notification button {
    background-color: #444;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
  }

  .notification button:hover {
    background-color: #666;
  }

  @media (max-width: 768px) {
    .event-page {
      width: 80%;
    }

    .event-title {
      font-size: 32px;
    }

    .header {
      flex-direction: column;
      align-items: center;
      margin-bottom: 20px;
    }

    .event-photo {
      width: 100%;
      height: auto;
      margin-bottom: 20px;
    }

    .event-details {
      width: 100%;
      text-align: center;
      margin: 0;
    }

    .event-meta {
      flex-direction: column;
      gap: 15px;
      text-align: center;
    }

    .description {
      width: 95%;
      font-size: 20px;
    }

    .buttons {
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    .register-btn,
    .online-btn {
      width: 90%;
      font-size: 14px;
      margin: 10px 0;
    }
  }

  .close-btn {
    position: absolute;
    top: 10px;
    right: 20px;
    font-size: 36px;
    color: rgba(135, 135, 135, 1);
    cursor: pointer;
    font-weight: bold;
  }

  .close-btn:hover {
    color: #ffffff;
  }
</style>

