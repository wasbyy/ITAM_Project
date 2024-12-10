<script lang="ts">
  import { goto } from '$app/navigation'; // Для навигации
  import { onMount } from 'svelte'; // Для загрузки данных после монтирования компонента
  import { BASE_URL } from '../../../config';
  
  interface Event {
    event_id: number;
    event_name: string;
  }

  let events: Event[] = [];

  async function fetchEvents() {
    try {
      const response = await fetch(`${BASE_URL}/events`);
      if (!response.ok) {
        throw new Error('Не удалось загрузить данные');
      }
      const data: Event[] = await response.json();
      events = data;
    } catch (error) {
      console.error('Ошибка при получении данных:', error);
    }
  }

  function viewStatistics(eventId: number) {
    goto(`/analytics/${eventId}`);
  }

  function editEvent(eventId: number) {
    goto(`/edit_event/${eventId}`);
  }

  function logout() {
    localStorage.removeItem('auth_token'); // Удаление токена из localStorage
    goto('/'); // Перенаправление на страницу входа
  }

  onMount(() => {
    fetchEvents();
  });
</script>

<div class="app-container">

<div class="container">
  <a href="/">
    <img src="/itam_logo.png" alt="Логотип" class="logo" />
  </a>

  <div class="header">
    <div class="profile-icon"></div>
    <div>
      <div class="title">Имя Пользователя</div>
      <div class="subtitle">Почта</div>
    </div>
    <button class="logout-btn" on:click={logout}>Выйти</button>
  </div>

  <div class="events-list">
    <div class="events-header">
      <h2>МЕРОПРИЯТИЯ</h2>
      <div class="buttons-right">
        <button class="archive-btn" on:click={() => goto('/archieve/admin')}>АРХИВ</button>
        <button class="create-btn" on:click={() => goto('/add_event')}>+</button>
      </div>
    </div>

    {#each events as event}
    <div class="event">
      <div class="event-name-panel">
        <div class="event-name">{event.event_name}</div>
      </div>
      <div class="buttons">
        <button class="stats-btn" on:click={() => viewStatistics(event.event_id)}>Статистика</button>
        <button class="edit-btn" on:click={() => editEvent(event.event_id)}>Редактировать</button>
      </div>
    </div>
    {/each}
  </div>
</div>
</div>

<style>/* Глобальные стили для всей страницы */
.app-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        height: 100%;
        padding: 20px;
        background-color: #171615; /* Черный фон для всей страницы */
        color: white;
        font-family: "Inter", sans-serif;
    }
  
  .container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    padding: 20px;
  }
  
  .header {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
    padding-left: 4%;
    margin-top: 1.5%;
  }
  
  .profile-icon {
    width: 105px;
    height: 105px;
    border-radius: 50px;
    background-image: url('/Profile.png'); /* Добавление изображения */
    background-position: center; /* Центрирование изображения */
    margin-right: 15px;
    margin-top: 5px;
    box-shadow: 0 0 15px 5px rgba(1, 199, 232, 0.4), 0 0 30px 10px rgba(79, 189, 46, 0.4); /* Градиентное свечение */
  }
  
  .title {
    font-size: 64px;
    font-weight: bold;
    margin: 0;
    margin-left: 38px;
  }
  
  .subtitle {
    font-size: 32px;
    color: #888;
    margin: 0;
    margin-left: 38px;
  }
  
  .events-list {
    flex-grow: 1;
    margin-top: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
  }
  
  .events-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 92%; /* Общая ширина */
    margin-bottom: 15px;
  }
  
  .events-header h2 {
    font-size: 48px;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
  }
  
  .buttons-right {
    display: flex;
    gap: 10px;
    margin-top: 15px;
  }
  
  .archive-btn {
    background: transparent; /* Прозрачный фон */
    color: white; /* Белый текст */
    text-align: center;
    padding: 10px 50px;
    font-size: 24px;
    font-weight: 100;
    border: 2px solid #444444; /* Белый контур */
    border-radius: 40px; /* Овальная форма */
    cursor: pointer;
  }
  
  .archive-btn:hover {
    background: rgba(255, 255, 255, 0.1); /* Прозрачный белый фон при наведении */
  }
  
  .create-btn {
    background: linear-gradient(90deg, #01C7E8, #4FBD2E); /* Линейный градиент */
    color: white;
    border-radius: 50px;
    padding: 10px 40px;
    font-size: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    border: white ;
  }
  
  .create-btn:hover {
    filter: brightness(1.1); /* Увеличение яркости при наведении */
  }
  
  .event {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #242423;
    padding: 15px; /* Уменьшен отступ */
    border-radius: 21px;
    margin-bottom: 12px; /* Уменьшено расстояние между панелями */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    height: 80px; /* Уменьшена высота */
    width: 90%;
    border: #444444 solid;
  }
  
  .event-name-panel {
    background-color: #171615;
    width: 50%;
    height: 75%; /* Высота на всю панель мероприятия */
    padding: 8px 15px; /* Уменьшен внутренний отступ */
    border-radius: 21px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    overflow: hidden;
  }
  
  .event-name {
    font-size: 28px; /* Уменьшен размер шрифта */
    font-weight: normal;
    color: white;
    word-wrap: break-word; /* Перенос длинных слов */
    word-break: break-word; /* Разрывы слов для предотвращения выхода за пределы */
  }
  
  .buttons {
    display: flex;
    gap: 26px; /* Уменьшено расстояние между кнопками */
  }
  
  button {
    padding: 15px 17px; /* Уменьшены внутренние отступы кнопок */
    font-size: 20px; /* Уменьшен размер шрифта кнопок */
    border: 2px solid white;
    background: transparent;
    color: white;
    border-radius: 40px;
    cursor: pointer;
  }
  
  .stats-btn:hover {
    background: rgba(26, 188, 156, 0.1);
  }
  
  .edit-btn:hover {
    background: rgba(52, 152, 219, 0.1);
  }
  
  .logo {
    position: absolute;
    top: 50px;
    right: 80px;
    width: 100px; /* Размер логотипа */
    height: auto;
    cursor: pointer;
    z-index: 1000; /* Поверх всего контента */
  }
  
  /* Адаптивные стили для мобильных устройств */
  @media (max-width: 768px) {
    .logo {
    position: absolute;
    top: 20px;
    right: 40px;
    
  }
    /* Заголовки */
    .title {
      font-size: 40px;
    }
  
    .subtitle {
      font-size: 24px;
    }
  
    .events-header h2 {
      font-size: 36px;
    }
  
    /* Стили для кнопок */
    .archive-btn {
      font-size: 20px;
      padding: 8px 30px;
    }
  
    .create-btn {
      font-size: 24px;
      padding: 8px 30px;
    }
  
    /* Уменьшение размеров панели мероприятий */
    .event {
      padding: 12px;
      height: 70px;
      margin-bottom: 10px;
    }
  
    .event-name {
      font-size: 22px;
    }
  
    .event-name-panel {
      padding: 5px 12px;
    }
  
    .buttons {
      gap: 12px;
    }
  
    button {
      padding: 12px 15px;
      font-size: 16px;
    }
  }
  
  @media (max-width: 480px) {
    /* Уменьшаем размер шрифта и расстояния для самых маленьких экранов */
    .title {
      font-size: 32px;
      margin-top: 80px;
    }
    .profile-icon {
    margin-top: 70px;
    width: 60px;
    height: 50px;
    background-size: cover;
  }
  
    .subtitle {
      font-size: 20px;
    }
  
    .events-header h2 {
      font-size: 24px;
    }
  
    .archive-btn {
      font-size: 14px;
      padding: 8px 15px;
      margin-left: 10px;
    }
  
    .create-btn {
      font-size: 14px;
      padding: 10px 10px;
    }
  
    .event {
      padding: 10px;
      height: 60px;
      margin-bottom: 8px;
    }
  
    .event-name {
      font-size: 14px;
    }
  
    .event-name-panel {
      padding: 5px 10px;
    }
  
    .buttons {
      gap: 8px;
    }
  
    button {
      padding: 7px 10px;
      font-size: 10px;
    }
  }
  .logout-btn {
    margin-left: 20px;
    margin-bottom: 30px;
    background: transparent;
    border: 2px solid #444444;
    color: white;
    padding: 8px 18px;
    font-size: 20px;
    border-radius: 30px;
    cursor: pointer;
  }

  .logout-btn:hover {
    background: rgba(255, 255, 255, 0.1);
  }
</style>
