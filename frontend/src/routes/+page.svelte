<script lang="ts">
  import { onMount } from "svelte";
  import { BASE_URL } from "../config";
  import { goto } from "$app/navigation";
  import { getCookie } from "$lib/utils/utilCookie";
  
  interface Event {
    event_id: number;
    event_name: string;
    short_description: string;
    place: string;
    tags: string;
    image_url?: string;
    date: string;
  }

  let events: Event[] = [];
  let isAuthenticated = false;
  let userRole: string | null = null;
  let isRoleLoaded = false;
  let isLoading = true;

  const loadEvents = async () => {
  try {
    const response = await fetch(`${BASE_URL}/events`);
    if (!response.ok) throw new Error("Не удалось загрузить мероприятия");
    const data: Event[] = await response.json();

    events = await Promise.all(
      data.map(async (event) => ({
        ...event,
        image_url: await (async () => {
          try {
            const imgResponse = await fetch(`${BASE_URL}/show_event_image/${event.event_id}`);
            if (!imgResponse.ok) throw new Error("Не удалось загрузить изображение");
            const blob = await imgResponse.blob();
            return URL.createObjectURL(blob);
          } catch {
            return "https://avatars.mds.yandex.net/i?id=166c32386ec148d145f75f850da055e2298d59d7-12472594-images-thumbs&n=13"; // Плейсхолдер
          }
        })(),
      }))
    );

    // Сортируем мероприятия по event_id (по возрастанию)
    events.sort((a, b) => a.event_id - b.event_id);
  } catch (error) {
    console.error("Ошибка загрузки данных мероприятий:", error);
  } finally {
    isLoading = false;
  }
};

  const getUserRole = async () => {
    try {
      const token = getCookie("auth_token");
      if (!token) throw new Error("Необходима авторизация");

      const response = await fetch(`${BASE_URL}/user_role`, {
        headers: { Authorization: `${token}` },
      });

      if (!response.ok) throw new Error("Ошибка при получении роли пользователя");
      userRole = await response.text();
    } catch (error) {
      console.error("Ошибка получения роли:", error);
      userRole = null;
    } finally {
      isRoleLoaded = true;
    }
  };

  onMount(async () => {
    isAuthenticated = !!getCookie("auth_token");
    await loadEvents();
    if (isAuthenticated) await getUserRole();
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
          on:click={() => goto(userRole === '"admin"' ? "/lk/admin" : userRole === '"user"' ? "/lk/user" : "/error")}
        >
          Профиль
        </button>
      {:else}
        <button class="login-btn" on:click={() => goto("/auntification/selectrole")}>Вход</button>
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
          <div class="event-card" on:click={() => goto(`/event/${event.event_id}`)}>
            <img src={event.image_url} alt="Фото мероприятия" />
            <div class="info">
              <h3>{event.event_name}</h3>
              <p>{event.short_description}</p>
              <div class="details">
                <span>{event.place}</span>
                <span>{new Date(event.date).toLocaleDateString()}</span>              
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
<footer class="footer">
  <div class="footer-container">
    <div class="footer-logo">
      <img src="/itam_logo.png" alt="Логотип ITAM" />
      <p>2024</p>
    </div>
    <div class="footer-credits">
      <div class="footer-role">
        <p>Frontend</p>
        <p>@Wasbyy</p>
      </div>
      <div class="footer-role">
        <p>Backend</p>
        <p>@dontpaniczy</p>
      </div>
      <div class="footer-role">
        <p>Design</p>
        <p>@aantaars</p>
        <p>@kisssssssik</p>
        <p>@thePolishaz3</p>
      </div>
    </div>
  </div>
</footer>

</div>


<style>

.page{
    display: flex;
    flex-direction: column;
  }
  .container {
  position: relative; /* Для управления абсолютным позиционированием внутри */
  height: 100vh; /* Высота контейнера — 100% от высоты экрана */
  width: 100vw; /* Ширина контейнера — 100% от ширины экрана */
  display: flex; /* Используем flexbox для выравнивания */
  align-items: center; /* Выравниваем элементы по вертикали */
  justify-content: center; /* Выравниваем элементы по горизонтали */
  text-align: center; /* Текст будет выравнен по центру */
  overflow: hidden; /* Прячем содержимое за пределами контейнера */
}

.title {
  position: relative; /* Не используем абсолютное позиционирование */
  font-size: 85px; /* Размер шрифта заголовка */
  color: white; /* Белый цвет текста */
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.4); /* Тень для текста */
  text-transform: uppercase; /* Преобразуем текст в верхний регистр */
  font-family: "Press Start 2P", monospace; /* Шрифт в стиле ретро */
  z-index: 1; /* Заголовок над фоном */
}


  /* Фон для страницы */
/* Фон для страницы */
.background {
  position: absolute; /* Абсолютное позиционирование для фонового изображения */
  top: 0px; /* Прикрепляем к верхней части */
  left: 0; /* Прикрепляем к левой части */
  width: 100%; /* Задаем ширину на весь экран */
  height:100%; /* Минимальная высота — 100% от высоты экрана, чтобы фон не обрезался */
  background: url("/background.png");
  background-size: cover;
  background-position: center ;
  filter: brightness(1.1); /* Немного увеличиваем яркость фона */
  z-index: 0; /* Фон будет находиться позади всех остальных элементов */
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
    margin-right: 3rem; /* Отступ справа */
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




  /* Стиль для "страницы" мероприятий */
  .gray-background {
    width: 100%; /* Задаем ширину 100% */
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
  background: rgba(37, 37, 37, 0.6); /* Уменьшаем прозрачность */
  border-radius: 30px; /* Скругленные углы */
  display: flex; /* Используем flexbox внутри карточки */
  flex-direction: row; /* Изображение слева, информация справа */
  padding: 20px; /* Отступы внутри карточки */
  color: white; /* Белый цвет текста */
  position: relative; /* Для размещения градиентной рамки */
  overflow: hidden; /* Прячем содержимое, выходящее за границы */
  z-index: 1; /* Поверх градиента */
  transition: transform 0.2s ease-in-out, background 0.3s ease; /* Плавный переход для трансформации и фона */
  border: #838383 solid 1px;
  backdrop-filter: blur(10px); /* Размытие заднего фона */
}

.event-card:hover {
  transform: scale(1.03); /* Увеличиваем карточку на 5% при наведении */
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6); /* Увеличиваем тень при наведении */
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
    width: 90%;
    margin: 0; /* Убираем отступы */
    font-size: 32px; /* Устанавливаем больший размер шрифта */
    color: #fff; /* Белый цвет текста */
    font-weight: bold; /* Полужирное начертание */
    align-self: flex-start; /* Выравниваем заголовок по левому краю */
    letter-spacing: 1px; /* Увеличиваем расстояние между буквами */
  }

  /* Контейнер для тегов */
  .event-card .tags {
  position: absolute; /* Абсолютное позиционирование */
  top: 20px; /* Отступ сверху */
  right: 20px; /* Отступ справа */
  display: flex; /* Используем flexbox для выравнивания тегов */
  flex-direction: row; /* Теги будут располагаться в строку */
  gap: 10px; /* Отступы между тегами */
  justify-content: flex-start; /* Выравнивание по верхнему краю */
  align-items: center; /* Выравнивание по правому краю */
}

  /* Стили для каждого тега */
  .event-card .tags .tag {
    font-size: 12px; /* Размер шрифта тегов */
    
    color: #c4c4c4; /* Оранжевый цвет для тегов */
    background: #333; /* Темный фон для тегов */
    padding: 5px 10px; /* Отступы внутри тега */
    border-radius: 20px; /* Скругленные углы */
    text-transform: uppercase; /* Верхний регистр для тегов */
    cursor: pointer; /* Курсор в виде руки */
    transition: background 0.3s; /* Плавный переход при наведении */
  }

  /* Эффект при наведении на тег */
  .event-card .tags .tag:hover {
    background: #797979; /* Изменение фона при наведении */
    color: #252525; /* Цвет текста при наведении */
  }
  .profile-btn {
    display: block; /* Изначально будем показывать кнопку профиля, если есть токен */
  }
  .loading-indicator{
    color: white;
    font-size: 20px;
  }

  /* Медиа-запросы для мобильных устройств */
  @media (max-width: 768px) {
    .footer-container {
      flex-direction:row; /* Выстраиваем элементы вертикально */
      align-items: center; /* Центрируем элементы */
      height: auto; /* Автоматическая высота */
    }

    .footer-logo {
      align-items: center; /* Центрируем логотип */
    }

    .footer-credits {
      flex-direction: row; /* Выстраиваем роли вертикально */
      gap: 10px; /* Отступы между ролями */
    }

    .footer-role {
      align-items: center; /* Центрируем роли */
      font-size: 12px; /* Уменьшаем размер шрифта */
    }
    .footer-logo img {
  width: 60px; /* Ширина логотипа */
  margin-bottom: 10px;
}
    
    .top-bar {
      flex-direction: column;
      align-items: flex-start;
      padding: 10px;
    }

    .title {
      font-size: 50px;
    }

    .event-cards {
      grid-template-columns: 1fr;
      gap: 15px;
    }

    .event-card {
      flex-direction: column;
      padding: 15px;
    }

    .event-card img {
      width: 150px;
      height: 150px;
      margin-right: 0;
      margin-bottom: 15px;
    }

    .event-card .info h3 {
      font-size: 24px;
    }

    .event-card .details {
      font-size: 16px;
      margin-bottom: 10px;
    }

    .login-btn,
    .profile-btn {
      font-size: 1rem;
      padding: 5px 10px;
      height: 35px;
    }

    .logo img {
      height: 50px;
    }
  }

  @media (max-width: 480px) {

    .background{
      background-image: url("/background(full).png");
      background-position: center center;
      background-size: 430px;
      background-repeat: no-repeat;    
    }
    .gray-background{
      background-size: contain;
      background-position: center top;
    }
    .title {
      font-size: 24px;
    }
    
    .event-cards{
      gap: 20px; 
    }
    .event-card {
      padding: 10px;
    }

    .event-card .info h3 {
      font-size: 20px;
    }

    .event-card .details {
      font-size: 14px;
    }

    .top-bar {
    flex-direction: row; /* Горизонтальное расположение */
    justify-content: space-between; /* Логотип слева, кнопка справа */
    align-items: center; /* Центрируем элементы по вертикали */
    padding-top: 5%; /* Отступы сверху и по бокам */
    margin-left: 10px;
    width: 100%;
  }


  .logo img {
    height: 40px; /* Подгоняем размер логотипа */
    width: auto;
  }

  .login-btn,
  .profile-btn {
    width: auto; /* Автоматическая ширина */
    height: 35px; /* Уменьшаем высоту кнопок */
    font-size: 1rem; /* Уменьшаем размер текста */
    padding: 5px 15px; /* Отступы внутри кнопки */
  }

    .event-card .tags .tag {
      font-size: 10px;
      padding: 4px 8px;
    }
    .footer-logo img {
      margin-right: 10px;
      width: 40px; /* Уменьшаем размер логотипа */

    }

    .footer-role {
      font-size: 9px; /* Еще меньший шрифт */
    }
    .footer{
      margin: -10px -20px;
    }
  }
  .footer {
  color: #e0e0e0; /* Светло-серый текст */
  padding: 20px 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  border-top: 1px solid #838383; /* Серая полоска */

}

.footer-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
  max-width: 1200px;
  height: 175px;
}

.footer-logo {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.footer-logo img {
  width: 80px; /* Ширина логотипа */
  margin-bottom: 10px;
}

.footer-credits {
  display: flex;
  gap: 40px;
}

.footer-role {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.footer-role p:first-child {
  color: #a0a0a0; /* Серый цвет для ролей */
  font-size: 14px;
  margin-bottom: 5px;
}

</style>
