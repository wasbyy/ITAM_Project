<script lang="ts">
    import { onMount } from "svelte";
    import Icon from "$lib/components/Icon.svelte";
    import { BASE_URL } from "../../../config";
    import { goto } from "$app/navigation";

    interface ArchivedEvent {
        event_id: number;
        event_name: string;
        date: string;
        short_description: string;
        place: string;
        tags: string[];
        image?: string;
    }

    let events: ArchivedEvent[] = [];
    let isLoading = true; // Состояние загрузки

    async function loadArchivedEvents(): Promise<void> {
        try {
            const response = await fetch(`${BASE_URL}/archived_events`);
            if (response.ok) {
                const data: ArchivedEvent[] = await response.json();

                // Параллельная загрузка изображений
                const images = await Promise.all(data.map(event => fetchEventImage(event.event_id)));

                // Ассоциируем изображения с мероприятиями
                events = data.map((event, index) => ({
                    ...event,
                    image: images[index] || "https://avatars.mds.yandex.net/i?id=166c32386ec148d145f75f850da055e2298d59d7-12472594-images-thumbs&n=13",
                }));
            } else {
                console.error("Ошибка при получении данных:", response.status);
            }
        } catch (error) {
            console.error("Ошибка при запросе данных:", error);
        } finally {
            isLoading = false;
        }
    }

    async function fetchEventImage(eventId: number): Promise<string> {
        try {
            const response = await fetch(`${BASE_URL}/show_event_image/${eventId}`);
            if (response.ok) {
                const imageBlob = await response.blob();
                return URL.createObjectURL(imageBlob);
            } else {
                console.error(`Ошибка загрузки изображения для мероприятия с ID ${eventId}: ${response.status}`);
                return "";
            }
        } catch (error) {
            console.error(`Ошибка запроса изображения для мероприятия с ID ${eventId}:`, error);
            return "";
        }
    }

    function navigateToEvent(eventId: number): void {
        goto(`/archive_event/${eventId}`);
    }

    onMount(() => {
        loadArchivedEvents();
    });
</script>

<style>
    * {
        font-family: "Inter", sans-serif;
    }

    .background-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #171615;
        z-index: -1;
    }

    .container {
        max-width: 100%;
        margin: 20px auto;
        padding: 20px;
        color: white;
    }

    h1 {
        color: white;
        text-align: center;
        font-size: 64px;
        margin-bottom: 50px;
        text-transform: uppercase;
    }

    .grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
    }

    .card {
        cursor: pointer;
        background-color: #333;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        padding: 10px;
        width: 250px;
        text-decoration: none;
        display: block;
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .card img {
        width: 90%;
        margin: 10px auto;
        display: block;
        border-radius: 6px;
    }

    .card-title {
        margin-top: 20px;
        margin-bottom: 10px;
        font-size: 28px;
        color: white;
        text-align: center;
    }

    .loading-message {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        color: white;
        font-size: 32px;
        font-weight: bold;
        text-transform: uppercase;
    }

    .logo {
        margin-left: 75px;
    }

    /* Медиазапросы для мобильных устройств */
    @media (max-width: 768px) {
        h1 {
            margin-top: 40px;
            font-size: 32px;  /* Меньший шрифт для заголовка */
            margin-bottom: 20px;
        }

        .card {
            width: 48%;  /* Карточки занимают 48% ширины контейнера */
            max-width: 320px; /* Ограничение ширины */
            margin-bottom: 20px;  /* Отступ снизу */
        }

        .grid {
            flex-wrap: wrap; /* Карточки переносятся на следующую строку */
            justify-content: space-between; /* Пробел между карточками */
        }

        .card-title {
            font-size: 20px; /* Уменьшаем размер текста */
        }
    }

    @media (max-width: 480px) {
        .card-title {
            font-size: 18px; /* Еще меньше шрифт для мелких экранов */
        }

        .loading-message {
            font-size: 24px; /* Меньший шрифт при загрузке */
        }

        .card img {
            width: 80%;  /* Уменьшаем размер изображения */
        }
    }
</style>

<div class="logo"><Icon id="logo" left={false} /></div>
<div class="background-container"></div>

<div class="container">
    {#if isLoading}
        <div class="loading-message">Загрузка...</div>
    {:else}
        <h1>Архивные мероприятия</h1>
        <div class="grid">
            {#each events as event}
            <a href={`/archive_event/${event.event_id}`} class="card">
                <img src={event.image} alt={event.event_name} />
                <div class="card-title">{event.event_name}</div>
            </a>
            {/each}
        </div>
    {/if}
</div>
    