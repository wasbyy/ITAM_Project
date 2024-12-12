<script lang="ts">
  import Icon from "$lib/components/Icon.svelte";

  // Функция для обработки нажатия кнопок
  const handleButtonClick = (role: "participant" | "admin") => {
    const button = document.querySelector(`.glow-on-hover.${role}`); // Находим кнопку по классу
    if (button) {
      button.classList.add("active"); // Добавляем класс активности
      setTimeout(() => {
        button.classList.remove("active"); // Убираем класс через 100ms
        // Переход на соответствующую страницу
        const url =
          role === "participant"
            ? "/auntification/authorization/user"
            : "/auntification/authorization/admin";
        window.location.href = url;
      }, 100); 
    }
  };
</script>
<style>
  /* Основной контейнер */
  .container {
    background-image: url("/select.png");
    background-repeat: no-repeat;
    background-size: cover;
    height: 100vh; /* Занимает весь экран */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    overflow: hidden;
    margin-bottom: 100px;
  }

  .background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('/background_Selectrole.png') no-repeat center center / cover;
    filter: brightness(1.1);
    z-index: -1;
  }

  /* Контейнер для кнопок, чтобы они оставались по центру */
  .buttons-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 3rem; /* Увеличенное расстояние между кнопками */
    position: relative;
    z-index: 1; /* Обеспечим, чтобы кнопки были поверх фона */
  }

  /* Общий стиль для кнопок */
  .glow-on-hover {
    width: 500px;
    height: 90px;
    padding: 25px;
    border: 3px solid white;
    outline: none;
    background: white;
    cursor: pointer;
    position: relative;
    z-index: 0;
    border-radius: 50px;
    font-size: 34px;
    font-family: "Font Over";
    font-weight: 400;
    color: white;
    display: flex; /* Flexbox для центрирования */
    justify-content: center; /* Центрирование по горизонтали */
    text-align: center; /* Выравнивание текста */
  }

  /* Эффект при наведении для кнопки участника (смена цветов) */
  .participant:hover:before {
    background: linear-gradient(45deg, #5b75f3, #8e5be7, #f066e3, #ff3f89); /* Яркие оттенки розового, фиолетового и синего */
    opacity: 1;
  }

  .glow-on-hover.participant:hover span {
    background: transparent;
  }

  /* Эффект при наведении для кнопки админа (смена цветов) */
  .glow-on-hover.admin:hover {
    background: linear-gradient(45deg, #0AE1B0, #09D5BC, #06BBD9); /* Зеленый градиент для админа */
  }

  .glow-on-hover.admin:hover span {
    background: transparent;
  }

  /* Анимация нажатия */
  .glow-on-hover:active {
    transform: scale(0.9); /* Уменьшаем кнопку */
    transition: transform 0.4s ease; /* Плавное уменьшение */
  }

  /* Анимация для градиентного текста */
  @keyframes gradient-text-animation {
    0% { background-position: 0 0; }
    50% { background-position: 400% 0; }
    100% { background-position: 0 0; }
  }

  /* Градиентный фон кнопок */
  .participant:before, .admin:before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    background-size: 400%;
    z-index: -1;
    filter: blur(3px);
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    opacity: 0;
    transition: opacity .3s ease-in-out;
    border-radius: 50px; /* Более закругленные края */
  }

  /* Подсветка для участника (смена цветов) */
  .participant:hover:before {
    background: linear-gradient(45deg, #73A1FB, #9F89F0, #BE79E9, #F15FDE); /* Оранжево-розовый для участника */
    opacity: 1;
  }

  /* Подсветка для админа (смена цветов) */
  .admin:hover:before {
    background: linear-gradient(45deg, #0AE1B0, #09d576, #06d2d9); /* Зеленый и бирюзовый для админа */
    opacity: 1;
  }

  .glow-on-hover:after {
    z-index: -1;
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: #111;
    left: 0;
    top: 0;
    border-radius: 50px; /* Более закругленные края */
  }

  @media (max-width: 768px) {
    /* Уменьшаем размер кнопок и шрифта на мобильных устройствах */
    .glow-on-hover {
      width: 300px;
      height: 60px;
      font-size: 24px;
      padding: 15px;
    }

    /* Изменяем контейнер кнопок на вертикальный */
    .buttons-container {
      flex-direction: column;
      gap: 2rem;
    }

    /* Уменьшаем размеры фона и скрываем некоторые элементы на малых экранах */
    .background {
      filter: brightness(1);
    }

    /* Дополнительные стили для мобильного фона */
    .container {
      background-size: cover;
      height: auto;
      min-height: 100vh;
      margin-bottom: 0;
    }
  }
</style>
  <div class="container">
    <!-- Первый фон -->
    <div class="background"></div>
    <Icon id="logo"/>
  
    <div class="buttons-container">
      <button
        class="glow-on-hover participant"
        on:click={() => handleButtonClick("participant")}
      >
        <span>я участник</span>
      </button>
      <button
        class="glow-on-hover admin"
        on:click={() => handleButtonClick("admin")}
      >
        <span>я организатор</span>
      </button>
    </div>
    
  </div>
  