<script lang="ts">
    import { goto } from '$app/navigation'; // SvelteKit
    import Icon from '$lib/components/Icon.svelte';
    // Поля формы
    let name: string = '';
    let email: string = '';
    let password: string = '';
    let telephone_number: number | null = null;
    let course: number | null = null;
    let university_group: string = '';
    

    // Состояние для уведомлений
    let notificationMessage: string = '';
    let notificationType: 'success' | 'error' | 'info' = 'info';

    // URL API
    const BASE_URL = 'http://130.193.52.139:8000';

    // Функция для отображения уведомлений
    const showNotification = (message: string, type: 'success' | 'error' | 'info') => {
        notificationMessage = message;
        notificationType = type;

        // Скрыть уведомление через 3 секунды
        setTimeout(() => {
            notificationMessage = '';
        }, 3000);
    };

    // Обработчик регистрации
    const handleRegister = async () => {
    if (name && email && password && telephone_number && course && university_group) {
        const registrationData = {
            name,
            email,
            password,
            telephone_number,
            course,
            university_group,
        };

        // Логируем данные перед отправкой
        console.log('Данные для регистрации:', registrationData);
        console.log('URL для запроса:', `${BASE_URL}/create_user`);

        try {
            const response = await fetch(`${BASE_URL}/create_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(registrationData),
            });

            // Логируем объект ответа
            console.log('Ответ от сервера (RAW):', response);

            if (response.ok) {
                const result = await response.json();

                // Логируем результат успешного ответа
                console.log('Успешный ответ от сервера:', result);
                showNotification('Регистрация успешна!', 'success');
                goto('/mainpage'); // Переход на главную страницу
            } else {
                // Логируем, если ответ не OK
                const error = await response.json();
                console.error('Ошибка регистрации:', error);
                showNotification(`Ошибка: ${error.detail || 'Неизвестная ошибка'}`, 'error');
            }
        } catch (err) {
            // Логируем ошибки сети или запроса
            console.error('Ошибка при выполнении запроса:', err);
            showNotification('Сервер недоступен. Проверьте подключение.', 'error');
        }
    } else {
        // Логируем, если поля формы не заполнены
        console.warn('Не все поля заполнены. Проверьте форму.');
        showNotification('Пожалуйста, заполните все поля!', 'info');
    }
};

</script>
<style>
    /* Общий стиль для страницы */
    :global(body) {
        margin: 0;
        padding: 0;
        font-family: "Inter", sans-serif;
        background-color: #1e1d1c;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .login-container {
        position: relative;
        background: #1a1a1a;
        border-radius: 20px;
        padding: 2.5rem;
        width: 400px;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    }

    /* Градиентная обводка */
    .login-container::before {
        content: '';
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

    .btn {
        position: relative;
        background: linear-gradient(45deg, #00ff99, #1db954, #2ecc71, #00ff00);
        background-size: 300% 300%;
        padding: 1rem 1.5rem;
        color: white;
        border-radius: 20px;
        font-size: 1.1rem;
        border: none;
        width: 80%;
        animation: buttonGradient 2s linear infinite;
        transition: all 0.3s ease;
        font-weight: 100;
        font-size: 20px;
    }

    @keyframes buttonGradient {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    .btn:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 255, 0, 0.5);
    }

    .btn:active {
        transform: scale(0.95);
        box-shadow: 0 4px 10px rgba(0, 255, 0, 0.3);
    }

    /* Стиль для уведомлений */
    .notification {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: rgb(255, 255, 255);
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
        color: rgb(255, 255, 255);
        font-size: 1.5rem;
        cursor: pointer;
    }
</style>

<Icon id="logo"/>

<div class="login-container">
    <h1 class="title">Регистрация</h1>
    <input type="text" placeholder="Имя" bind:value={name} />
    <input type="email" placeholder="Почта" bind:value={email} />
    <input type="password" placeholder="Пароль" bind:value={password} />
    <input type="tel" placeholder="Номер телефона" bind:value={telephone_number} />
    <input type="number" placeholder="Курс" bind:value={course} />
    <input type="text" placeholder="Учебная группа" bind:value={university_group} />
    <button class="btn" on:click={handleRegister}>Зарегистрироваться</button>
</div>

{#if notificationMessage}
  <div class="notification {notificationType}">
    {notificationMessage}
    <button on:click={() => notificationMessage = ''}>×</button>
  </div>
{/if}
