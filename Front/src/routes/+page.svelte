<script lang="ts">
  import { onMount } from "svelte";
  import { BASE_URL } from "../config";
  import { goto } from "$app/navigation";

  interface Event {
    event_id: number;
    event_name: string;
    short_description: string;
    place: string;
    tags: string;
    image_url?: string;
  }

  let events: Event[] = [];
  let isAuthenticated = false;
  let userRole: string | null = null;
  let isRoleLoaded = false;
  let isLoading = true;

  // Функция для получения изображения мероприятия
  const fetchEventImage = async (eventId: number): Promise<string> => {
    try {
      const response = await fetch(`${BASE_URL}/show_event_image/${eventId}`);
      if (!response.ok) throw new Error("Не удалось загрузить изображение");
      const blob = await response.blob();
      return URL.createObjectURL(blob);
    } catch (error) {
      console.error("Ошибка загрузки изображения:", error);
      return "https://via.placeholder.com/400x400"; // Плейсхолдер
    }
  };

  // Загрузка списка мероприятий
  const loadEvents = async () => {
    try {
      const response = await fetch(`${BASE_URL}/events`);
      if (!response.ok) throw new Error("Не удалось загрузить мероприятия");
      const data: Event[] = await response.json();
      events = await Promise.all(
        data.map(async (event) => ({
          ...event,
          image_url: await fetchEventImage(event.event_id),
        }))
      );
    } catch (error) {
      console.error("Ошибка загрузки данных мероприятий:", error);
    } finally {
      isLoading = false;
    }
  };
  $: {
    console.log(userRole);
  }
  // Получение роли пользователя
  const getUserRole = async () => {
    try {
      const token = localStorage.getItem("auth_token");
      if (!token) throw new Error("Необходима авторизация");

      const response = await fetch(`${BASE_URL}/user_role`, {
        headers: { Authorization: `${token}` },
      });

      if (!response.ok)
        throw new Error("Ошибка при получении роли пользователя");
      userRole = await response.text();
    } catch (error) {
      console.error("Ошибка получения роли:", error);
      userRole = null;
    } finally {
      isRoleLoaded = true;
    }
  };

  // Навигация в зависимости от роли
  const navigateToByRole = (role: string) => {
    const url =
      role === '"admin"'
        ? "/lk/admin"
        : role === '"user"'
          ? "/lk/user"
          : "/error";
    goto(url);
  };

  // Обработка клика на профиль
  // const handleProfileClick = async () => {
  //   if (!isRoleLoaded) {
  //     console.warn("Роль пользователя еще не загружена");
  //     return;
  //   }
  //   if (userRole) {
  //     navigateToByRole(userRole);
  //   } else {
  //     goto("/error");
  //   }
  // };

  // Обработка клика на карточку мероприятия
  const handleEventClick = (eventId: number) => {
    goto(`/event/${eventId}`);
  };

  // Загрузка данных при монтировании компонента
  onMount(async () => {
    isAuthenticated = !!localStorage.getItem("auth_token");
    await loadEvents();
    if (isAuthenticated) {
      await getUserRole();
    }
  });
</script>

