<script lang="ts">
    import { onMount } from "svelte";
    import Icon from "$lib/components/Icon.svelte";
    // Тип данных для мероприятия
    interface EventData {
        event_name: string;
        place: string;
        long_description: string;
        max_count_of_members: number;
        online_event_link: string;
        format: string;
        tags: string;
        is_active: boolean;
    }

    // Заглушка для данных мероприятия
    export let eventInfo = {
        photo: "",
        title: "Название мероприятия",
        date: "",
        time: "",
        location: "",
        format: "",
        participants: "",
        description: "",
    };

    // URL для запроса данных мероприятия
    const API_URL = "http://158.160.72.41:8000/docs#/Events/{event_id}"; // Замените на актуальный URL бэкенда

    // Функция для загрузки данных мероприятия
    async function fetchEventData() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error(`Ошибка загрузки данных: ${response.statusText}`);
            }
            const data: EventData = await response.json();

            // Обновление данных мероприятия
            eventInfo = {
                photo: "", // Замените на поле из бэкенда, если есть
                title: data.event_name,
                date: "ДД/ММ/ГГ", // Подставьте дату, если есть
                time: "00:00", // Подставьте время, если есть
                location: data.place,
                format: `Формат мероприятия: ${data.format}`,
                participants: `Участников: 0/${data.max_count_of_members}`, // Реальные данные
                description: data.long_description,
            };
        } catch (error) {
            console.error("Ошибка при загрузке данных:", error);
        }
    }

    // Загружаем данные при монтировании компонента
    onMount(() => {
        fetchEventData();
    });

    // Функция для регистрации
    function register() {
        alert("Вы зарегистрировались на мероприятие!");
    }

    // Функция для подключения к онлайн встрече
    function joinOnline() {
        alert("Вы присоединились к онлайн встрече!");
    }
</script>

<style>

/* Основной контейнер для всей страницы */
.page-background {
    background-color: #171615;
    background-image: url('/eventbackground.png'); /* Фон с изображением */
    background-size: cover;
    background-position: center center; /* Центрируем фоновое изображение */
    min-height: 100vh; /* Высота экрана */
    width: 100%; /* Занимает всю ширину */
    display: flex;
    justify-content: center; /* Контент начинается с верхней части */
    align-items: flex-start; /* Выравнивание содержимого сверху */
    position: absolute;  /* Обеспечиваем, чтобы контейнер был поверх всего */
    top: 0;
    left: 0;
}

/* Панель мероприятия */
.event-page {
    background-color: rgba(36, 36, 35, 0.9); /* Полупрозрачный черный фон */
    color: white;
    padding: 20px;
    max-width: 90%;
    width: 100%;
    min-height: 50vh;
    margin-top: 90px;    
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: flex-start; /* Элементы выравниваются сверху */
}


    .header {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
        align-items: flex-start;
    }

    .event-photo {
        width: 540px;
        height: 270px;
        object-fit: cover;
        border-radius: 10px;
        background-color: #ccc;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #888;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    }

    .event-details {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap: 10px;
    }

    .event-title {
        font-size: 48px;
        font-weight: bold;
        margin: 0;
        margin-bottom: 30px;
        font-family: 'Press Start 2P', monospace;
    }

    .event-meta {
        display: flex;
        gap: 40px;
        font-size: 32px;
        color: #888;
        font-family: "Inter", sans-serif;
    }

    .event-format {
        font-size: 32px;
        color: #888;
        margin-bottom: 10px;
        font-family: "Inter", sans-serif;
    }

    .event-participants {
        font-size: 32px;
        color: #888;
        font-family: "Inter", sans-serif;
    }

    .description {
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 24px;
    margin-bottom: 20px;
    word-wrap: break-word;
    font-family: "Inter", sans-serif;
    max-height: none; /* Снимаем ограничения по высоте */
    flex-grow: 1; /* Это позволяет растягиваться, если описание большое */
}

    .buttons {
        display: flex;
        justify-content: space-between;
        gap: 700px;
        margin-top: auto;
    }

    .register-btn,
    .online-btn {
        flex: 1;
        background-color: #FB607F;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: 0.3s;
        text-align: center;
        font-family: "Inter", sans-serif;
    }

    .register-btn:hover {
        background-color: #ff4c4c;
    }

    .online-btn {
        background-color: #FB8967;
    }

    .online-btn:hover {
        background-color: #ff893c;
    }
</style>

<Icon id="logo" />
<div class="page-background">
    <div class="event-page">
        <!-- Фото и заголовок -->
        <div class="header">
            {#if eventInfo.photo}
                <img src={eventInfo.photo} alt="Фото мероприятия" class="event-photo" />
            {:else}
                <div class="event-photo">540x270 Placeholder</div>
            {/if}
            <div class="event-details">
                <h1 class="event-title">{eventInfo.title}</h1>
                <div class="event-meta">
                    <span>{eventInfo.location}</span>
                    <span>{eventInfo.date}</span>
                    <span>{eventInfo.time}</span>
                </div>
                <div>
                    <div class="event-format">{eventInfo.format}</div>
                    <div class="event-participants">{eventInfo.participants}</div>
                </div>
            </div>
        </div>

        <!-- Описание -->
        <div class="description">{eventInfo.description}</div>

        <!-- Кнопки -->
        <div class="buttons">
            <button class="register-btn" on:click={register}>Зарегистрироваться</button>
            <button class="online-btn" on:click={joinOnline}>Онлайн встреча</button>
        </div>
    </div>
</div>

