<script lang="ts">
    import { goto } from '$app/navigation'; // SvelteKit
    import Icon from '$lib/components/Icon.svelte';
    import { BASE_URL } from '../../../config';

    // Поля формы
    let name: string = '';
    let email: string = '';
    let telegram_id: string = ''; // Начинается пустым
    let password: string = '';
    let telephone_number: string = ''; // Теперь это строка
    let course: string = '';
    let university_group: string = '';

    // Уведомления
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

    // Обработчик фокуса на поле Telegram
    const handleTelegramFocus = () => {
        if (telegram_id === '') {
            telegram_id = '@'; // Добавляем @, если поле пустое
        }
    };

    // Обработчик ввода в поле Telegram
    const handleTelegramInput = (event: Event) => {
        const input = event.target as HTMLInputElement;
        if (!input.value.startsWith('@')) {
            telegram_id = '@' + input.value.replace('@', ''); // Гарантируем, что @ всегда первый символ
        } else {
            telegram_id = input.value;
        }
    };

    // Обработчик регистрации
    const handleRegister = async () => {
        console.log('Данные формы:', { name, email, telegram_id, password, telephone_number, course, university_group });

        // Проверка обязательных полей
        if (
            !name ||
            !email ||
            !password ||
            !telephone_number ||
            !course ||
            isNaN(Number(course)) || // Убедитесь, что курс — это число
            !university_group
        ) {
            showNotification('Пожалуйста, заполните все обязательные поля!', 'error');
            return;
        }

        // Проверка Telegram ID
        if (!telegram_id || telegram_id === '@') {
            showNotification('Telegram ID обязателен и должен быть корректным (начинаться с @ и содержать текст)!', 'error');
            return;
        }

        // Проверка номера телефона с поддержкой символа '+'
        const phonePattern = /^\+?[0-9]{10,15}$/; // Регулярное выражение для проверки номера телефона (с возможным знаком +)
        if (!phonePattern.test(telephone_number)) {
            showNotification('Номер телефона должен содержать только цифры (от 10 до 15 символов) и может начинаться с +!', 'error');
            return;
        }

        // Формируем данные для отправки
        const registrationData = {
            name,
            telegram_id,
            email,
            password,
            telephone_number, // Оставляем как строку
            course: Number(course),
            university_group,
        };

        console.log('Отправка данных на сервер:', registrationData);

        try {
            const response = await fetch(`${BASE_URL}/create_user`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(registrationData),
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Успешный ответ:', result);
                showNotification('Регистрация успешна!', 'success');
                goto('/auntification/authorization/user');
            } else {
                const error = await response.json();
                console.error('Ошибка регистрации:', error);
                showNotification(`Ошибка: ${error.detail || 'Неизвестная ошибка'}`, 'error');
            }
        } catch (err) {
            console.error('Ошибка при выполнении запроса:', err);
            showNotification('Ошибка соединения с сервером.', 'error');
        }
    };
</script>

<style>
    .page-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #1e1d1c;
    }
        .border-container {
        position: relative;
        padding: 3px; /* Отступ для обводки */
        background: linear-gradient(135deg, #00ff00, #1db954, #00ff99, #2ecc71);
        border-radius: 20px; /* Радиус скругления обводки */
        z-index: 0; /* Убедитесь, что обводка будет под основной панелью */
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

    .login-container input.error {
        border: 2px solid red;
        background-color: rgba(255, 0, 0, 0.1);
    }

    @media (max-width: 768px) {
        .login-container {
            margin-top: 120px;
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
    <div class="border-container">
        <div class="login-container">
        <h1 class="title">Регистрация</h1>
        <input
            type="text"
            placeholder="ФИО"
            bind:value={name}
            required
        />
        <input
            type="email"
            placeholder="Почта"
            bind:value={email}
            required
        />
        <input
            type="text"
            placeholder="Telegram"
            bind:value={telegram_id}
            on:focus={handleTelegramFocus} 
            on:input={handleTelegramInput} 
            class:error={telegram_id === '@'} 
        />
        <input
            type="password"
            placeholder="Пароль"
            bind:value={password}
            required
        />
        <input
            type="tel"
            placeholder="Номер телефона"
            bind:value={telephone_number}
            required
            class:error={!/^\+?[0-9]{10,15}$/.test(telephone_number) && telephone_number !== ''} 
        />
        <input
            type="number"
            placeholder="Курс"
            bind:value={course}
            required
        />
        <input
            type="text"
            placeholder="Учебная группа"
            bind:value={university_group}
            required
        />
        <button class="btn" on:click={handleRegister}>Зарегистрироваться</button>

        {#if notificationMessage}
            <div class="notification {notificationType}">
                {notificationMessage}
                <button on:click={() => notificationMessage = ''}>×</button>
            </div>
        {/if}
        </div>
    </div>
</div>