<div class="page">
  <div class="container">
    <div class="background"></div>
    <div class="top-bar">
      <div class="logo">
        <img src="/itam_logo.png" alt="Логотип" />
      </div>
      {#if isAuthenticated && isRoleLoaded}
        <button
          class="profile-btn"
          on:click={() => navigateToByRole(userRole ? userRole : "")}
          >Профиль</button
        >
      {:else}
        <button
          class="login-btn"
          on:click={() => goto("/auntification/selectrole")}>Вход</button
        >
      {/if}
    </div>
    <h1 class="title">Мероприятия</h1>
  </div>

  <div class="gray-background">
    {#if isLoading}
      <div class="loading-indicator">Загрузка...</div>
    {:else if events.length === 0}
      <div class="no-events">Нет доступных мероприятий</div>
    {:else}
      <div class="event-cards">
        {#each events as event (event.event_id)}
          <!-- svelte-ignore a11y_click_events_have_key_events -->
          <!-- svelte-ignore a11y_no_static_element_interactions -->
          <div
            class="event-card"
            on:click={() => handleEventClick(event.event_id)}
          >
            <img src={event.image_url} alt="Фото мероприятия" />
            <div class="info">
              <h3>{event.event_name}</h3>
              <p>{event.short_description}</p>
              <div class="details">
                <span>{event.place}</span>
                <span>{event.event_id}</span>
                <span>{new Date().toLocaleDateString()}</span>
              </div>
            </div>
            <div class="tags">
              {#each event.tags.split(" ") as tag}
                <span class="tag">{tag}</span>
              {/each}
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  /* Стили для глобальных элементов страницы */
    :global(body) {
      margin: 0; /* Убираем отступы */
      padding: 0; /* Убираем внутренние отступы */
      background: #171615; /* Цвет фона страницы */
      overflow-x: hidden; /* Отключаем горизонтальную прокрутку */
      font-family: "Inter", sans-serif; /* Устанавливаем шрифт для страницы */
    }
  .page{
    display: flex;
    flex-direction: column;
  }
  /* Контейнер для главной страницы */
  .container { /* Контейнер позиционируется относительно родителя */
    height: 90vh; /* Высота контейнера — 100% от высоты экрана */
    width: 100vw; /* Ширина контейнера — 100% от ширины экрана */
    display: flex; /* Используем flexbox для удобного выравнивания */
    flex-direction: column; /* Элементы внутри контейнера выстраиваются по вертикали */
    align-items: center; /* Выравниваем элементы по центру по горизонтали */
    justify-content: center; /* Выравниваем элементы по центру по вертикали */
    text-align: center; /* Выравниваем текст по центру */
    overflow: hidden; /* Прячем все, что выходит за пределы контейнера */
    position: relative; /* Добавляем относительное позиционирование */
  }

  /* Фон для страницы */
  .background {
    position: absolute; /* Абсолютное позиционирование для фонового изображения */
    top: 0; /* Прикрепляем к верхней части */
    left: 0; /* Прикрепляем к левой части */
    width: 100%; /* Задаем ширину на весь экран */
    height: 100%; /* Задаем высоту на весь экран */
    background: url("/background.png") no-repeat center center / cover; /* Загружаем фоновое изображение */
    filter: brightness(1.1); /* Немного увеличиваем яркость фона */
    z-index: -1; /* Фон будет находиться позади всех остальных элементов */
  }

  /* Панель сверху страницы с логотипом и кнопкой "Вход" */
  /* Добавим стили для кнопки и иконки */
  .top-bar {
    position: absolute;
    top: 20px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    color: white;
    font-size: 1rem;
    text-transform: uppercase;
  }

  .login-btn,
  .profile-btn {
    margin-right: 2rem;
    margin-top: 0.4rem;
    border: 2px solid white;
    padding: 5px 15px;
    border-radius: 20px;
    cursor: pointer;
    background: transparent;
    font-size: 1.2rem;
    text-transform: uppercase;
    height: 40px;
    color: white;
  }

  .login-btn:hover,
  .profile-btn:hover {
    background: white;
    color: black;
  }

  .profile-btn {
    display: none; /* Изначально скрываем кнопку профиля */
  }

  /* Логотип */
  .logo {
    margin-left: 2rem; /* Отступ слева */
  }

  .logo img {
    height: 60px; /* Высота логотипа */
    width: auto; /* Ширина пропорциональна высоте */
    object-fit: contain; /* Сохраняем пропорции изображения */
  }

  /* Кнопка для входа */
  .login-btn {
    margin-right: 2rem; /* Отступ справа */
    margin-top: 0.4rem; /* Отступ сверху */
    border: 2px solid white; /* Белая рамка */
    padding: 5px 15px; /* Отступы внутри кнопки */
    border-radius: 20px; /* Скругленные углы */
    cursor: pointer; /* Курсор при наведении — указатель */
    background: transparent; /* Прозрачный фон */
    font-size: 1.2rem; /* Размер шрифта */
    text-transform: uppercase; /* Верхний регистр */
    width: 105px; /* Ширина кнопки */
    height: 40px; /* Высота кнопки */
    color: white; /* Белый цвет текста */
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.4); /* Тень для текста */
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.4); /* Легкая тень для кнопки */
  }

  .login-btn:hover {
    background: white; /* При наведении фон становится белым */
    color: black; /* Цвет текста становится черным */
  }

  /* Заголовок на главной странице */
  .title {
    font-size: 100px; /* Размер шрифта заголовка */
    color: white; /* Белый цвет текста */
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.4); /* Тень для текста */
    text-transform: uppercase; /* Преобразуем текст в верхний регистр */
    font-family: "Press Start 2P", monospace; /* Шрифт в стиле ретро */
  }

  /* Стиль для "страницы" мероприятий */
  .gray-background {
    width: 100%; /* Задаем ширину 100% */
    background: #171615; /* Цвет фона страницы */
    display: flex; /* Используем flexbox для выравнивания */
    justify-content: center; /* Центрируем содержимое по горизонтали */
    background-image: url(/backgroundBottom.png);
    background-size: cover;
  }

  /* Контейнер для карточек мероприятий */
  .event-cards {
    width: 95%; /* Ограничиваем ширину карточек до 85% */
    display: grid; /* Используем CSS Grid */
    grid-template-columns: repeat(2, 1fr); /* Два столбца одинаковой ширины */
    gap: 25px; /* Отступы между карточками */
    justify-content: center; /* Центрируем сетку по горизонтали */
    margin-bottom: 30px;
  }

  /* Стиль для каждой карточки мероприятия */
  .event-card {
    background: #252525; /* Темный фон для карточки */
    border-radius: 30px; /* Скругленные углы */
    display: flex; /* Используем flexbox внутри карточки */
    flex-direction: row; /* Изображение слева, информация справа */
    padding: 20px; /* Отступы внутри карточки */
    color: white; /* Белый цвет текста */
    position: relative; /* Для размещения градиентной рамки */
    overflow: hidden; /* Прячем содержимое, выходящее за границы */
    z-index: 1; /* Поверх градиента */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4); /* Легкая тень */
    transition: transform 0.2s ease-in-out; /* Плавный переход для трансформации */
  }

  .event-card:hover {
    transform: scale(1.03); /* Увеличиваем карточку на 5% при наведении */
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6); /* Увеличиваем тень при наведении */
  }

  /* Градиентная рамка */
  .event-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 165, 0, 0.7),
      rgba(255, 99, 71, 0.7),
      rgba(255, 69, 0, 0.7),
      rgba(255, 165, 0, 0.7)
    ); /* Оранжево-красный градиент */
    background-size: 300% 300%; /* Размер фона для анимации */
    border-radius: 30px; /* Совпадает с радиусом карточки */
    padding: 3px; /* Толщина обводки */
    -webkit-mask:
      linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0); /* Маска для создания рамки */
    mask:
      linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0);
    -webkit-mask-composite: exclude; /* Для удаления внутреннего содержимого */
    mask-composite: exclude;
    z-index: -1; /* Помещаем за карточкой */
    animation: circularGradient 15s linear infinite; /* Анимация движения */
  }

  /* Анимация кругового движения градиента */
  @keyframes circularGradient {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }

  /* Изображение мероприятия в карточке */
  .event-card img {
    width: 200px; /* Ширина изображения */
    height: 200px; /* Высота изображения */
    object-fit: cover; /* Масштабирование изображения с обрезкой */
    border-radius: 8px; /* Скругленные углы изображения */
    margin-right: 20px; /* Отступ справа для разделения с текстовой информацией */
  }

  /* Блок с информацией о мероприятии */
  .event-card .info {
    display: flex; /* Используем flexbox для вертикального выравнивания */
    flex-direction: column; /* Элементы располагаются по вертикали */
    justify-content: flex-end; /* Выровнять элементы по нижнему краю */
    gap: 10px; /* Отступы между блоками */
    flex-grow: 1; /* Позволяет этому блоку занимать оставшееся пространство */
  }

  /* Блок с деталями (время, дата, место) */
  .event-card .details {
    display: flex; /* Выравниваем элементы по горизонтали */
    justify-content: flex-start; /* Выравниваем элементы по правому краю */
    font-size: 22px; /* Размер шрифта */
    color: #aaa; /* Цвет текста */
    gap: 30px; /* Добавляем небольшой пробел между полями (время, дата, место) */
    margin-top: auto; /* Отталкиваем блок с деталями к низу карточки */
  }

  /* Стиль для заголовков мероприятий */
  .event-card .info h3 {
    margin: 0; /* Убираем отступы */
    font-size: 32px; /* Устанавливаем больший размер шрифта */
    color: #fff; /* Белый цвет текста */
    font-weight: bold; /* Полужирное начертание */
    align-self: flex-start; /* Выравниваем заголовок по левому краю */
    letter-spacing: 1px; /* Увеличиваем расстояние между буквами */
  }

  /* Контейнер для тегов */
  .event-card .tags {
    display: flex; /* Используем flexbox для выравнивания тегов */
    flex-direction: column; /* Теги будут располагаться в столбик */
    gap: 10px; /* Отступы между тегами */
    justify-content: flex-start; /* Выравнивание по верхнему краю */
    align-items: flex-start; /* Выравнивание по левому краю */
  }

  /* Стили для каждого тега */
  .event-card .tags .tag {
    font-size: 12px; /* Размер шрифта тегов */
    color: #f4a261; /* Оранжевый цвет для тегов */
    background: #333; /* Темный фон для тегов */
    padding: 5px 10px; /* Отступы внутри тега */
    border-radius: 20px; /* Скругленные углы */
    text-transform: uppercase; /* Верхний регистр для тегов */
    cursor: pointer; /* Курсор в виде руки */
    transition: background 0.3s; /* Плавный переход при наведении */
  }

  /* Эффект при наведении на тег */
  .event-card .tags .tag:hover {
    background: #f4a261; /* Изменение фона при наведении */
    color: #252525; /* Цвет текста при наведении */
  }
  .profile-btn {
    display: block; /* Изначально будем показывать кнопку профиля, если есть токен */
  }
  .loading-indicator{
    color: white;
    font-size: 20px;
  }
</style>
