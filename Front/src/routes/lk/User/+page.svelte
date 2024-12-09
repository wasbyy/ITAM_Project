<script lang="ts">
    let events = [
        { id: 1, name: "Мероприятие 1", time: "12:30", date: "2024-12-05" },
        { id: 2, name: "Мероприятие 2", time: "14:00", date: "2024-12-06" },
        { id: 3, name: "Мероприятие 3", time: "16:15", date: "2024-12-07" },
        { id: 4, name: "Мероприятие 4", time: "18:45", date: "2024-12-08" },
    ];

    function viewTime(eventId: number) {
        const event = events.find(e => e.id === eventId);
        if (event) {
            alert(`Время мероприятия: ${event.time}`);
        }
    }

    function viewDate(eventId: number) {
        const event = events.find(e => e.id === eventId);
        if (event) {
            alert(`Дата мероприятия: ${event.date}`);
        }
    }
</script>

<style>/* Глобальные стили для всей страницы */
    :global(html, body) {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        height: 100%;
        background-color: #171615; /* Черный фон для всей страницы */
        color: white;
        font-family: "Inter", sans-serif;
        overflow-y: auto; /* Разрешаем прокрутку всей страницы */
    }
    
    .container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        height: 100%;
        padding: 20px;
    }
    
    .header {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
        padding-left: 4%;
        margin-top: 1.5%;
    }
    
    .profile-container {
        position: relative; /* Для размещения дочерних элементов слоями */
        width: 105px;
        height: 105px;
    }
    
    .profile-glow {
        position: absolute;
        top: 1px;
        left: 2px;
        width: 95%;
        height: 95%;
        border-radius: 50%; /* Идеальный круг */
        box-shadow: 
            inset 0 0 25px rgba(255, 255, 255, 0.7),   
            inset 20px 0 40px rgba(249, 89, 218, 0.7),  
            inset -20px 0 40px rgba(206, 111, 228, 0.7), 
            inset 20px 0 150px rgba(154, 139, 240, 0.7),
            inset -20px 0 150px rgba(108, 162, 251, 0.7),
            0 0 5px rgba(249, 89, 218, 0.6),         
            -8px 0 15px rgba(206, 111, 228, 0.6), 
            8px 0 15px rgba(108, 162, 251, 0.6),
            0px 0 20px rgba(154, 139, 240, 0.6);
        z-index: 1; /* Под иконкой профиля */
    }
    
    .profile-image {
        position: absolute;
        width: 105px;
        height: 105px;
        border-radius: 50%; /* Идеальный круг */
        background-image: url('/Profile.png'); /* Добавление изображения */
        background-position: center; /* Центрирование изображения */
        background-size: cover;
        z-index: 2; /* Поверх свечения */
    }
    
    .title {
        font-size: 64px;
        font-weight: bold;
        margin: 0;
        margin-left: 38px;
    }
    
    .subtitle {
        font-size: 32px;
        color: #888;
        margin: 0;
        margin-left: 38px;
    }
    
    .events-list {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: 20px;
        /* Убираем ограничение на прокрутку, теперь вся страница будет прокручиваться */
    }
    
    .events-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 92%; /* Общая ширина */
        margin-bottom: 15px;
    }
    
    .events-header h2 {
        font-size: 48px;
        font-weight: bold;
        color: white;
        margin-bottom: 10px;
    }
    
    .archive-btn {
    background: transparent; /* Прозрачный фон */
    color: white; /* Белый текст */
    text-align: center;
    padding: 10px 50px;
    font-size: 24px;
    font-weight: bolder;
    border: 2px solid #444444; /* Белый контур */
    border-radius: 40px; /* Овальная форма */
    cursor: pointer;
    text-decoration: none; /* Убираем подчеркивание */
}

