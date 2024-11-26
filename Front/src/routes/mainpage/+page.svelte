<script>
  const authorisation = () => {
    window.location.href = "http://localhost:5173/selectrole"; 
  };
</script>

<style>
  /* Общий стиль страницы */
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'Press Start 2P', monospace;
    background: black;
    overflow-x: hidden; /* Запрещаем горизонтальную прокрутку */
  }

  /* Основной контейнер */
  .container {
    position: relative;
    height: 100vh; /* Занимает весь экран */
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    overflow: hidden;
  }

  /* Первый фоновый блок */
  .background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('/src/lib/components/background.png') no-repeat center center / cover;
    filter: brightness(1.1);
    z-index: -1;
  }

  

  /* Верхняя панель */
  .top-bar {
    position: absolute;
    top: 20px;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    color: white;
    font-size: 1rem;
    text-transform: uppercase;
  }

  /* Логотип */
  .logo {
    margin-left: 20px;
  }

  .logo img {
    height: 60px;
    width: auto;
    object-fit: contain;
  }

  /* Кнопка вход */
  .login-btn {
    margin-right: 2rem;
    border: 2px solid white;
    padding: 5px 15px;
    border-radius: 20px;
    cursor: pointer;
    background: transparent;
    font-size: 0.9rem;
    text-transform: uppercase;
    width: 80px;
    height: 35px;
    color: white;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
  }

  .login-btn:hover {
    background: white;
    color: black;
  }

  /* Заголовок */
  .title {
    font-size: 5.5rem;
    color: white;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
    text-transform: uppercase;
    font-family: 'Press Start 2P', monospace;
  }

  /* Стиль для контента после фона */
  .content {
    margin-top: 100px; /* Отступ от верхней части для прокрутки */
    color: white;
    font-size: 2rem;
    padding: 20px;
    background: #222;
    text-align: center;
  }

  /* Стиль для дополнительного контента, который будет прокручиваться */
  .scrollable-section {
    padding: 50px 0;
    background: #333;
    color: white;
    text-align: center;
  }

  .scrollable-section h2 {
    margin-bottom: 20px;
  }

  .scrollable-section p {
    font-size: 1.2rem;
  }

  html {
    scroll-behavior: smooth;
  }
</style>

<div class="container">
  <!-- Первый фон -->
  <div class="background"></div>

  <!-- Верхняя панель -->
  <div class="top-bar">
    <div class="logo">
      <img src="/src/lib/components/itam_logo.png" alt="Логотип" />
    </div>
    <button class="login-btn" onclick={authorisation}>Вход</button>
  </div>

  <!-- Заголовок -->
  <div class="title">Мероприятия</div>
</div>


<!-- Контент, который будет отображаться после второго фона -->
