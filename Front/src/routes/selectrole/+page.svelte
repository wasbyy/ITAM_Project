<script lang="ts">
    const handleParticipantClick = () => {
        // Перенаправление на страницу входа для участников
        window.location.href = "http://localhost:5173/authorization"; 
    };

    const handleAdminClick = () => {
        // Перенаправление на страницу входа для админов
        window.location.href = "http://localhost:5173/authorization"; 
    };
</script>

<style>
    /* Импорт пиксельного шрифта */
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Общий стиль для страницы */
    :global(body) {
        margin: 0;
        padding: 0;
        font-family: 'Press Start 2P', monospace; /* Пиксельный стиль */
        background-color: #000; /* Черный фон */
        color: white; /* Белый текст */
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .container {
        text-align: center;
    }

    .buttons {
        display: flex;
        justify-content: center;
        gap: 3rem; /* Увеличенное расстояние между кнопками */
    }

    .button {
        width: 280px; /* Фиксированная ширина для одинакового размера кнопок */
        padding: 1.5rem 0; /* Увеличенный вертикальный отступ */
        font-size: 1rem; /* Размер текста */
        font-family: 'Press Start 2P', monospace; /* Пиксельный шрифт на кнопках */
        color: white;
        background: transparent;
        border: 3px solid white; /* Толще обводка */
        border-radius: 30px; /* Овальные края */
        cursor: pointer;
        text-transform: uppercase; /* Все буквы заглавные */
        letter-spacing: 2px; /* Расстояние между буквами */
        transition: all 0.3s ease; /* Плавный переход */
        text-align: center; /* Центрирование текста */
        display: inline-block; /* Гарантия того, что кнопки остаются блочными */
        position: relative; /* Для псевдоэлементов */
        overflow: hidden; /* Чтобы градиентная подсветка не выходила за края */
    }

    /* Плавная анимация при нажатии */
    .button:active {
        transform: scale(0.92); /* Уменьшение кнопки при клике */
    }

    /* Подсветка зеленым градиентом для кнопки "участник" */
    .button:nth-child(1):hover {
        border-color: transparent;
        background-image: linear-gradient(90deg, #00ff00, #009900); /* Зеленый градиент */
        color: black; /* Черный текст */
        animation: shine 1.5s infinite linear; /* Добавляет плавное движение */
    }

    /* Подсветка фиолетовым градиентом для кнопки "админ" */
    .button:nth-child(2):hover {
        border-color: transparent;
        background-image: linear-gradient(90deg, #9900cc, #ff00ff); /* Фиолетовый градиент */
        color: black; /* Черный текст */
        animation: shine 1.5s infinite linear; /* Добавляет плавное движение */
    }

    /* Добавление плавного мерцания градиента */
    @keyframes shine {
        0% {
            background-position: -200%;
        }
        50% {
            background-position: 100%;
        }
        100% {
            background-position: 200%;
        }
    }

    .branding {
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 0.8rem;
        font-family: 'Press Start 2P', monospace; /* Пиксельный шрифт для текста брендинга */
        color: white;
        opacity: 0.6; /* Легкая прозрачность */
    }
</style>

<div class="container">
    <div class="buttons">
        <button class="button" on:click={handleParticipantClick}>
            я участник
        </button>
        <button class="button" on:click={handleAdminClick}>
            я админ
        </button>
    </div>
</div>
