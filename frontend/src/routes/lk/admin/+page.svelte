<script lang="ts">
  import { goto } from '$app/navigation'; // Для навигации
  import { onMount } from 'svelte'; // Для загрузки данных после монтирования компонента
  import { BASE_URL } from '../../../config';
  import { eraseCookie, getCookie } from '$lib/utils/utilCookie';

  interface Event {
    event_id: number;
    event_name: string;
  }

  interface UserInfo {
    user_id: number;
    telegram_id: string;
    name: string;
    email: string;
    telephone_number: string;
    course: number;
    university_group: string;
  }

  let events: Event[] = [];
  let userInfo: UserInfo | null = null;
  let error: string | null = null;

  async function fetchEvents() {
    try {
      const response = await fetch(`${BASE_URL}/events`);
      if (!response.ok) {
        throw new Error('Не удалось загрузить данные мероприятий');
      }
      const data: Event[] = await response.json();
      events = data;
    } catch (err) {
      console.error('Ошибка при получении данных мероприятий:', err);
      error = 'Ошибка при загрузке мероприятий';
    }
  }

  async function fetchUserInfo() {
    try {
      const authToken = getCookie('auth_token');
      if (!authToken) {
        throw new Error('Не найден токен авторизации');
      }

      const response = await fetch(`${BASE_URL}/users_info`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error('Не удалось загрузить данные пользователя');
      }
      const data: UserInfo = await response.json();
      userInfo = data;
    } catch (err) {
      console.error('Ошибка при получении данных пользователя:', err);
      error = 'Ошибка при загрузке данных пользователя';
    }
  }

  function viewStatistics(eventId: number) {
    goto(`/analytics/${eventId}`);
  }

  function editEvent(eventId: number) {
    goto(`/edit_event/${eventId}`);
  }

  function logout() {
    eraseCookie('auth_token'); // Удаление токена из localStorage
    goto('/'); // Перенаправление на страницу входа
  }

  onMount(() => {
    fetchEvents();
    fetchUserInfo();
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
        {#if userInfo}
          <div class="title">{userInfo.name}</div>
          <div class="subtitle">{userInfo.email}</div>
        {:else if error}
          <div class="error">{error}</div>
        {:else}
          <div class="title">Загрузка...</div>
          <div class="subtitle">Пожалуйста, подождите</div>
        {/if}
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

      {#if events.length > 0}
  {#each events as event}
    <div 
      class="event" 
      on:click={() => goto(`/event/${event.event_id}`)}
    >
      <div class="event-name-panel">
        <div class="event-name">{event.event_name}</div>
      </div>
      <div class="buttons">
        <button 
          class="stats-btn" 
          on:click={(e) => {
            e.stopPropagation(); // Остановить всплытие события
            viewStatistics(event.event_id);
          }}
        >
          Статистика
        </button>
        <button 
          class="edit-btn" 
          on:click={(e) => {
            e.stopPropagation(); // Остановить всплытие события
            editEvent(event.event_id);
          }}
        >
          Редактировать
        </button>
      </div>
    </div>
  {/each}
{:else if error}
  <p class="error">{error}</p>
{:else}
  <p>Загрузка мероприятий...</p>
{/if}

    </div>
  </div>
</div>

<style>
  /* Глобальные стили для всей страницы */
  .app-container {
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 100%;
    padding: 0px;
    background-image: url('/backgroundlkuser.png');
    min-height: 100vh;
    background-size: cover;
    background-position: center кcenter;
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
    width: 80px; /* Уменьшен размер */
    height: 80px; /* Уменьшен размер */
    border-radius: 40px;
    background-image: url('/Profile.png');
    background-size: contain;
    background-position: center;
    margin-right: 10px;
    box-shadow: 0 0 10px 3px rgba(1, 199, 232, 0.4), 0 0 20px 7px rgba(79, 189, 46, 0.4);
  }
  
  .title {
    font-size: 48px; /* Уменьшен размер шрифта */
    font-weight: bold;
    margin: 0;
    margin-left: 25px;
  }
  
  .subtitle {
    font-size: 24px; /* Уменьшен размер шрифта */
    color: #888;
    margin: 0;
    margin-left: 25px;
  }
  
  .logout-btn {
    margin-left: 20px;
    margin-bottom: 25px;
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
    font-size: 36px; /* Уменьшен размер шрифта */
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
  }
  
  .buttons-right {
    display: flex;
    gap: 10px;
    margin-top: 5px;
    height: 45px;
  }
  
  .archive-btn {
    background: transparent; /* Прозрачный фон */
    color: white; /* Белый текст */
    text-align: center;
    padding: 5px 35px;
    font-size: 20px;
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
    border: white;
  }
  
  .create-btn:hover {
    filter: brightness(1.1); /* Увеличение яркости при наведении */
  }
  
  .event {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(36, 36, 35, 0.8); /* Прозрачный фон */
    padding: 10px; /* Уменьшен отступ */
    border-radius: 15px; /* Уменьшено закругление */
    margin-bottom: 12px; /* Уменьшено расстояние */
    height: 60px; /* Уменьшена высота */
    width: 90%;
    border: #838383 solid 1px;
    cursor: pointer; /* Изменение курсора на указатель */

  }
  
  .event-name-panel {
    background-color: #171615;
    width: 50%;
    height: 80%; /* Уменьшена высота панели */
    padding: 5px 10px; /* Уменьшен внутренний отступ */
    border-radius: 15px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    overflow: hidden;
  }
  
  .event-name {
    font-size: 20px; /* Уменьшен размер шрифта */
    font-weight: normal;
    color: white;
    word-wrap: break-word; /* Перенос длинных слов */
    word-break: break-word; /* Разрывы слов для предотвращения выхода за пределы */
  }
  
  .buttons {
    display: flex;
    gap: 15px; /* Уменьшено расстояние между кнопками */
  }
  
  button {
    padding: 10px 12px; /* Уменьшены внутренние отступы */
    font-size: 16px; /* Уменьшен размер шрифта кнопок */
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
    right: 78px;
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
    .title {
      font-size: 36px; /* Для мобильных устройств */
    }
    .subtitle {
      font-size: 20px;
    }
    .profile-icon {
      width: 60px; /* Уменьшен для мобильных */
      height: 60px;
    }
    .events-header h2 {
      font-size: 30px;
    }
    .event {
      height: 50px;
    }
    .event-name {
      font-size: 16px;
    }
    .buttons {
      gap: 10px;
    }
    button {
      font-size: 14px;
      padding: 8px 10px;
    }
  }
  
  @media (max-width: 480px) {
    .title {
      font-size: 24px;
    }
    .subtitle {
      font-size: 16px;
    }
    .profile-icon {
      width: 50px;
      height: 50px;
    }
    .event {
      height: 40px;
    }
    .event-name {
      font-size: 12px;
    }
    .buttons {
      gap: 8px;
    }
    button {
      font-size: 12px;
      padding: 8px 10px;
    }
  }
</style>

