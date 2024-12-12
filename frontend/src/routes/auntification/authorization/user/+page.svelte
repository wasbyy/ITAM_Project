<script lang="ts">
  import { goto } from "$app/navigation"; // Импортируем функцию goto
  import Icon from "$lib/components/Icon.svelte";
  import { setCookie } from "$lib/utils/utilCookie";
  let username: string = "";
  let password: string = "";
  let isLoading: boolean = false;  // Состояние загрузки
  let errorMessage: string | null = null;  // Состояние для ошибок
  import { BASE_URL } from "../../../../config";

  const handleLogin = async () => {
    errorMessage = null;  // Сбрасываем ошибку перед новой попыткой
    if (username && password) {
      isLoading = true; // Включаем индикатор загрузки

      try {
        const requestBody = new URLSearchParams({
          grant_type: "password",
          username: username,
          password: password,
          scope: "read write",
          client_id: "", 
          client_secret: "",
        }).toString();

        const response = await fetch(`${BASE_URL}/login/token`, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: requestBody,
        });

        const data = await response.json();

        if (response.ok) {
          setCookie("auth_token", data.access_token);
          goto("/lk/user"); // Переход на страницу после успешного входа
        } else {
          errorMessage = data.message || "Что-то пошло не так";
        }
      } catch (error) {
        errorMessage = "Ошибка при отправке данных: " + error.message;
      } finally {
        isLoading = false; // Отключаем индикатор загрузки
      }
    } else {
      errorMessage = "Заполните все поля!";
    }
  };

  // Обработчик для перехода на страницу регистрации
  const goToRegistration = () => {
    goto("/auntification/registration");
  };
</script>

<Icon id="logo" />

<div class="page-container">
  <div class="login-container">
    <h1 class="title">Вход</h1>
    <input type="text" placeholder="Почта" bind:value={username} />
    <input type="password" placeholder="Пароль" bind:value={password} />
    
    <!-- Показ ошибки -->
    {#if errorMessage}
      <div class="error-message">{errorMessage}</div>
    {/if}

    <!-- Кнопка с индикатором загрузки -->
    <button class="btn" on:click={handleLogin} disabled={isLoading}>
      {#if isLoading}
        <span class="spinner"></span> Загрузка...
      {:else}
        Войти
      {/if}
    </button>
    
    <div class="register-text" on:click={goToRegistration}>
      Зарегистрироваться
    </div>
  </div>
</div>

<style>

  /* Стили для общего контейнера */
  .page-container {
    padding: 0;
    font-family: "Inter", sans-serif;
    background-color: #171615; /* Темный фон */
    color: white; /* Белый текст */
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url("/authUser.png");
    background-size: cover;
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
    font-weight:8 00;
    
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

  .btn {
    position: relative;
    background: transparent; /* Прозрачный фон */
    color: white; /* Белый текст */
    border: 2px solid rgb(203, 203, 203); /* Белая обводка */
    padding: 1rem 1.5rem;
    border-radius: 20px;
    font-size: 1.1rem;
    width: 50%;
    transition: all 0.3s ease;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "Font Over", sans-serif;

  }

  .btn:disabled {
    background-color: #444444;
    cursor: not-allowed;
  }

  .btn:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 10px rgba(255, 255, 255, 0.3);
  }

  .btn:active {
    transform: scale(0.95);
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.3);
  }

  .register-text {
    margin-top: 0.7rem;
    margin-bottom: -0.5rem;
    font-size: 0.9rem;
    color: #e0e0e0;
    cursor: pointer;
    color: #7826ca;
    
  }

  .register-text:hover {
    color: #8a29eb92;
  }

  .register-text:focus {
    outline: none;
  }

  /* Стили для ошибки */
  .error-message {
    color: red;
    font-size: 0.9rem;
    margin-top: 1rem;
  }

  /* Индикатор загрузки (спиннер) */
  .spinner {
    border: 3px solid #f3f3f3; /* Светлый фон спиннера */
    border-top: 3px solid #3498db; /* Синий цвет для верхней части */
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite; /* Анимация вращения */
    margin-right: 10px; /* Расстояние между спиннером и текстом */
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

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
