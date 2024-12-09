<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import Icon from "$lib/components/Icon.svelte";
    import { BASE_URL } from "../../../config";

    interface EventData {
        event_name: string;
        place: string;
        long_description: string;
        max_count_of_members: number;
        online_event_link?: string;
        format: string;
        tags: string;
        date: string; // ISO-строка с датой и временем
        is_active: boolean;
    }

    let eventInfo = {
        photo: "",
        title: "Название мероприятия",
        date: "",
        time: "",
        location: "",
        format: "",
        participants: "",
        maxCountOfMembers: 0,
        description: "",
        onlineLink: "",
    };

    let loading = true;
    let error = "";
    let isAuthorized = false;
    let showNotification = false;
    let notificationMessage = "";
    let notificationType: "success" | "error" = "error";

    function checkAuthorization() {
        const token = localStorage.getItem("auth_token");
        isAuthorized = !!token;
    }

    function formatDateTime(isoDate: string) {
        const dateObj = new Date(isoDate);
        if (isNaN(dateObj.getTime())) {
            return "Некорректная дата";
        }
        const options: Intl.DateTimeFormatOptions = {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        };
        return dateObj.toLocaleString("ru-RU", options);
    }

    async function fetchEventImage(eventId: string) {
        const imageUrl = `${BASE_URL}/show_event_image/${eventId}`;
        try {
            const response = await fetch(imageUrl);
            if (response.ok) {
                return imageUrl;
            } else {
                console.warn("Изображение не найдено, используется placeholder");
                return "";
            }
        } catch (err) {
            console.error("Ошибка загрузки изображения:", err);
            return "";
        }
    }

    async function fetchRegisteredCount(eventId: string) {
        const API_URL = `${BASE_URL}/count_members/${eventId}`;
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error(`Ошибка загрузки количества участников: ${response.status}`);
            }
            const data = await response.json();
            const currentCount = typeof data === "number" ? data : 0;
            eventInfo.participants = `Участников: ${currentCount}/${eventInfo.maxCountOfMembers}`;
        } catch (err) {
            console.error("Ошибка получения количества участников:", err);
            eventInfo.participants = `Участников: неизвестно/${eventInfo.maxCountOfMembers}`;
        }
    }

    async function fetchEventData(eventId: string) {
        const API_URL = `${BASE_URL}/events/${eventId}`;
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error(`Ошибка загрузки данных: ${response.status}`);
            }
            const data: EventData = await response.json();

            const [formattedDate, formattedTime] = formatDateTime(data.date).split(", ");
            const eventPhoto = await fetchEventImage(eventId);

            eventInfo = {
                photo: eventPhoto,
                title: data.event_name,
                date: formattedDate,
                time: formattedTime,
                location: data.place,
                format: `Формат мероприятия: ${data.format}`,
                participants: `Участников: 0/${data.max_count_of_members}`,
                maxCountOfMembers: data.max_count_of_members,
                description: data.long_description,
                onlineLink: data.online_event_link || "",
            };

            await fetchRegisteredCount(eventId);
        } catch (err) {
            console.error("Ошибка загрузки данных события:", err);
            error = (err as Error).message;
        } finally {
            loading = false;
        }
    }

    $: {
        const eventId = $page.params.event_id;
        if (eventId) {
            fetchEventData(eventId);
        } else {
            error = "Некорректный идентификатор события.";
            loading = false;
        }
    }

    onMount(() => {
        checkAuthorization();
    });

    async function register() {
    if (!isAuthorized) {
        notificationType = "error";
        showNotification = true;
        notificationMessage = "Для регистрации войдите в аккаунт.";
        return;
    }

    const token = localStorage.getItem("auth_token");
    if (!token) {
        notificationType = "error";
        showNotification = true;
        notificationMessage = "Ошибка авторизации. Повторите вход.";
        return;
    }

    const eventId = parseInt($page.params.event_id, 10);
    if (isNaN(eventId)) {
        notificationType = "error";
        showNotification = true;
        notificationMessage = "Ошибка: некорректный идентификатор события.";
        return;
    }

    const API_URL = `${BASE_URL}/add_member?event_id=${eventId}`;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                Authorization: `${token}`,
            },
        });

        // Проверка на 401 ошибку
        if (response.status === 401) {
            notificationType = "error";
            showNotification = true;
            notificationMessage = "Для регистрации войдите в аккаунт.";
            return;
        }

        if (!response.ok) {
            throw new Error(`Ошибка регистрации: ${response.statusText}`);
        }

        const result = await response.json();
        notificationType = "success";
        showNotification = true;
        notificationMessage = "Вы успешно зарегистрировались на мероприятие!";

        await fetchRegisteredCount(String(eventId));
    } catch (err) {
        notificationType = "error";
        showNotification = true;
        notificationMessage = "Не удалось зарегистрироваться. Попробуйте позже.";
    }
}


    function joinOnline() {
        if (eventInfo.onlineLink) {
            window.open(eventInfo.onlineLink, "_blank");
        } else {
            alert("Ссылка на онлайн встречу недоступна.");
        }
    }

    function closeNotification() {
        showNotification = false;
        notificationMessage = "";
    }
</script>

<div class="icon"><Icon id="logo" /></div>

