<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import Icon from "$lib/components/Icon.svelte";

  let eventId: string;

  // Данные мероприятия
  let eventData = {
    event_name: '',
    place: '',
    long_description: '',
    short_description: '',
    max_count_of_members: 0,
    online_event_link: '',
    format: 'offline',
    date: '',
    tags: ''
  };

  // Отдельные поля для даты и времени
  let eventDate = '';
  let eventTime = '';

  let isLoading = true;

  // Функция загрузки данных мероприятия
  async function fetchEventDetails() {
    const authToken = localStorage.getItem('auth_token'); // Получение токена из локального хранилища

    if (!authToken) {
      alert('Необходимо войти в систему для просмотра данных!');
      return;
    }

    try {
      const response = await fetch(`http://62.84.122.113:8000/events/${eventId}`, {
        method: 'GET',
        headers: {
          'Authorization': `${authToken}` // Добавляем токен в заголовок
        }
      });

      if (!response.ok) {
        throw new Error(`Ошибка загрузки данных: ${response.statusText}`);
      }

      const data = await response.json();
      eventData = {
        event_name: data.event_name || '',
        place: data.place || '',
        long_description: data.long_description || '',
        short_description: data.short_description || '',
        max_count_of_members: data.max_count_of_members || 0,
        online_event_link: data.online_event_link || '',
        format: data.format || 'offline',
        date: data.date || '',
        tags: data.tags || ''
      };

      // Разделяем дату и время
      if (eventData.date) {
        [eventDate, eventTime] = eventData.date.split('T');
      }
    } catch (error) {
      console.error('Ошибка загрузки данных мероприятия:', error);
    } finally {
      isLoading = false;
    }
  }

  // Загружаем данные при монтировании компонента
  onMount(() => {
    eventId = $page.params.eventId;
    fetchEventDetails();
  });

  // Обработчик обновления данных
  async function updateEvent() {
    const authToken = localStorage.getItem('auth_token'); // Получение токена из локального хранилища

    if (!authToken) {
      alert('Необходимо войти в систему для обновления данных!');
      return;
    }

    // Объединяем дату и время перед отправкой
    eventData.date = `${eventDate}T${eventTime}`;

    try {
      const response = await fetch(`http://62.84.122.113:8000/events/${eventId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${authToken}` // Добавляем токен в заголовок
        },
        body: JSON.stringify(eventData)
      });

      if (!response.ok) {
        throw new Error(`Ошибка обновления данных: ${response.statusText}`);
      }

      alert('Данные успешно обновлены!');
    } catch (error) {
      console.error('Ошибка обновления данных:', error);
      alert('Не удалось обновить данные.');
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
          <input type="text" bind:value={eventData.tags} placeholder="Теги (через пробел)" />
          <textarea bind:value={eventData.short_description} placeholder="Короткое описание (до 150 символов)"></textarea>
          <textarea bind:value={eventData.long_description} placeholder="Длинное описание"></textarea>

          <div class="form-row">
            <!-- Привязка отдельных полей для даты и времени -->
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

    <div class="create-button-container">
      <button on:click={updateEvent}>Обновить данные</button>
    </div>
  {/if}
</div>



<style>


  :global(html, body) {
    margin: 0;
    padding: 0;
    background-color: #171615;
    height: 100%;
  }

  .page-background {
    background-color: #171615;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    box-sizing: border-box;
  }

  h1 {
    font-size: 46px;
    font-family: 'Epilepsy Sans', sans-serif;
    color: white;
    margin-top: 90px;
    margin-bottom: 30px;
    text-align: left;
    width: 100%;
    max-width: 1200px;
    margin-right: 3%;
    font-family: 'Press Start 2P', monospace;
  }

  .container {
    width: 90%;
    max-width: 1200px;
    padding: 20px;
    background-color: #242423;
    border-radius: 40px;
    color: white;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    gap: 20px;
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

  input, textarea, select {
    background-color: #171615;
    color: white;
    border: none;
    border-radius: 16px;
    padding: 20px;
    font-size: 20px;
  }

  textarea {
    min-height: 150px;
  }

  input:focus, textarea:focus, select:focus {
    outline: none;
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.7);
  }

  .form-row {
    display: flex;
    gap: 15px;
    width: 100%;
  }

  .form-row input, .form-row select {
    flex: 1;
    width: auto;
  }

  .form-row.narrow {
    justify-content: space-between;
  }

  .create-button-container {
    width: 83%;
    text-align: right;
    margin-top: 20px;
  }

  .create-button-container button {
    padding: 10px 20px;
    font-size: 16px;
    color: white;
    background-color: #242423;
    border: 1.3px solid rgba(255, 255, 255, 0.473);
    border-radius: 30px;
    cursor: pointer;
    width: 200px;
    transition: background-color 0.3s;
  }

  .create-button-container button:hover {
    background-color: white;
    color: black;
  }
  @media screen and (max-width: 768px) {
        h1 {
            font-size: 24px; /* Уменьшаем размер заголовка для мобильных */
            text-align: center; /* Выравниваем текст по центру */
        }

        .container {
            padding: 10px; /* Уменьшаем отступы */
            border-radius: 20px; /* Немного меньше радиус */
            width: 100%; /* Занимает всю ширину экрана */
            box-shadow: none; /* Убираем тень для минимализма */
        }

        .form {
            flex-direction: column; /* Элементы идут в столбик */
            gap: 10px; /* Меньше промежутки */
        }

        .form-row {
            flex-direction: column; /* Поля размещаем в столбик */
            gap: 10px;
        }

        input,
        textarea,
        select {
            font-size: 16px; /* Уменьшаем размер шрифта */
            padding: 10px; /* Уменьшаем внутренние отступы */
        }

        .create-button-container {
            margin-top: 10px;
            text-align: center; /* Центрируем кнопку */
        }

        .create-button-container button {
            width: 100%; /* Кнопка занимает всю ширину */
            font-size: 18px; /* Чуть больше шрифт для удобства на мобильных */
        }
    }
</style>
