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
                image: images[index] || "https://via.placeholder.com/150",
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
        gap: 40px;
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

    .card-description {
        font-size: 14px;
        color: #ccc;
        text-align: center;
        margin-bottom: 20px;
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
</style>

<Icon id="logo" left={false} />
<div class="background-container"></div>

<div class="container">
    {#if isLoading}
        <div class="loading-message">Загрузка...</div>
    {:else}
        <h1>Архивные мероприятия</h1>
        <div class="grid">
            {#each events as event}
                <div class="card" on:click={() => navigateToEvent(event.event_id)}>
                    <img src={event.image} alt={event.event_name} />
                    <div class="card-title">{event.event_name}</div>
                </div>
            {/each}
        </div>
    {/if}
</div>
