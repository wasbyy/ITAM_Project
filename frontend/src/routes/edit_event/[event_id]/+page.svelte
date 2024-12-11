<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import Icon from "$lib/components/Icon.svelte";
  import { BASE_URL } from "../../../config";
  import { getCookie } from "$lib/utils/utilCookie";

  let eventId: string;

  // Данные мероприятия
  let eventData = {
    event_name: "",
    place: "",
    long_description: "",
    short_description: "",
    max_count_of_members: 0,
    online_event_link: "",
    format: "offline",
    date: "",
    tags: "",
  };

  // Отдельные поля для даты и времени
  let eventDate = "";
  let eventTime = "";

  let isLoading = true;

  // Функция загрузки данных мероприятия
  async function fetchEventDetails() {
    const authToken = getCookie("auth_token");

    if (!authToken) {
      alert("Необходимо войти в систему для просмотра данных!");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/events/${eventId}`, {
        method: "GET",
        headers: { Authorization: `${authToken}` },
      });

      if (!response.ok) {
        throw new Error(`Ошибка загрузки данных: ${response.statusText}`);
      }

      const data = await response.json();

      eventData = {
        event_name: data.event_name || "",
        place: data.place || "",
        long_description: data.long_description || "",
        short_description: data.short_description || "",
        max_count_of_members: data.max_count_of_members || 0,
        online_event_link: data.online_event_link || "",
        format: data.format || "offline",
        date: data.date || "",
        tags: data.tags || "",
      };

      if (eventData.date) {
        [eventDate, eventTime] = eventData.date.split("T");
      }
    } catch (error) {
      console.error("Ошибка загрузки данных мероприятия:", error);
    } finally {
      isLoading = false;
    }
  }

  onMount(() => {
    eventId = $page.params.event_id;
    if (eventId) {
      fetchEventDetails();
    }
  });

  async function updateEvent() {
    const authToken = getCookie("auth_token");
    if (!authToken) {
      alert("Необходимо войти в систему для обновления данных!");
      return;
    }

    eventData.date = `${eventDate}T${eventTime}`;
    try {
      const response = await fetch(`${BASE_URL}/events/${eventId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `${authToken}`,
        },
        body: JSON.stringify(eventData),
      });

      if (!response.ok) {
        throw new Error(`Ошибка обновления данных: ${response.statusText}`);
      }

      alert("Данные успешно обновлены!");
      // Перенаправление на страницу /lk/admin после успешного обновления
      window.location.href = "/lk/admin";
    } catch (error) {
      console.error("Ошибка обновления данных:", error);
      alert("Не удалось обновить данные.");
    }
  }

  async function deleteEvent() {
    const authToken = getCookie("auth_token");
    if (!authToken) {
      alert("Необходимо войти в систему для удаления данных!");
      return;
    }

    if (confirm("Вы уверены, что хотите удалить это мероприятие?")) {
      try {
        const response = await fetch(`${BASE_URL}/delete_event/${eventId}`, {
          method: "DELETE",
          headers: { Authorization: `${authToken}` },
        });

        if (!response.ok) {
          throw new Error(`Ошибка удаления мероприятия: ${response.statusText}`);
        }

        alert("Мероприятие успешно удалено!");
        // Перенаправление на страницу /lk/admin после успешного удаления
        window.location.href = "/lk/admin";
      } catch (error) {
        console.error("Ошибка удаления мероприятия:", error);
        alert("Не удалось удалить мероприятие.");
      }
    }
  }

  async function archiveEvent() {
    const authToken = getCookie("auth_token");
    if (!authToken) {
      alert("Необходимо войти в систему для архивации данных!");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/archive_events/${eventId}`, {
        method: "PATCH",
        headers: {
          Authorization: `${authToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ archived: true }),
      });

      if (!response.ok) {
        throw new Error(`Ошибка архивации мероприятия: ${response.statusText}`);
      }

      alert("Мероприятие успешно архивировано!");
      // Перенаправление на страницу /lk/admin после успешной архивации
      window.location.href = "/lk/admin";
    } catch (error) {
      console.error("Ошибка архивации мероприятия:", error);
      alert("Не удалось архивировать мероприятие.");
    }
  }
</script>