{#if loading}
    <div class="loading">Загрузка...</div>
{:else if error}
    <div class="error">{error}</div>
{:else}
    <div class="page-background">
        <div class="event-page">
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

            <div class="description">{eventInfo.description}</div>

            <div class="buttons">
                <button class="register-btn" on:click={register}>Зарегистрироваться</button>

                {#if eventInfo.onlineLink.trim() !== ""}
                    <button class="online-btn" on:click={joinOnline}>Онлайн встреча</button>
                {/if}
            </div>
        </div>
    </div>

    {#if showNotification}
        <div class="notification {notificationType}">
            <p>{notificationMessage}</p>
            <button on:click={closeNotification}>Закрыть</button>
        </div>
    {/if}
{/if}



<style>.page-background {
    background-color: #171615;
    background-image: url('/eventbackground.png');
    background-size: cover;
    background-position: center center;
    min-height: 100vh;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    position: absolute;
    top: 0;
    left: 0;
}

.event-page {
    background-color: rgba(36, 36, 35, 0.9);
    color: white;
    padding: 30px;
    max-width: 1200px;
    width: 100%;
    min-height: 50vh;
    margin-top: 90px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: flex-start; /* Выравниваем все элементы по левому краю */
}

.header {
    display: flex;
    gap: 30px;
    margin-bottom: 30px;
    align-items: flex-start;
    flex-wrap: nowrap; /* Элементы не переносятся */
    width: 100%;
    justify-content: flex-start; /* Выравниваем блоки по левому краю */
}

.event-photo {
    width: 400px; /* Ширина изображения */
    height: 400px; /* Высота изображения */
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
    gap: 15px; /* Увеличен отступ между информацией */
    max-width: 600px;
    margin-left: 30px; /* Отступ между фото и текстом */
    text-align: left; /* Текст выравниваем по левому краю */
}

.event-title {
    font-size: 48px;
    font-weight: bold;
    margin: 0;
    margin-bottom: 20px; /* Уменьшен отступ снизу */
    font-family: 'Press Start 2P', monospace;
}

.event-meta {
    display: flex;
    gap: 20px;
    font-size: 28px; /* Уменьшен шрифт для лучшего восприятия */
    color: #888;
    font-family: "Inter", sans-serif;
}

.event-format, .event-participants {
    font-size: 28px;
    color: #888;
    margin-bottom: 50px; /* Уменьшен отступ снизу */
    font-family: "Inter", sans-serif;
}

.description {
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 24px;
    margin-top: 20px; /* Отступ сверху */
    word-wrap: break-word;
    font-family: "Inter", sans-serif;
    max-height: none;
    flex-grow: 1;
    width: calc(100% -20px); /* Равняется ширине контейнера минус ширина изображения + отступ */
    text-align: left;
}

.buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 30px; /* Увеличен отступ между описанием и кнопками */
    flex-wrap: wrap;
    width: 100%;
    justify-content: space-between; /* Располагаем кнопки по бокам */
}

.register-btn,
.online-btn {
    flex: 0 0 15%; /* Кнопки занимают по 45% ширины */
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
    margin: 5px 0;
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

/* Уведомление */
.notification {
    position: fixed;
    bottom: 20px;
    left: 55px;
    color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    font-size: 16px;
    background-color: var(--notification-bg, #f44336);
}

.notification.success {
    --notification-bg: #4CAF50;
}

.notification.error {
    --notification-bg: #f44336;
}

.notification button {
    margin-top: 10px;
    background-color: #444;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
}

.notification button:hover {
    background-color: #666;
}

/* Медиазапросы для мобильных устройств */
@media (max-width: 768px) {
    .header {
        flex-direction: column;
        align-items: center;
        margin-bottom: 20px;
    }

    .event-photo {
        width: 100%; /* Изображение будет занимать всю ширину экрана */
        height: auto; /* Сохраняем пропорции */
        margin-bottom: 20px;
    }

    .event-details {
        width: 100%; /* Контент будет занимать всю ширину */
        text-align: center; /* Выравниваем текст по центру */
    }

    .event-title {
        font-size: 36px; /* Уменьшаем размер шрифта на мобильных устройствах */
    }

    .event-meta {
        font-size: 20px;
        gap: 20px;
        text-align: center;
    }

    .event-format, .event-participants {
        font-size: 20px;
    }

    .description {
        font-size: 18px;
        word-wrap: break-word;
    }

    .buttons {
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .register-btn,
    .online-btn {
        width: 90%; /* Кнопки занимают 90% ширины экрана */
        font-size: 14px;
        margin: 10px 0;
    }
}

/* Медиазапросы для планшетов */
@media (max-width: 1024px) {
    .event-photo {
        width: 300px;
        height: 300px;
    }

    .event-title {
        font-size: 42px;
    }

    .event-meta {
        flex-direction: column; /* На мобильных устройствах мы меняем направление на вертикальное */
        align-items: center; /* Выравнивание по центру по оси X */
        font-size: 24px; /* Уменьшаем шрифт для мобильных устройств */
        gap: 10px; /* Уменьшаем расстояние между элементами */
    }

    .event-format, .event-participants {
        font-size: 26px;
    }
}

.event-title {
    font-size: clamp(24px, 6vw, 48px); /* Размер шрифта будет от 24px до 48px, и динамически изменяться в зависимости от ширины экрана */
}

.event-meta {
    font-size: clamp(14px, 3vw, 32px); /* Шрифт будет адаптироваться между 14px и 32px */
}

.event-format,
.event-participants {
    font-size: clamp(16px, 3vw, 32px); /* Для формата и участников тоже динамическое изменение */
}

</style>
