<script lang="ts">
    import { onMount } from "svelte";
    import Icon from "$lib/components/Icon.svelte";
    import { BASE_URL } from "../../../config";
    import { getCookie } from "$lib/utils/utilCookie"; // Импортируем функцию для получения куки
    import { goto } from "$app/navigation";

    // Тип данных для завершенных мероприятий
    interface CompletedEvent {
        event_id: number;
        event_name: string;
        date: string;
        image?: string; // Поле для изображения
    }

    let events: CompletedEvent[] = [];
    let isLoading = true; // Состояние загрузки

    // Функция для загрузки завершенных мероприятий
    async function loadCompletedEvents(): Promise<void> {
        try {
            // Получаем токен из куки
            const token = getCookie('auth_token');
            if (!token) {
                console.error("Токен отсутствует. Пользователь не авторизован.");
                return;
            }

            // Выполняем запрос с токеном в заголовке
            const response = await fetch(`${BASE_URL}/user_completed_events`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`, // Передаем токен в заголовке
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                const data: CompletedEvent[] = await response.json();

                // Загружаем изображения для каждого события
                const eventsWithImages = await Promise.all(data.map(async (event) => {
                    const imageUrl = await fetchEventImage(event.event_id); // Загружаем изображение для текущего мероприятия
                    return {
                        ...event,
                        image: imageUrl, // Присваиваем загруженное изображение
                    };
                }));

                events = eventsWithImages.map(event => ({
                    ...event,
                    date: new Date(event.date).toLocaleDateString(),
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

    // Функция для получения изображения для мероприятия
    async function fetchEventImage(eventId: number): Promise<string> {
        try {
            const response = await fetch(`${BASE_URL}/show_event_image/${eventId}`);
            if (response.ok) {
                const imageBlob = await response.blob();
                return URL.createObjectURL(imageBlob); // Возвращаем URL для изображения
            } else {
                console.error(`Ошибка загрузки изображения для мероприятия с ID ${eventId}: ${response.status}`);
                return "https://via.placeholder.com/150"; // Если изображения нет, возвращаем заглушку
            }
        } catch (error) {
            console.error(`Ошибка запроса изображения для мероприятия с ID ${eventId}:`, error);
            return "https://via.placeholder.com/150"; // Если произошла ошибка, возвращаем заглушку
        }
    }

    // Загружаем мероприятия при монтировании компонента
    onMount(() => {
        loadCompletedEvents();
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
        width: 100vw;
        height: 100vh;
        background-color: #171615;
        z-index: -1;
    }

    .container {
        max-width: 84%;
        margin: 20px auto;
        padding: 20px;
        color: white;
    }

    h1 {
        color: white;
        text-align: left;
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
        background-color: #333;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        padding: 22px;
        width: 265px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .card img {
        width: 100%;
        height: 100%; /* Сделаем высоту равной ширине, чтобы изображение было квадратным */
        display: block;
        border-radius: 6px;
        object-fit: cover; /* Обеспечивает, что изображение будет масштабироваться без искажения */
        box-sizing: border-box; /* Учитываем рамку в размере изображения */
    }

    .card-title {
        margin-top: 20px;
        margin-bottom: 10px;
        font-size: 24px;
        color: white;
        text-align: center;
    }

    .card-date {
        color: #aaa;
        text-align: center;
    }
</style>



<Icon id="logo" left={false} />
<div class="background-container"></div>

<div class="container">
    <h1>Завершенные мероприятия</h1>
    <div class="grid">
        {#each events as event}
            <div class="card">
                <!-- Используем правильные поля из объекта -->
                <img src={event.image} alt={event.event_name} />
                <div class="card-title">{event.event_name}</div>
                <div class="card-date">{event.date}</div>
            </div>
        {/each}
    </div>
</div>