<Icon id="logo" />
<div class="page-background">
  <h1>Редактирование мероприятия</h1>

  {#if isLoading}
    <div>Загрузка данных...</div>
  {:else}
    <div class="container">
      <div class="form">
        <div class="form-column">
          <input type="text" bind:value={eventData.event_name} placeholder="Название мероприятия" />
          <input type="text" bind:value={eventData.tags} placeholder="Короткие теги (через пробел)" />
          <textarea
            bind:value={eventData.short_description}
            placeholder="Короткое описание (до 150 символов)"
            class="short-description"
          ></textarea>
          <textarea
            bind:value={eventData.long_description}
            placeholder="Длинное описание"
            class="long-description"
          ></textarea>

          <div class="form-row">
            <input type="date" bind:value={eventDate} />
            <input type="time" bind:value={eventTime} />
            <input type="text" bind:value={eventData.place} placeholder="Место" />
          </div>

          <div class="form-row narrow">
            <input type="number" bind:value={eventData.max_count_of_members} placeholder="Макс. участников" />
            <select bind:value={eventData.format}>
              <option value="offline">Офлайн</option>
              <option value="online">Онлайн</option>
            </select>
          </div>

          <input type="text" bind:value={eventData.online_event_link} placeholder="Ссылка на онлайн мероприятие (если нет - пробел)" />
        </div>
      </div>
    </div>

    <div class="action-buttons-container">
      <div class="left-buttons">
        <button class="delete-button" on:click={deleteEvent}>Удалить мероприятие</button>
        <button class="archive-button" on:click={archiveEvent}>Архивировать мероприятие</button>
      </div>
      <div class="right-button">
        <button class="update-button" on:click={updateEvent}>Обновить данные</button>
      </div>
    </div>
  {/if}
</div>


<style>
  .page-background {
    background-color: #171615;
    width: 100vw;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    box-sizing: border-box;
    background-image: url("/editevent.png");
    background-size: cover;
    background-position: center center;
  }

  h1 {
    font-size: 42px;
    font-family: 'Press Start 2P', monospace;
    color: white;
    margin-top: 80px;
    margin-bottom: 30px;
    text-align: left;
    width: 90%;
  }

  .container {
    width: 90%;
    padding: 15px;
    background-color: rgba(36, 36, 35, 0.5);
    border-radius: 40px;
    color: white;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    gap: 40px;
    border: 1.3px solid rgba(255, 255, 255, 0.473);
  }

  .form {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }

  .form-column {
    display: flex;
    flex-direction: column;
    gap: 15px;
    flex: 1;
  }

  input,
  textarea,
  select {
    background-color: #171615;
    color: white;
    border: none;
    border-radius: 16px;
    padding: 20px;
    font-size: 16px;
  }

  .short-description {
    height: 100px;
  }

  .long-description {
    height: 250px;
  }

  .form-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    width: 100%;
  }

  .form-row input,
  .form-row select {
    flex: 1;
    min-width: 100px;
  }

  .action-buttons-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    width: 92%;
  }

  .left-buttons {
    display: flex;
    gap: 10px;
  }

  .right-button {
    display: flex;
  }

  .delete-button,
  .update-button,
  .archive-button {
    padding: 20px 22px;
    font-size: 15px;
    color: white;
    background-color: #242423;
    border: 1.3px solid rgba(255, 255, 255, 0.473);
    border-radius: 30px;
    cursor: pointer;
    width: 250px;
    text-align: center;
    transition: background-color 0.3s;
  }

  .delete-button:hover {
    background-color: #d9534f;
  }

  .update-button:hover {
    background-color: white;
    color: black;
  }

  .archive-button:hover {
    background-color: #f0ad4e;
  }

  @media (max-width: 480px) {
    h1 {
      font-size: 24px;
      margin-top: 80px;
    }

    input,
    textarea,
    select {
      padding: 8px;
      font-size: 12px;
      border-radius: 10px;
    }

    .action-buttons-container {
      gap: 3px;
    }

    .delete-button,
    .update-button,
    .archive-button {
      font-size: 10px;
      width: 100px;
      padding: 6px 8px;
    }
  }
  
  .page-background {
    background-color: #171615;
    width: 100vw;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    box-sizing: border-box;
    background-image: url("/editevent.png");
    background-size: cover;
    background-position: center center;
  }

  h1 {
    font-size: 42px;
    font-family: 'Press Start 2P', monospace;
    color: white;
    margin-top: 80px;
    margin-bottom: 30px;
    text-align: left;
    width: 90%;
  }

  .container {
    width: 90%;
    padding: 15px;
    background-color: rgba(36, 36, 35, 0.5);
    border-radius: 40px;
    color: white;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    gap: 40px;
    border: 1.3px solid rgba(255, 255, 255, 0.473);
  }

  .form {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }

  .form-column {
    display: flex;
    flex-direction: column;
    gap: 15px;
    flex: 1;
  }

  input,
  textarea,
  select {
    background-color: #171615;
    color: white;
    border: none;
    border-radius: 16px;
    padding: 20px;
    font-size: 16px;
  }

  .short-description {
    height: 100px;
  }

  .long-description {
    height: 250px;
  }

  .form-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    width: 100%;
  }

  .form-row input,
  .form-row select {
    flex: 1;
    min-width: 100px;
  }

  .action-buttons-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    width: 92%;
  }

  .left-buttons {
    display: flex;
    gap: 10px;
  }

  .right-button {
    display: flex;
  }

  .delete-button,
  .update-button,
  .archive-button {
    padding: 20px 22px;
    font-size: 15px;
    color: white;
    background-color: #242423;
    border: 1.3px solid rgba(255, 255, 255, 0.473);
    border-radius: 30px;
    cursor: pointer;
    width: 250px;
    text-align: center;
    transition: background-color 0.3s;
  }

  .delete-button:hover {
    background-color: #d9534f;
  }

  .update-button:hover {
    background-color: white;
    color: black;
  }

  .archive-button:hover {
    background-color: #f0ad4e;
  }

  @media (max-width: 480px) {
    h1 {
      font-size: 24px;
      margin-top: 80px;
    }

    input,
    textarea,
    select {
      padding: 8px;
      font-size: 12px;
      border-radius: 10px;
    }

    .action-buttons-container {
      gap: 3px;
    }

    .delete-button,
    .update-button,
    .archive-button {
      font-size: 10px;
      width: 100px;
      padding: 6px 8px;
    }
  }
</style>

