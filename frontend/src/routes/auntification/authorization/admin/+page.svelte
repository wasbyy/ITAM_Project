<script lang="ts">
  import { goto } from "$app/navigation";
  import Icon from "$lib/components/Icon.svelte";
  import { setCookie } from "$lib/utils/utilCookie";
  let username: string = '';
  let password: string = '';
  let isLoading: boolean = false;  // Состояние загрузки
  let errorMessage: string | null = null;  // Состояние для ошибок
  import { BASE_URL } from "../../../../config";

  const handleLogin = async () => {
    // Сброс ошибки перед новой попыткой
    errorMessage = null;
    if (username && password) {
      isLoading = true; // Включаем индикатор загрузки
      console.log('Credentials entered:', { username, password });

      try {
        // Кодируем данные в формате application/x-www-form-urlencoded
        const requestBody = new URLSearchParams({
          grant_type: 'password',
          username: username,
          password: password,
          scope: 'read write',  // Если scope не обязательное, можно оставить пустым или убрать
          client_id: '',        // Добавьте client_id, если это нужно
          client_secret: ''     // Добавьте client_secret, если это нужно
        }).toString();

        console.log('Sending request with body:', requestBody);  // Логируем тело запроса

        const response = await fetch(`${BASE_URL}/login/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',  // Указываем нужный заголовок
          },
          body: requestBody,  // Отправляем данные в теле запроса
        });

        console.log('Response status:', response.status); // Логируем статус ответа
        const data = await response.json();
        console.log('Response data:', data);

        if (response.ok) {
          console.log('Login successful:', data);
          setCookie("auth_token", data.access_token);
          goto('/lk/admin');  // Перенаправление на страницу после успешного входа
        } else {
          // Если сервер вернул ошибку, показываем сообщение об ошибке
          errorMessage = data.message || 'Неверный логин или пароль';
        }
      } catch (error) {
        console.error('Ошибка при отправке данных:', error);
        errorMessage = 'Не удалось выполнить запрос. Попробуйте позже.';
      } finally {
        isLoading = false;  // Отключаем индикатор загрузки после завершения запроса
      }
    } else {
      errorMessage = 'Заполните все поля!';
    }
  };
</script>

<Icon id="logo" />
<div class="page-container">
  <!-- Контейнер для обводки -->
  <div class="border-container">
    <!-- Основная панель входа -->
    <div class="login-container">
      <h1 class="title">Вход</h1>

      <!-- Поля для ввода логина и пароля -->
      <input type="text" placeholder="Почта" bind:value={username} />
      <input type="password" placeholder="Пароль" bind:value={password} />

      <!-- Уведомление об ошибке -->
      {#if errorMessage}
        <p class="error-message">{errorMessage}</p>
      {/if}

      <!-- Кнопка для отправки формы -->
      <button class="btn" on:click={handleLogin} disabled={isLoading}>
        {#if isLoading}
          Загрузка...
        {:else}
          Войти
        {/if}
      </button>
    </div>
  </div>
</div>

<style>
  .page-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url("/authAdm.png");
    background-position: center center;
    background-size: cover;
    position: relative;
  }

  /* Стили для контейнера входа */
  .login-container {
    position: relative;
    background: rgba(26, 26, 26, 0.8); /* Прозрачный фон с 80% непрозрачности */
    border-radius: 20px;
    padding: 2rem;
    width: 400px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6); /* Тень */
    border: 2px solid #666666; /* Обводка панели */
  }

  .login-container h1 {
    font-size: 2rem;
    margin-top: -0.5rem;
    margin-bottom: 2rem;
    color: #e0e0e0;
    font-weight: bold;
  }

  .login-container input {
    width: 100%;
    margin-bottom: 1rem;
    padding: 1rem;
    border-radius: 10px;
    border: none;
    outline: none;
    background: rgba(255, 255, 255, 0.1);
    color: #e0e0e0;
    font-size: 1rem;
    text-align: left;
    transition: background 0.3s ease;
  }

  .login-container input:focus {
    background: rgba(255, 255, 255, 0.2);
  }

  /* Кнопка с прозрачным фоном и белой обводкой */
  .btn {
    position: relative;
    background: transparent; /* Прозрачный фон */
    border: 2px solid white; /* Белая обводка */
    padding: 1rem 1.5rem;
    color: white;
    border-radius: 20px;
    font-size: 1.1rem;
    width: 50%;
    transition: all 0.3s ease;
    font-weight: 100;
    font-size: 20px;
    font-family: "Font Over";
  }

  /* Эффект при наведении */
  .btn:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 10px rgba(255, 255, 255, 0.3); /* Белая тень при наведении */
  }

  /* Эффект при нажатии */
  .btn:active {
    transform: scale(0.95); /* Уменьшение кнопки при нажатии */
    box-shadow: 0 2px 5px rgba(255, 255, 255, 0.1); /* Легкая тень */
  }

  /* Стили для сообщения об ошибке */
  .error-message {
    margin-bottom: 0.4rem;  /* Отступ снизу */
    color: red;
    font-size: 0.9rem;
  }

  /* Мобильная адаптация */
  @media (max-width: 768px) {
    .login-container {
      width: 80%;
      padding: 1.5rem;
    }

    .login-container h1 {
      font-size: 1.5rem;
      margin-top: 0;
      margin-bottom: 1rem;
    }

    .login-container input {
      padding: 0.8rem;
      font-size: 0.9rem;
    }

    .btn {
      padding: 0.8rem 1.2rem;
      font-size: 1rem;
    }
  }
</style>
