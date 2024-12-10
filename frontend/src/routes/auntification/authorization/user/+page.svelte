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
    margin: -8px;
    padding: 0;
    font-family: "Inter", sans-serif;
    background-color: #171615; /* Темный фон */
    color: white; /* Белый текст */
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  /* Стили для контейнера входа */
  .login-container {
    position: relative;
    background: #1a1a1a;
    border-radius: 20px;
    padding: 2rem;
    width: 400px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6); /* Тень */
    border: 2px solid #2ecc71; /* Обводка панели */
  }

  .login-container::before {
    content: "";
    position: absolute;
    top: -3px;
    left: -3px;
    right: -3px;
    bottom: -3px;
    background: linear-gradient(135deg, #00ff00, #1db954, #00ff99, #2ecc71);
    background-size: 300% 300%;
    border-radius: 23px;
    z-index: -1;
    animation: greenGradient 3s ease infinite;
  }

  @keyframes greenGradient {
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

  .btn {
    position: relative;
    background: linear-gradient(45deg, #00ff99, #1db954, #2ecc71, #00ff00dc);
    background-size: 300% 300%;
    padding: 1rem 1.5rem;
    color: white;
    border-radius: 20px;
    font-size: 1.1rem;
    border: none;
    width: 50%;
    animation: buttonGradient 3s linear infinite;
    transition: all 0.3s ease;
    font-weight: 100;
    font-size: 20px;
    margin-top: 0%;
  }

  @keyframes buttonGradient {
    0% {
      background-position: 0% 0%;
    }
    50% {
      background-position: 100% 100%;
    }
    100% {
      background-position: 0% 0%;
    }
  }

  .btn:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0, 255, 0, 0.5);
  }

  .btn:active {
    transform: scale(0.95);
    box-shadow: 0 4px 10px rgba(0, 255, 0, 0.3);
  }

  .register-text {
    margin-top: 1rem;
    margin-bottom: -0.3rem;
    font-size: 0.9rem;
    color: #e0e0e0;
    cursor: pointer;
    color: #01c47692;
  }

  .register-text:hover {
    color: #00ff99;
  }
  .register-text {
  background: none; /* Убирает фоновый цвет */
  border: none; /* Убирает границы */
  color: inherit; /* Наследует цвет текста от родителя */
  font: inherit; /* Наследует шрифт от родителя */
  cursor: pointer; /* Указывает, что элемент кликабельный */
  padding: 0; /* Убирает внутренние отступы */
  color: #2ecc71;
}

.register-text:hover {
  text-decoration: none; /* Убирает подчёркивание при наведении */
}

.register-text:focus {
  outline: none; /* Убирает стандартный контур при фокусе */
}

  @media (max-width: 768px) {
    /* Уменьшаем размеры контейнера и элементов */
    .login-container {
      width: 80%; /* Уменьшаем ширину контейнера */
      padding: 1.5rem; /* Уменьшаем отступы внутри */
    }

    .login-container h1 {
      font-size: 1.5rem; /* Уменьшаем размер заголовка */
      margin-top: 0; /* Убираем лишний отступ сверху */
      margin-bottom: 1rem; /* Уменьшаем отступ снизу */
    }

    .login-container input {
      padding: 0.8rem; /* Уменьшаем внутренний отступ */
      font-size: 0.9rem; /* Уменьшаем размер шрифта */
    }

    .btn {
      padding: 0.8rem 1.2rem; /* Уменьшаем отступы на кнопке */
      font-size: 1rem; /* Уменьшаем размер шрифта на кнопке */
    }
  }
</style>
