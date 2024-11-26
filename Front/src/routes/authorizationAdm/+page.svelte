<script lang="ts">
    import Header from "$lib/components/Header.svelte";
    let login: string = '';
    let password: string = '';
    const handleLogin = () => {
        if (login && password) {
            console.log('Login:', login);
            console.log('Password:', password);
        } else {
            console.log('Заполните все поля!');
        }
    };
</script>

<style>
    /* Общий стиль для страницы */
    :global(body) {
        margin: 0;
        padding: 0;
        font-family: 'DM Sans', sans-serif;
        background-color: #1e1d1c; /* Темный фон */
        color: white; /* Белый текст */
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .login-container {
        position: relative; /* Для градиентной обводки */
        background: #1a1a1a; /* Цвет панели */
        border-radius: 20px;
        padding: 2.5rem; /* Пространство внутри панели */
        width: 400px; /* Увеличенная ширина панели */
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }

    /* Градиентная обводка с круговым движением */
    .login-container::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(135deg, #ff4cf0, #ff8c00, #ff0080, #ff4cf0); /* Начало и конец совпадают */
        background-size: 300% 300%; /* Увеличенный размер для плавного движения */
        border-radius: 23px; /* Радиус больше панели на 3px */
        z-index: -1; /* Размещение позади панели */
        animation: circularGradient 5s linear infinite; /* Анимация для кругового движения */
    }

    /* Анимация кругового движения градиента */
    @keyframes circularGradient {
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
    font-size: 2rem; /* Увеличенный размер заголовка */
    margin-top: -0.5rem; /* Поднимаем заголовок вверх */
    margin-bottom: 2rem; /* Уменьшенный отступ снизу */
    color: #e0e0e0; /* Основной акцентный цвет */
    font-weight: bold;
}


    .login-container input {
        width: 100%; /* Поля растянуты по ширине */
        margin-bottom: 1rem;
        padding: 1rem; /* Увеличенный внутренний отступ */
        border-radius: 10px;
        border: none;
        outline: none;
        background: rgba(255, 255, 255, 0.1); /* Полупрозрачный фон */
        color: #e0e0e0; /* Цвет текста */
        font-size: 1rem;
        text-align: left;
        transition: background 0.3s ease;
    }

    .login-container input:focus {
        background: rgba(255, 255, 255, 0.2); /* Подсветка при фокусе */
    }
/* Импорт пиксельного шрифта */
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Стиль кнопки с градиентной анимацией */
    .btn {
        position: relative;
        background: linear-gradient(45deg, #D38312 10%, #A83279 90%); /* Начальный градиент */
        background-size: 200% 100%; /* Увеличиваем область для плавного перемещения */
        padding: 1rem 1.5rem;
        color: white;
        border-radius: 20px; /* Округлые края */
        font-size: 1.1rem; /* Уменьшенный размер шрифта */
        border: none;
        width: 50%; /* Ширина по всей панели */
        animation: gradientAnimation 4s linear infinite; /* Анимация переливания */
        transition: all 0.3s ease; /* Плавный переход */
        font-family: "Pixelify Sans", serif;
        font-weight: 100;
        font-size: 20px;        
    }

    /* Анимация плавного переливания градиента */
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
        transform: scale(1.01); /* Увеличение кнопки при наведении */
        box-shadow: 0 4px 10px rgba(255, 255, 255, 0.15); /* Легкая подсветка */
    }

    .btn:active {
        transform: scale(0.95); /* Уменьшение размера при нажатии */
        box-shadow: 0 2px 5px rgba(255, 255, 255, 0.1); /* Уменьшенная тень */
    }
</style>

<div class="login-container">
    <Header />
    <h1 class="title">Вход</h1>
    <input type="text" placeholder="Логин" bind:value={login} />
    <input type="password" placeholder="Пароль" bind:value={password} />
    <button class="btn" on:click={handleLogin}>Войти</button>
</div>