<script lang="ts">
    import { goto } from '$app/navigation'; // SvelteKit
    import Icon from '$lib/components/Icon.svelte';
    import { BASE_URL } from '../../../config';
  
    // Поля формы
    let name: string = '';
    let email: string = '';
    let telegram_id: string = '';
    let password: string = '';
    let telephone_number: string = '';
    let course: string = '';
    let university_group: string = '';
  
    // Состояния
    let isLoading: boolean = false; // Для загрузки
    let notificationMessage: string = '';
    let notificationType: 'success' | 'error' | 'info' = 'info';
  
    // Функция уведомлений
    const showNotification = (message: string, type: 'success' | 'error' | 'info') => {
      notificationMessage = message;
      notificationType = type;
      setTimeout(() => {
        notificationMessage = '';
      }, 3000);
    };
  
    // Обработчики для полей
    const handleTelegramFocus = () => {
      if (telegram_id === '') {
        telegram_id = '@'; // Добавляем @, если поле пустое
      }
    };
  
    const handleTelegramInput = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (!input.value.startsWith('@')) {
        telegram_id = '@' + input.value.replace('@', '');
      } else {
        telegram_id = input.value;
      }
    };
  
    const handleRegister = async () => {
      // Проверка обязательных полей
      if (!name || !email || !password || !telephone_number || !course || isNaN(Number(course)) || !university_group) {
        showNotification('Пожалуйста, заполните все обязательные поля!', 'error');
        return;
      }
  
      if (!telegram_id || telegram_id === '@') {
        showNotification('Telegram ID обязателен и должен быть корректным!', 'error');
        return;
      }
  
      const phonePattern = /^\+?[0-9]{10,15}$/;
      if (!phonePattern.test(telephone_number)) {
        showNotification('Номер телефона должен содержать только цифры (от 10 до 15 символов) и может начинаться с +!', 'error');
        return;
      }
  
      const registrationData = { name, telegram_id, email, password, telephone_number, course: Number(course), university_group };
  
      try {
        // Устанавливаем флаг загрузки
        isLoading = true;
  
        const response = await fetch(`${BASE_URL}/create_user`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(registrationData),
        });
  
        if (response.ok) {
          const result = await response.json();
          showNotification('Регистрация успешна!', 'success');
          goto('/auntification/authorization/user');
        } else {
          const error = await response.json();
          showNotification(`Ошибка: ${error.detail || 'Неизвестная ошибка'}`, 'error');
        }
      } catch (err) {
        showNotification('Ошибка соединения с сервером.', 'error');
      } finally {
        // Снимаем флаг загрузки
        isLoading = false;
      }
    };
  </script>
  
  <style>
    .page-container {
      display: flex;
      justify-content: center; /* Центрирование по горизонтали */
      align-items: center; /* Центрирование по вертикали */
      height: 100vh;
      width: 100vw; /* Растягиваем на всю ширину экрана */
      background-color: #171615;
      background-image: url("/authUser.png");
      background-size: cover;
      background-position: center;
    }
  
    .login-container {
      position: relative;
      background: rgba(26, 26, 26, 0.8);
      border-radius: 20px;
      padding: 2rem;
      width: 400px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
      border: 2px solid #666666;
    }
  
    .login-container h1 {
      font-size: 2rem;
      color: #e0e0e0;
      margin-bottom: 1.5rem;
      font-weight: bold;
    }
  
    .login-container input {
      width: 100%;
      margin-bottom: 1.5rem;
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
  
    .login-container input.error {
      border: 2px solid red;
      background-color: rgba(255, 0, 0, 0.1);
    }
  
    .btn {
      background: transparent;
      color: white;
      border: 2px solid rgb(203, 203, 203);
      padding: 1rem 2.5rem;
      border-radius: 20px;
      font-size: 1.1rem;
      width: 75%;
      transition: all 0.3s ease;
      font-weight: bold;
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: "Font Over";

    }
  
    .btn:hover {
      transform: scale(1.05);
      box-shadow: 0 2px 10px rgba(255, 255, 255, 0.3);
    }
  
    .btn:active {
      transform: scale(0.95);
      box-shadow: 0 4px 10px rgba(255, 255, 255, 0.3);
    }
  
    .btn.loading::after {
      content: '';
      position: absolute;
      border: 3px solid transparent;
      border-top: 3px solid #fff;
      border-radius: 50%;
      width: 20px;
      height: 20px;
      animation: spin 1s linear infinite;
    }
  
    .notification {
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      background-color: #333;
      color: white;
      padding: 1rem;
      border-radius: 10px;
      font-size: 1rem;
      z-index: 1000;
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 300px;
      opacity: 1;
      transition: opacity 0.3s ease-out;
    }
  
    .notification.success {
      background-color: #28a745;
    }
  
    .notification.error {
      background-color: #dc3545;
    }
  
    .notification.info {
      background-color: #ffc107;
    }
  
    .notification.hidden {
      opacity: 0;
    }
  
    .notification button {
      background: none;
      border: none;
      color: white;
      font-size: 1.5rem;
      cursor: pointer;
    }
  
    @keyframes spin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
  
    @media (max-width: 768px) {
      .login-container {
        margin-top: 100px;
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
  
    @media (max-width: 480px) {
      .login-container {
        margin-top: 100px;
        width: 80%;
        padding: 1rem;
      }
  
      .login-container h1 {
        font-size: 1.2rem;
      }
  
      .login-container input {
        font-size: 0.8rem;
        width: 95%;
      }
  
      .btn {
        width: 80%;
        padding: 0.7rem 1rem;
        font-size: 1rem;
      }
    }
  </style>
  
  <Icon id="logo" />
  <div class="page-container">
    <div class="login-container">
      <h1 class="title">Регистрация</h1>
      <input type="text" placeholder="ФИО" bind:value={name} required />
      <input type="email" placeholder="Почта" bind:value={email} required />
      <input
        type="text"
        placeholder="Telegram"
        bind:value={telegram_id}
        on:focus={handleTelegramFocus}
        on:input={handleTelegramInput}
        class:error={telegram_id === '@'}
      />
      <input type="password" placeholder="Пароль" bind:value={password} required />
      <input
        type="tel"
        placeholder="Номер телефона"
        bind:value={telephone_number}
        required
        class:error={!/^\+?[0-9]{10,15}$/.test(telephone_number) && telephone_number !== ''}
      />
      <input type="number" placeholder="Курс" bind:value={course} required />
      <input type="text" placeholder="Учебная группа" bind:value={university_group} required />
      <button class="btn {isLoading ? 'loading' : ''}" on:click={handleRegister}>
        {isLoading ? 'Загрузка...' : 'Зарегистрироваться'}
      </button>
  
      {#if notificationMessage}
        <div class="notification {notificationType}">
          {notificationMessage}
          <button on:click={() => notificationMessage = ''}>×</button>
        </div>
      {/if}
    </div>
  </div>
  