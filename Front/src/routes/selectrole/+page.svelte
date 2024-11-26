<script lang="ts">
    import Header from "$lib/components/Header.svelte";
    const handleParticipantClick = () => {
        // Перенаправление на страницу входа для участников
        window.location.href = "http://localhost:5173/authorizationUser"; 
    };

    const handleAdminClick = () => {
        // Перенаправление на страницу входа для админов
        window.location.href = "http://localhost:5173/authorizationAdm"; 
    };

</script>

<style>
    /* Импорт пиксельного шрифта */
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Общий стиль для страницы */
    :global(body) {
        margin: 0;
        padding: 0;
        font-family: 'Press Start 2P', monospace; /* Пиксельный шрифт */
        background-color: #1e1d1c; /* Тёмный фон */
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

    /* Общий стиль для кнопок */
    .glow-on-hover {
        width: 500px;
        height: 80px;
        border: none;
        outline: none;
        background: none;
        cursor: pointer;
        position: relative;
        z-index: 0;
        border-radius: 50px; /* Более закругленные края */
        font-size: 26px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: "Pixelify Sans", serif;
        color: white; /* По умолчанию белый текст */
    }

    /* Кнопка участника (фоновое свечение) */
    .f {
        box-shadow: 0 0 15px rgba(72, 255, 0, 0.3), 0 0 30px rgba(0, 255, 255, 0.2); /* Зеленое и бирюзовое свечение */
        transition: box-shadow 0.3s ease-in-out; /* Плавный переход для свечения */
    }

    /* Кнопка администратора (обновленное свечение) */
    .a {
        box-shadow: 0 0 15px rgba(255, 90, 0, 0.3), 0 0 30px rgba(255, 0, 150, 0.2); /* Оранжевый и розовый градиент */
        transition: box-shadow 0.3s ease-in-out; /* Плавный переход для свечения */
    }

    /* Эффект при наведении для кнопки участника */
    .glow-on-hover.participant:hover {
        color: transparent; /* Прячем текст, чтобы применить градиент */
    }

    .glow-on-hover.participant:hover span {
        background: linear-gradient(45deg, #48ff00, #00ffd5, #48ff00); /* Зеленый градиент для участника */
        background-size: 400%;
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        animation: gradient-text-animation 20s linear infinite;
    }

    /* Эффект при наведении для кнопки админа */
    .glow-on-hover.admin:hover {
        color: transparent; /* Прячем текст, чтобы применить градиент */
    }

    .glow-on-hover.admin:hover span {
        background: linear-gradient(45deg, #ff6000, #ff00ff, #ff007f); /* Оранжево-розовый градиент для админа */
        background-size: 400%;
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        animation: gradient-text-animation 20s linear infinite;
    }

    /* Анимация для градиентного текста */
    @keyframes gradient-text-animation {
        0% { background-position: 0 0; }
        50% { background-position: 400% 0; }
        100% { background-position: 0 0; }
    }

    /* Градиентный фон кнопок */
    .participant:before, .admin:before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        background-size: 400%;
        z-index: -1;
        filter: blur(5px);
        width: calc(100% + 4px);
        height: calc(100% + 4px);
        animation: glowing 20s linear infinite;
        opacity: 0;
        transition: opacity .3s ease-in-out;
        border-radius: 50px; /* Более закругленные края */
    }

    /* Подсветка для участника */
    .participant:hover:before {
        background: linear-gradient(45deg, #48ff00, #00ffd5, #48ff00); /* Зеленый и бирюзовый для участника */
        opacity: 1;
    }

    /* Подсветка для админа */
    .admin:hover:before {
        background: linear-gradient(45deg, #ff6000, #ff00ff, #ff007f); /* Оранжево-розовый для админа */
        opacity: 1;
    }

    .glow-on-hover:after {
        z-index: -1;
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        background: #111;
        left: 0;
        top: 0;
        border-radius: 50px; /* Более закругленные края */
    }
</style>

<div class="container">
    <Header />
    <div class="buttons">
        <button class="glow-on-hover participant f" on:click={handleParticipantClick}>
            <span>я участниk</span>
        </button>
        <button class="glow-on-hover admin a" on:click={handleAdminClick}>
            <span>я организатор</span>
        </button>
    </div>
</div>
