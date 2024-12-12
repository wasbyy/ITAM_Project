<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { BASE_URL } from "../../../config";
    import Icon from "$lib/components/Icon.svelte";
    import { eraseCookie, getCookie } from "$lib/utils/utilCookie";
    import { formatDateTime } from "$lib/utils/utilTime";
  
    type Event = {
      event_id: number;
      event_name: string;
      date: string;
    };
  
    type UserInfo = {
      user_id: number;
      name: string;
      email: string;
      telephone_number: string;
      course: number;
      university_group: string;
    };
  
    export let data: { events: Event[]; error?: string; loading?: boolean };
  
    let userInfo: UserInfo | null = null;
    let error: string | null = null;
  
    const authToken = getCookie("auth_token");
  
    async function fetchUserInfo() {
      if (!authToken) {
        error = "Токен аутентификации не найден";
        return;
      }
  
      try {
        const response = await fetch(`${BASE_URL}/users_info`, {
          method: "GET",
          headers: {
            Authorization: `${authToken}`,
            "Content-Type": "application/json",
          },
        });
  
        if (!response.ok) {
          const { message } = await response.json();
          throw new Error(message || "Не удалось получить данные пользователя");
        }
  
        userInfo = await response.json(); // Сохраняем полученные данные
      } catch (err) {
        error = err.message || "Произошла ошибка при получении данных";
      }
    }
  
    function logout(): void {
      eraseCookie("auth_token");
      goto("/");
    }
  
    function goToArchive(): void {
      if (authToken) {
        goto(`/archieve/user/`);
      } else {
        goto("/");
        console.error("Токен не найден");
      }
    }
  
    onMount(fetchUserInfo); // Получаем данные пользователя при монтировании компонента
  </script>
  
  <div class="global-container">
    <div class="container">
        <a href="/">
            <img src="/itam_logo.png" alt="Логотип" class="logo" />
        </a>
        <div class="header">
            <div class="profile-container">
                <div class="profile-glow"></div>
                <div class="profile-image"></div>
            </div>
            <div>
                {#if userInfo}
                    <div class="title">{userInfo.name}</div>
                {:else if error}
                    <div class="error">{error}</div>
                {:else}
                    <div class="title">Загрузка...</div>
                    <div class="subtitle">Пожалуйста, подождите</div>
                {/if}
            </div>
            <!-- Кнопка выхода -->
            <button class="logout-btn" on:click={logout}>Выйти</button>
        </div>

        <!-- Новый раздел "Данные" -->
        <div class="data-section">
            <h2>Данные</h2>
            <div class="data-panels">
                {#if userInfo}
                    <div class="data-panel">{userInfo.telephone_number}</div>
                    <div class="data-panel">{userInfo.email}</div>
                    <div class="data-panel">{userInfo.course} курс {userInfo.university_group}</div>
                {:else}
                    <div class="data-panel">Загрузка данных...</div>
                {/if}
            </div>
        </div>

        <!-- Events Section -->
        <div class="events-list">
            <div class="events-header">
                <h2>МЕРОПРИЯТИЯ</h2>
                <button class="archive-btn" on:click={goToArchive}>АРХИВ</button>
            </div>

            {#if data.loading}
                <p>Загрузка мероприятий...</p>
            {:else if data.error}
                <p class="error">Ошибка: {data.error}</p>
            {:else if data.events.length === 0}
                <p>Нет мероприятий</p>
            {:else}
            {#each data.events as event}
                <!-- svelte-ignore a11y_no_static_element_interactions -->
                <!-- svelte-ignore a11y_click_events_have_key_events -->
                <div class="event" on:click={() => goto(`/event/${event.event_id}`)}>
                    <div class="event-name-panel">
                        <div class="event-name">{event.event_name}</div>
                    </div>
                    <div class="buttons">
                        <button class="time-btn">{formatDateTime(event.date).formattedTime}</button>
                        <button class="date-btn">{formatDateTime(event.date).formattedDate}</button>
                    </div>
                </div>
            {/each}
        
            {/if}
        </div>
    </div>
    
</div>

<style>
  /* Стили для глобального контейнера */
  .global-container {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    height: 100%;
    background-color: #171615; /* Черный фон для всей страницы */
    color: white;
    font-family: "Inter", sans-serif;
    background-image: url('/backgroundlkuser.png');
    min-height: 100vh;
    background-size: cover;
    background-position: center кcenter;
  }

  .container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
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

  .profile-container {
    position: relative; /* Для размещения дочерних элементов слоями */
    width: 105px;
    height: 105px;
  }

  .profile-glow {
    position: absolute;
    top: 1px;
    left: 2px;
    width: 70%;
    height: 70%;
    border-radius: 50%; /* Идеальный круг */
    box-shadow:
      inset 0 0 25px rgba(255, 255, 255, 0.7),
      inset 20px 0 40px rgba(249, 89, 218, 0.7),
      inset -20px 0 40px rgba(206, 111, 228, 0.7),
      inset 20px 0 150px rgba(154, 139, 240, 0.7),
      inset -20px 0 150px rgba(108, 162, 251, 0.7),
      0 0 5px rgba(249, 89, 218, 0.6),
      -8px 0 15px rgba(206, 111, 228, 0.6),
      8px 0 15px rgba(108, 162, 251, 0.6),
      0px 0 20px rgba(154, 139, 240, 0.6);
    z-index: 1; /* Под иконкой профиля */
    margin-top: 15px;

  }

  .profile-image {
  position: absolute;
  width: 80px;
  height: 75px;
  border-radius: 50%; /* Идеальный круг */
  background-image: url("/Profile.png"); /* Добавление изображения */
  background-position: center; /* Центрирование изображения */
  background-size: cover;
  z-index: 2; /* Поверх свечения */
  margin-top: 15px;
  overflow: hidden; /* Чтобы затемнение не выходило за пределы круга */
}

.profile-image::after {
  content: ''; /* Создаем пустой псевдоэлемент */
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2); /* Черный с прозрачностью для затемнения */
  border-radius: 50%; /* Закругляем псевдоэлемент, чтобы он совпал с формой изображения */
  z-index: 1; /* Находится ниже изображения */
}

  .title {
    font-size: 60px;
    font-weight: bold;
    margin: 0;
    margin-left: 10px;
  }

  .subtitle {
    font-size: 28px;
    color: #888;
    margin: 0;
    margin-left: 18px;
  }

  .events-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-top: 20px;
    /* Убираем ограничение на прокрутку, теперь вся страница будет прокручиваться */
  }

  .events-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 92%; /* Общая ширина */
    margin-bottom: 15px;
  }

  .events-header h2 {
    font-size: 36px;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
  }

  .archive-btn {
    background: transparent; /* Прозрачный фон */
    color: white; /* Белый текст */
    text-align: center;
    padding: 10px 50px;
    font-size: 22px;
    font-weight: bolder;
    border: 2px solid #636363; /* Белый контур */
    border-radius: 40px; /* Овальная форма */
    cursor: pointer;
    text-decoration: none; /* Убираем подчеркивание */
  }

  .archive-btn:hover {
    background: rgba(
      255,
      255,
      255,
      0.1
    ); /* Прозрачный белый фон при наведении */
  }

  .event {
    cursor: pointer; /* Изменение курсора на указатель при наведении на мероприятие */
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #242423;
    padding: 10px; /* Уменьшен отступ */
    border-radius: 21px;
    margin-bottom: 17px; /* Уменьшено расстояние между панелями */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    height: 60px; /* Уменьшена высота */
    width: 90%;
    border: #444444 solid;
    background: rgba(36, 36, 35, 0.8); /* Прозрачный фон */
    border: #838383 solid 1px;


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
  }

  .event-name {
    font-size: 24px; /* Уменьшен размер шрифта */
    font-weight: normal;
    color: white;
  }

  .buttons {
    display: flex;
    gap: 26px; /* Уменьшено расстояние между кнопками */
  }

  button {
    padding: 10px 17px; /* Уменьшен внутренний отступ кнопок */
    font-size: 18px; /* Уменьшен размер шрифта кнопок */
    border: 2px solid white;
    background: transparent;
    color: white;
    border-radius: 40px;
    cursor: pointer;
  }

  .time-btn:hover {
    background: rgba(26, 188, 156, 0.1);
  }

  .date-btn:hover {
    background: rgba(52, 152, 219, 0.1);
  }

  /* Стиль для нового раздела "Данные" */
  .data-section {
    margin-left: 4%;
    margin-bottom: 30px;
    text-align: left;
  }

  .data-section h2 {
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 20px;
  }

  .data-panels {
    display: flex;
    justify-content: left;
    gap: 20px;
  }

  .data-panel {
    position: relative; /* Для псевдоэлемента */
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px 25px; /* Внутренние отступы */
    font-size: 24px;
    font-weight: bold;
    color: white;
    background-color: #171615; /* Фон панели */
    border-radius: 50px; /* Скруглённые углы */
    z-index: 1; /* Выше псевдоэлемента */
    text-align: center;
    min-width: 200px; /* Минимальная ширина панели */
  }

  .data-panel::before {
    content: ""; /* Пустое содержимое */
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: inherit; /* Наследуем скруглённые углы */
    padding: 2px; /* Ширина рамки */
    background: linear-gradient(
      90deg,
      #f859da,
      #d56ce3,
      #a684ee,
      #a684ee
    ); /* Градиент рамки */
    -webkit-mask:
      linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0); /* Маска для видимости только рамки */
    -webkit-mask-composite: xor; /* XOR для видимости только границ */
    mask-composite: exclude; /* То же самое для стандартных браузеров */
    z-index: -1; /* Позади панели */
  }
  @media (max-width: 480px) {
    /* Уменьшаем шрифт заголовков */
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

  .events-header h2 {
    font-size: 36px; /* Уменьшен размер шрифта */
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
  }

    .event-name {
      font-size: 18px;
      padding: 5px;
    }

    .buttons button {
      font-size: 12px;
      padding: 8px 10px;
    }

    .event {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #242423;
    padding: 5px; /* Уменьшен отступ */
    border-radius: 15px; /* Уменьшено закругление */
    margin-bottom: 12px; /* Уменьшено расстояние */
    height: 60px; /* Уменьшена высота */
    width: 90%;
    border: 1px solid #444444;
  }
  
  .event-name-panel {
    background-color: #171615;
    width: 50%;
    height: 60%; /* Уменьшена высота панели */
    padding: 5px 50px; /* Уменьшен внутренний отступ */
    border-radius: 15px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    overflow: hidden;
  }

    .buttons {
      flex-direction: row; /* Кнопки вертикально */
      gap: 10px;
      justify-content: space-between;
    }

    /* Уменьшаем размер иконки профиля */
    .profile-container {
      width: 80px;
      height: 80px;
    }

    .profile-image {
      width: 80px;
      height: 80px;
    }

    /* Уменьшаем размеры панелей с данными */
    .data-panel {
      font-size: 18px;
      min-width: 150px; /* Уменьшаем минимальную ширину */
      padding: 10px 15px;
    }

    .data-panels {
      flex-direction: column;
      gap: 10px;
    }

    /* Уменьшаем размер кнопки архива */
    .archive-btn {
      font-size: 18px;
      padding: 8px 20px;
    }

    /* Изменения для контейнера и основного блока */
    .container {
      padding: 10px;
    }

    .header {
      margin-top: 10px;
      padding-left: 0;
      flex-direction: column;
      align-items: center;
      margin-right: 20px;
    }

    .events-list {
      padding: 0;
    }
  }
  .logout-btn {
    margin-left: 20px;
    margin-top: 15px;
    background: transparent;
    border: 2px solid #444444;
    color: white;
    padding: 10px 20px;
    font-size: 20px;
    border-radius: 30px;
    cursor: pointer;
  }


  .logout-btn:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  .logo{
    width: 100px;
    position: absolute;
    right: 80px;
    top: 60px;
  }
  @media (max-width: 768px) {
  .logo {
    width: 80px;
    top: 20px;
    right: 20px;
  }
  .profile-glow {
    display: none;
  }
  .title {
    font-size: 48px;
  }

  .subtitle {
    font-size: 22px;
  }

  .profile-container {
    width: 80px;
    height: 80px;
    margin-bottom: 30px

  }

  .profile-image {
    width: 80px;
    height: 80px;

  }

  .events-header h2 {
    font-size: 28px;
  }

  .event-name {
    font-size: 18px;
  }

  .buttons button {
    font-size: 14px;
    padding: 6px 12px;
  }

  .event {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #242423;
    padding: 5px;
    border-radius: 15px;
    margin-bottom: 12px;
    height: 50px;
    width: 90%;
  }

  .event-name-panel {
    background-color: #171615;
    width: 50%;
    height: 70%;
    padding: 5px 10px;
    border-radius: 15px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    overflow: hidden;
  }

  .buttons {
    flex-direction: row;
    gap: 10px;
    justify-content: space-between;
  }

  .data-panel {
    font-size: 18px;
    min-width: 150px;
    padding: 10px 15px;
  }

  .data-panels {
    flex-direction: column;
    gap: 10px;
  }

  .archive-btn {
    font-size: 16px;
    padding: 6px 18px;
    margin-top: 10px;
  }

  .logout-btn {
    font-size: 18px;
    padding: 10px 20px;
    border-radius: 30px;
    cursor: pointer;
  }

}
</style>
