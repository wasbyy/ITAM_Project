<script lang="ts">
  import { goto } from "$app/navigation";
    import Icon from "$lib/components/Icon.svelte";
    let username: string = '';
    let password: string = '';
    import { BASE_URL } from "../../../../config";

    const handleLogin = async () => {
        console.log('handleLogin called');

        if (username && password) {
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
                    localStorage.setItem('auth_token', data.access_token);
                    goto('/lk/admin')
                } else {
                    console.log('Error:', data.message || 'Что-то пошло не так');
                }
            } catch (error) {
                console.error('Ошибка при отправке данных:', error);
            }
        } else {
            console.log('Заполните все поля!');
        }
    };
</script>

<style>
.page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Занимает всю высоту страницы */
}

/* Контейнер для обводки */
.border-container {
  position: relative;
  padding: 3px; /* Отступ для обводки */
  background: linear-gradient(135deg, #ff4cf0, #ff8c00, #ff0080, #ff4cf0); /* Градиент для обводки */
  border-radius: 20px; /* Радиус скругления обводки */
  z-index: 0; /* Убедитесь, что обводка будет под основной панелью */
}

.login-container {
  position: relative;
  background: #1a1a1a; /* Цвет панели */
  border-radius: 20px;
  padding: 2.5rem;
  width: 400px; /* Ширина контейнера */
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  z-index: 1; /* Панель будет поверх фонового градиента */
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
  background: linear-gradient(45deg, #D38312 10%, #A83279 90%);
  background-size: 200% 100%;
  padding: 1rem 1.5rem;
  color: white;
  border-radius: 20px;
  font-size: 1.1rem;
  border: none;
  width: 50%;
  animation: gradientAnimation 4s linear infinite;
  transition: all 0.3s ease;
  font-weight: 100;
  font-size: 20px;
}

@keyframes gradientAnimation {
  0% {
    background-position: 0 0;
  }
  50% {
    background-position: 100% 0;
  }
  100% {
    background-position: 0 0;
  }
}

.btn:hover {
  transform: scale(1.01);
  box-shadow: 0 4px 10px rgba(255, 255, 255, 0.15);
}

.btn:active {
  transform: scale(0.95);
  box-shadow: 0 2px 5px rgba(255, 255, 255, 0.1);
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

<Icon id="logo"/>
<div class="page-container">
  <!-- Контейнер для обводки -->
  <div class="border-container">
    <!-- Основная панель входа -->
    <div class="login-container">
      <h1 class="title">Вход</h1>
      <input type="text" placeholder="Логин" bind:value={username} />
      <input type="password" placeholder="Пароль" bind:value={password} />
      <button class="btn" on:click={handleLogin}>Войти</button>
    </div>
  </div>
</div>
