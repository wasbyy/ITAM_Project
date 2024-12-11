<script lang="ts">
  import { goto } from "$app/navigation"; // Импортируем функцию goto
  import Icon from "$lib/components/Icon.svelte";
  import { setCookie } from "$lib/utils/utilCookie";
  let username: string = "";
  let password: string = "";
  import { BASE_URL } from "../../../../config";

  const handleLogin = async () => {
    console.log("handleLogin called");

    if (username && password) {
      console.log("Credentials entered:", { username, password });

      try {
        // Кодируем данные в формате application/x-www-form-urlencoded
        const requestBody = new URLSearchParams({
          grant_type: "password",
          username: username,
          password: password,
          scope: "read write", // Если scope не обязательное, можно оставить пустым или убрать
          client_id: "", // Добавьте client_id, если это нужно
          client_secret: "", // Добавьте client_secret, если это нужно
        }).toString();

        console.log("Sending request with body:", requestBody); // Логируем тело запроса

        const response = await fetch(`${BASE_URL}/login/token`, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded", // Указываем нужный заголовок
          },
          body: requestBody, // Отправляем данные в теле запроса
        });

        console.log("Response status:", response.status); // Логируем статус ответа
        const data = await response.json();
        console.log("Response data:", data);

        if (response.ok) {
          console.log("Login successful:", data);
          setCookie("auth_token", data.access_token);
          goto("/lk/user"); // Переход по маршруту
        } else {
          console.log("Error:", data.message || "Что-то пошло не так");
        }
      } catch (error) {
        console.error("Ошибка при отправке данных:", error);
      }
    } else {
      console.log("Заполните все поля!");
    }
  };

  // Обработчик для перехода на страницу регистрации
  const goToRegistration = () => {
    goto("/auntification/registration"); // Переход по маршруту
  };
</script>
<Icon id="logo" />

<div class="page-container">
  <div class="login-container">
    <h1 class="title">Вход</h1>
    <input type="text" placeholder="Логин" bind:value={username} />
    <input type="password" placeholder="Пароль" bind:value={password} />
    <button class="btn" on:click={handleLogin}>Войти</button>
    <button class="register-text" on:click={goToRegistration}>
      Зарегистрироваться
    </button>
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



  @keyframes greenGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
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

  /* Стили для кнопки Войти */
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
  }

  .btn:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 10px rgba(255, 255, 255, 0.3); /* Белая тень при наведении */
  }

  .btn:active {
    transform: scale(0.95);
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.3); /* Белая тень при клике */
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

  .register-text {
    background: none;
    border: none;
    color: inherit;
    font: inherit;
    cursor: pointer;
    padding: 0;
    color: #5e1da8
  }

  .register-text:hover {
    text-decoration: none;
  }

  .register-text:focus {
    outline: none;
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
