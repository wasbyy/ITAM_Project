<script lang="ts">
  let events = [
      { id: 1, name: "Мероприятие 1" },
      { id: 2, name: "Мероприятие 2" },
      { id: 3, name: "Мероприятие 3" },
      { id: 4, name: "Мероприятие 4" },
  ];

  function viewStatistics(eventId: number) {
      alert(`Просмотр статистики для мероприятия ID: ${eventId}`);
  }

  function editEvent(eventId: number) {
      alert(`Редактирование мероприятия ID: ${eventId}`);
  }

  function createEvent() {
      alert("Создание нового мероприятия");
  }
</script>

<style>
/* Глобальные стили для всей страницы */
:global(html, body) {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  height: 100%;
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
}

.create-btn:hover {
  filter: brightness(1.1); /* Увеличение яркости при наведении */
}

.event {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #444444;
  padding: 15px; /* Уменьшен отступ */
  border-radius: 21px;
  margin-bottom: 12px; /* Уменьшено расстояние между панелями */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 80px; /* Уменьшена высота */
  width: 90%;
}

.event-name-panel {
  background-color: black;
  width: 60%;
  height: 80%; /* Высота на всю панель мероприятия */
  padding: 8px 15px; /* Уменьшен внутренний отступ */
  border-radius: 21px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.event-name {
  font-size: 28px; /* Уменьшен размер шрифта */
  font-weight: normal;
  color: white;
}

.buttons {
  display: flex;
  gap: 26px; /* Уменьшено расстояние между кнопками */
}

button {
  padding: 15px 17px; /* Уменьшен внутренний отступ кнопок */
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
</style>

<div class="container">
  <!-- Логотип -->
  <a href="http://localhost:5173/mainpage">
    <img src="/itam_logo.png" alt="Логотип" class="logo" />
  </a>
  
  <!-- Header -->
  <div class="header">
    <div class="profile-icon"></div>
    <div>
      <div class="title">Имя Пользователя</div>
      <div class="subtitle">Почта</div>
    </div>
  </div>

  <!-- Events Section -->
  <div class="events-list">
    <div class="events-header">
      <h2>МЕРОПРИЯТИЯ</h2>
      <div class="buttons-right">
        <!-- Ссылка для перехода в архив -->
        <a href="http://localhost:5173/archive">
          <button class="archive-btn">АРХИВ</button>
        </a>
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div class="create-btn" on:click={createEvent}>+</div>
      </div>
    </div>
    {#each events as event}
    <div class="event">
      <div class="event-name-panel">
        <div class="event-name">{event.name}</div>
      </div>
      <div class="buttons">
        <button class="stats-btn" on:click={() => viewStatistics(event.id)}>Статистика</button>
        <button class="edit-btn" on:click={() => editEvent(event.id)}>Редактировать</button>
      </div>
    </div>
    {/each}
  </div>
</div>
