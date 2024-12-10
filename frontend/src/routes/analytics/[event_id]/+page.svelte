<script lang="ts">
  import { page } from '$app/stores';
  import Icon from '$lib/components/Icon.svelte';
  import { getCookie } from '$lib/utils/utilCookie';
  import { BASE_URL } from '../../../config';

  // Получение event_id из параметров маршрута
  export let event_id: string = $page.params.event_id;

  // Список участников
  let participants: { name: string; date: string; time: string }[] = [];

  // Функция для получения данных статистики мероприятия
  async function fetchStatistics(eventId: string) {
    try {
      const token = getCookie('auth_token'); // Получаем токен из localStorage
      if (!token) {
        throw new Error('Токен не найден, необходимо авторизоваться');
      }

      const response = await fetch(`${BASE_URL}/event_members/${eventId}`, {
        method: 'GET',
        headers: {
          'Authorization': `${token}`, // Добавляем токен в заголовок
        },
      });

      if (!response.ok) {
        throw new Error('Не удалось загрузить данные статистики');
      }

      const data = await response.json();

      // Преобразуем данные в формат name, date, time
      participants = data.map((item: { name: string; time_of_registration: string }) => {
        const registrationDate = new Date(item.time_of_registration);
        return {
          name: item.name,
          date: registrationDate.toLocaleDateString(), // Локализованная дата
          time: registrationDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) // Локализованное время
        };
      });
    } catch (error) {
      console.error('Ошибка при загрузке статистики:', error);
    }
  }

  // Загружаем данные при загрузке страницы
  fetchStatistics(event_id);
</script>

<Icon id="logo" />

<div class="page-background">
  <h1>Участники мероприятия</h1>

  <div class="subheading">Участники</div>

  <!-- Перебираем список участников -->
  {#if participants.length > 0}
    {#each participants as participant}
      <div class="participant-panel">
        <div class="name-container">
          <p class="name">{participant.name}</p>
        </div>
        <div class="date-time-container">
          <p class="date-time">{participant.date}</p>
          <p class="date-time">{participant.time}</p>
        </div>
      </div>
    {/each}
  {:else}
    <p style="font-size: 32px;">Данные отсутствуют или загружаются...</p>
  {/if}
</div>

<style scoped>
  .page-background {
    display: flex;
    margin-top: 50px;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    box-sizing: border-box;
    height: 100%;
    background-color: #171615; /* Переносим фон сюда */
    color: white; /* Переносим цвет текста сюда */
    font-family: "Inter", sans-serif; /* Переносим шрифт сюда */
  }

  h1 {
    font-size: 48px;
    margin-bottom: 40px;
    text-align: center;
    font-family: 'Press Start 2P', monospace;
    text-transform: uppercase;
  }

  .subheading {
    font-size: 32px;
    margin-bottom: 20px;
    align-self: flex-start;
    padding-left: 20px;
    font-weight: bolder;
  }

  .participant-panel {
    height: 45px;
    width: 95%;
    background-color: #444444;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .name-container {
    display: inline-block;
    padding: 0px 20px;
    background-color: #171615;
    border-radius: 16px;
    width: 20%;
    overflow: hidden; /* Обрезка содержимого, выходящего за границы */
    white-space: normal; /* Разрешаем перенос строк */
    word-wrap: break-word; /* Переносим слова при необходимости */
    word-break: break-word; /* Гарантируем перенос длинных слов */
  }

  .name {
    font-size: 18px;
    font-weight: bold;
    color: white;
    text-align: center; /* Центрируем текст для лучшего отображения */
  }

  .date-time-container {
    display: flex;
  }

  .date-time {
    font-size: 16px;
    color: white;
    text-align: center;
    padding: 5px 15px;
    border: 2px solid white;
    border-radius: 30px;
    margin-right: 15px;
    background-color: transparent;
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 36px;
      margin-bottom: 30px;
    }

    .subheading {
      font-size: 24px;
      padding-left: 10px;
    }

    .participant-panel {
      padding: 10px;
      gap: 5px;
    }

    .name-container {
      width: 50%; /* Увеличиваем ширину на телефонах */
      font-size: 16px; /* Уменьшаем шрифт */
    }

    .name {
      font-size: 14px;
    }

    .date-time {
      font-size: 14px;
      padding: 5px 10px;
    }
  }

  @media (max-width: 480px) {
    h1 {
      font-size: 28px;
      margin-bottom: 20px;
    }

    .subheading {
      font-size: 20px;
      padding-left: 5px;
    }

    .participant-panel {
      padding: 10px;
    }

    .name-container {
      width: 70%; /* Еще больше увеличиваем ширину для маленьких экранов */
      font-size: 14px;
    }

    .name {
      font-size: 12px;
    }

    .date-time {
      font-size: 12px;
      padding: 5px 8px;
    }
  }
</style>
