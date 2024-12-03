<script>
    // Массив мероприятий
    let events = [
        { id: 1, title: "Мероприятие 1", image: "https://via.placeholder.com/150" },
        { id: 2, title: "Мероприятие 2", image: "https://via.placeholder.com/150" },
        { id: 3, title: "Мероприятие 3", image: "https://via.placeholder.com/150" },
        { id: 4, title: "Мероприятие 4", image: "https://via.placeholder.com/150" },
        { id: 5, title: "Мероприятие 5", image: "https://via.placeholder.com/150" },
        { id: 6, title: "Мероприятие 6", image: "https://via.placeholder.com/150" },
        { id: 7, title: "Мероприятие 7", image: "https://via.placeholder.com/150" },
        { id: 8, title: "Мероприятие 8", image: "https://via.placeholder.com/150" },
    ];
</script>

<style>


    /* Фон на весь экран */
    .background-container {
        position: fixed; /* Фиксируем контейнер на фоне */
        top: 0;
        left: 0;
        width: 100vw; /* Ширина на весь экран */
        height: 100vh; /* Высота на весь экран */
        background-color: #1d1d1d; /* Темный фон */
        z-index: -1; /* Отправляем фон под основной контент */
    }

    .container {
        max-width: 1200px;
        margin: 20px auto;
        padding: 20px; /* Отступы внутри основного контейнера */
        text-align: center;
        color: white;
    }

    h1 {
        margin-bottom: 20px;
        color: white;
    }

    .grid {
        display: flex; /* Flex-контейнер */
        flex-wrap: wrap; /* Разрешить перенос элементов на новую строку */
        gap: 20px; /* Расстояние между карточками */
        justify-content: center; /* Центровка карточек по горизонтали */
    }

    .card {
        background-color: #333;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        padding: 10px; /* Рамка внутри карточки */
        width: 200px; /* Фиксированная ширина карточек */
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .card img {
        width: 90%; /* Оставляем рамку сверху, слева и справа */
        margin: 10px auto; /* Центровка изображения */
        display: block;
        border-radius: 6px; /* Закругленные края изображения */
    }

    .card-title {
        margin-top: 10px; /* Отступ между изображением и текстом */
        font-size: 1rem;
        background-color: #444;
        color: #ccc;
        padding: 10px;
        border-radius: 6px;
        text-align: center;
    }
</style>

<!-- Фон на весь экран -->
<div class="background-container"></div>

<!-- Основной контент -->
<div class="container">
    <h1>Архивные мероприятия</h1>
    <div class="grid">
        {#each events as event}
            <div class="card">
                <img src={event.image} alt={event.title} />
                <div class="card-title">{event.title}</div>
            </div>
        {/each}
    </div>
</div>