.archive-btn:hover {
    background: rgba(255, 255, 255, 0.1); /* Прозрачный белый фон при наведении */
}

    
    .event {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #242423;
        padding: 15px; /* Уменьшен отступ */
        border-radius: 21px;
        margin-bottom: 12px; /* Уменьшено расстояние между панелями */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        height: 80px; /* Уменьшена высота */
        width: 90%;
        border: #444444 solid;
    }
    
    .event-name-panel {
        background-color: #171615;
        width: 50%;
        height: 75%; /* Высота на всю панель мероприятия */
        padding: 8px 15px; /* Уменьшен внутренний отступ */
        border-radius: 21px;
        display: flex;
        justify-content: flex-start;
        align-items: center;
    }
    
    .event-name {
        font-size: 28px; /* Уменьшен размер шрифта */
        font-weight: normal;
        color: white;
    }
    
    .buttons {
        display: flex;
        gap: 26px; /* Уменьшено расстояние между кнопками */
    }
    
    button {
        padding: 15px 17px; /* Уменьшен внутренний отступ кнопок */
        font-size: 20px; /* Уменьшен размер шрифта кнопок */
        border: 2px solid white;
        background: transparent;
        color: white;
        border-radius: 40px;
        cursor: pointer;
    }
    
    .time-btn:hover {
        background: rgba(26, 188, 156, 0.1);
    }
    
    .date-btn:hover {
        background: rgba(52, 152, 219, 0.1);
    }
    
    .logo {
        position:absolute;
        top: 50px;
        right: 80px;
        width: 100px; /* Размер логотипа */
        height: auto;
        cursor: pointer;
        z-index: 1000; /* Поверх всего контента */
    }
    
    /* Стиль для нового раздела "Данные" */
    .data-section {
        margin-left: 4%;
        margin-bottom: 30px;
        text-align: left;
    }
    
    .data-section h2 {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .data-panels {
        display: flex;
        justify-content: left;
        gap: 20px;
    }
    
    .data-panel {
        position: relative; /* Для псевдоэлемента */
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 30px; /* Внутренние отступы */
        font-size: 24px;
        font-weight: bold;
        color: white;
        background-color: #171615; /* Фон панели */
        border-radius: 50px; /* Скруглённые углы */
        z-index: 1; /* Выше псевдоэлемента */
        text-align: center;
        min-width: 200px; /* Минимальная ширина панели */
    }
    
    .data-panel::before {
        content: ''; /* Пустое содержимое */
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: inherit; /* Наследуем скруглённые углы */
        padding: 2px; /* Ширина рамки */
        background: linear-gradient(90deg, #F859DA, #D56CE3, #A684EE, #A684EE); /* Градиент рамки */
        -webkit-mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0); /* Маска для видимости только рамки */
        -webkit-mask-composite: xor; /* XOR для видимости только границ */
        mask-composite: exclude; /* То же самое для стандартных браузеров */
        z-index: -1; /* Позади панели */
    }
    @media (max-width: 600px) {
    
    /* Уменьшаем шрифт заголовков */
    .title {
        font-size: 32px;
    }

    .subtitle {
        font-size: 18px;
    }

    .events-header h2 {
        font-size: 24px;
    }

    .event-name {
        font-size: 18px;
        padding: 5px;
    }

    .buttons button {
        font-size: 12px;
        padding: 8px 10px;
    }

    .event {
        flex-direction: column; /* Ставим элементы в колонку */
        height: auto;
        padding: 10px;
    }

    .event-name-panel {
        width: 100%; /* Панель события на всю ширину */
        height: auto;
        padding: 5px 10px;
        margin-bottom: 5px;

    }

    .buttons {
        flex-direction: row; /* Кнопки вертикально */
        gap: 10px;
        justify-content: space-between;
    }

    /* Уменьшаем размер иконки профиля */
    .profile-container {
        width: 80px;
        height: 80px;
    }

    .profile-image {
        width: 80px;
        height: 80px;
    }

    /* Уменьшаем размеры панелей с данными */
    .data-panel {
        font-size: 18px;
        min-width: 150px; /* Уменьшаем минимальную ширину */
        padding: 10px 15px;
    }

    .data-panels {
        flex-direction: column;
        gap: 10px;
    }

    /* Уменьшаем размер кнопки архива */
    .archive-btn {
        font-size: 18px;
        padding: 8px 20px;
    }

    /* Логотип также уменьшаем */
    .logo {
        width: 80px;
        top: 20px;
        right: 10px;
    }

    /* Изменения для контейнера и основного блока */
    .container {
        padding: 10px;
    }

    .header {
        margin-top: 10px;
        padding-left: 0;
        flex-direction: column;
        align-items: center;
        margin-right: 20px;

    }

    .events-list {
        padding: 0;
    }

}

</style>

<div class="container">
    <!-- Логотип -->
    <a href="http://localhost:5173/mainpage">
        <img src="/itam_logo.png" alt="Логотип" class="logo" />
    </a>
    
    <!-- Header -->
    <div class="header">
        <div class="profile-container">
            <div class="profile-glow"></div>
            <div class="profile-image"></div>
        </div>
        <div>
            <div class="title">Имя Пользователя</div>
            <div class="subtitle">Почта</div>
        </div>
    </div>

    <!-- Новый раздел "Данные" -->
    <div class="data-section">
        <h2>Данные</h2>
        <div class="data-panels">
            <div class="data-panel ">+7 (xxx) xxx-xx-xx</div>
            <div class="data-panel ">pochtapolizov@pochta.com</div>
            <div class="data-panel ">N курс БХХХ - N - N</div>
        </div>
    </div>

    <!-- Events Section -->
    <div class="events-list">
        <div class="events-header">
            <h2>МЕРОПРИЯТИЯ</h2>
            <a href="http://localhost:5173/archive" class="archive-btn">АРХИВ</a>
        </div>

        <!-- Event List -->
        {#each events as event}
        <div class="event">
            <div class="event-name-panel">
                <div class="event-name">{event.name}</div>
            </div>
            <div class="buttons">
                <button class="time-btn" on:click={() => viewTime(event.id)}>Время: {event.time}</button>
                <button class="date-btn" on:click={() => viewDate(event.id)}>Дата: {event.date}</button>
            </div>
        </div>
        {/each}
    </div>
</div>
