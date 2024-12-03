<script lang="ts">
  import { onMount } from 'svelte';

  interface Event {
    event_id: number;
    event_name: string;
    short_description: string;
    place: string;
    tags: string;
    image_url?: string; // URL изображения в виде Blob
  }

  let events: Event[] = [];

  const fetchEventImage = async (eventId: number): Promise<string> => {
    const url = `http://130.193.52.139:8000/show_event_image/${eventId}`;
    try {
      console.log(`Запрос на получение изображения для мероприятия ${eventId}...`);
      const response = await fetch(url, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error(`Ошибка загрузки изображения: ${response.status} ${response.statusText}`);
      }

      const blob = await response.blob(); // Получаем потоковые данные как Blob
      const imageUrl = URL.createObjectURL(blob); // Создаем объект URL для изображения
      console.log(`Изображение для мероприятия ${eventId} успешно загружено`);
      return imageUrl;
    } catch (error) {
      console.error(`Ошибка загрузки изображения для мероприятия ${eventId}:`, error);
      return 'https://via.placeholder.com/540x270'; // Заглушка
    }
  };

  const loadEvents = async () => {
    try {
      console.log('Запрос к серверу для получения мероприятий...');
      const response = await fetch('http://130.193.52.139:8000/events', {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Не удалось загрузить мероприятия');
      }

      const data = await response.json();
      if (Array.isArray(data)) {
        events = await Promise.all(
          data.map(async (event) => {
            const imageUrl = await fetchEventImage(event.event_id);
            return { ...event, image_url: imageUrl };
          })
        );
        console.log('Мероприятия успешно загружены:', events);
      } else {
        console.error('Полученные данные имеют неправильную структуру:', data);
      }
    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
    }
  };

  onMount(() => {
    console.log('Компонент монтируется, загружаем мероприятия...');
    loadEvents();
  });

  const authorisation = () => {
    window.location.href = "http://localhost:5173/selectrole"; 
  };
</script>


<style>
  /* Стили для глобальных элементов страницы */
  :global(body) {
    margin: 0; /* Убираем отступы */
    padding: 0; /* Убираем внутренние отступы */
    background: #171615; /* Цвет фона страницы */
    overflow-x: hidden; /* Отключаем горизонтальную прокрутку */
    font-family: "Inter", sans-serif; /* Устанавливаем шрифт для страницы */
  }

  /* Контейнер для главной страницы */
  .container {
    position: relative; /* Контейнер позиционируется относительно родителя */
    height: 100vh; /* Высота контейнера — 100% от высоты экрана */
    width: 100vw; /* Ширина контейнера — 100% от ширины экрана */
    display: flex; /* Используем flexbox для удобного выравнивания */
    flex-direction: column; /* Элементы внутри контейнера выстраиваются по вертикали */
    align-items: center; /* Выравниваем элементы по центру по горизонтали */
    justify-content: center; /* Выравниваем элементы по центру по вертикали */
    text-align: center; /* Выравниваем текст по центру */
    overflow: hidden; /* Прячем все, что выходит за пределы контейнера */
  }

  /* Фон для страницы */
  .background {
    position: absolute; /* Абсолютное позиционирование для фонового изображения */
    top: 0; /* Прикрепляем к верхней части */
    left: 0; /* Прикрепляем к левой части */
    width: 100%; /* Задаем ширину на весь экран */
    height: 100%; /* Задаем высоту на весь экран */
    background: url('/background.png') no-repeat center center / cover; /* Загружаем фоновое изображение */
    filter: brightness(1.1); /* Немного увеличиваем яркость фона */
    z-index: -1; /* Фон будет находиться позади всех остальных элементов */
  }

  /* Панель сверху страницы с логотипом и кнопкой "Вход" */
  .top-bar {
    position: absolute; /* Абсолютное позиционирование для верхней панели */
    top: 20px; /* Отступ сверху */
    width: 100%; /* Панель занимает всю ширину страницы */
    display: flex; /* Используем flexbox для выравнивания элементов */
    align-items: center; /* Выравниваем элементы по вертикали */
    justify-content: space-between; /* Равномерно распределяем логотип и кнопку */
    padding: 0 20px; /* Отступы по бокам */
    color: white; /* Цвет текста на панели */
    font-size: 1rem; /* Размер шрифта */
    text-transform: uppercase; /* Преобразуем текст в верхний регистр */
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
    font-family: 'Press Start 2P', monospace; /* Шрифт в стиле ретро */
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
  width: 85%; /* Ограничиваем ширину карточек до 85% */
  display: grid; /* Используем CSS Grid */
  grid-template-columns: repeat(2, 1fr); /* Два столбца одинаковой ширины */
  gap: 20px; /* Отступы между карточками */
  justify-content: center; /* Центрируем сетку по горизонтали */
}

/* Стиль для каждой карточки мероприятия */
.event-card {
  background: #252525; /* Темный фон для карточки */
  border-radius: 10px; /* Скругленные углы */
  display: flex; /* Используем flexbox внутри карточки */
  flex-direction: row; /* Изображение слева, информация справа */
  padding: 20px; /* Отступы внутри карточки */
  color: white; /* Белый цвет текста */
  position: relative; /* Для размещения градиентной рамки */
  overflow: hidden; /* Прячем содержимое, выходящее за границы */
  z-index: 1; /* Поверх градиента */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4); /* Легкая тень */
}


/* Градиентная рамка */
.event-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 165, 0, 0.7), rgba(255, 99, 71, 0.7), rgba(255, 69, 0, 0.7), rgba(255, 165, 0, 0.7)); /* Оранжево-красный градиент */
  background-size: 300% 300%; /* Размер фона для анимации */
  border-radius: 10px; /* Совпадает с радиусом карточки */
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


</style>
<div class="container">
  <div class="background"></div>
  <div class="top-bar">
    <div class="logo">
      <img src="/itam_logo.png" alt="Логотип" />
    </div>
    <button class="login-btn" onclick={authorisation}>Вход</button>
  </div>
  <div class="title">Мероприятия</div>
</div>

<!-- Страница мероприятий -->
<div class="gray-background">
  <div class="event-cards">
    <!-- Перебор мероприятий с помощью Svelte -->
    {#each events as event (event.event_id)}
      <div class="event-card">
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
          {#each event.tags.split(' ') as tag}
            <span class="tag">{tag}</span>
          {/each}
        </div>
      </div>
    {/each}
  </div>
</div>