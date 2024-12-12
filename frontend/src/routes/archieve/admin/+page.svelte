<script lang="ts">
    import { onMount } from "svelte";
    import Icon from "$lib/components/Icon.svelte";
    import { BASE_URL } from "../../../config";
    import { getCookie } from "$lib/utils/utilCookie"; // Импортируем функцию для получения куки
    import { goto } from "$app/navigation"; // Импортируем функцию для навигации

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
            const response = await fetch(`${BASE_URL}/archived_events`, {
                method: 'GET',
                headers: {
                    Authorization: `${token}`, // Передаем токен в заголовке
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

    // Функция для обработки клика по мероприятию
    function handleEventClick(eventId: number) {
        goto(`/event/${eventId}`);
    }
</script>

<style>
    * {
        font-family: "Inter", sans-serif;
        box-sizing: border-box; /* Это поможет избежать сдвигов на мобильных устройствах */
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
        max-width: 100%;
        margin: 0px auto;
        padding: 10px;
        padding-left: 40px;
        color: white;
    }

    h1 {
        color: white;
        text-align: left;
        font-size: 2.5rem; /* Для мобильных экранов уменьшаем шрифт */
        margin-bottom: 50px;
        text-transform: uppercase;
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); /* Сделаем сетку с минимальной шириной карточки 220px */
        gap: 20px;
        justify-items: center;
    }

    .card {
        background-color: #333;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        padding: 15px;
        width: 100%; /* Карточка растягивается по ширине контейнера */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        cursor: pointer; /* Добавим курсор при наведении */
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .card img {
        width: 100%;
        height: 100%; /* Заполняем весь блок */
        display: block;
        border-radius: 6px;
        object-fit: cover; /* Изображение будет заполнять весь блок, сохраняя свои пропорции */
        box-sizing: border-box;
    }

    .card-title {
        margin-top: 15px;
        margin-bottom: 10px;
        font-size: 1.2rem; /* Уменьшаем шрифт */
        color: white;
        text-align: center;
    }

    .card-date {
        color: #aaa;
        text-align: center;
        font-size: 0.9rem; /* Уменьшаем шрифт для даты */
    }

    @media (max-width: 768px) {
        .container {
            padding: 15px; /* Уменьшаем отступы на мобильных */
        }

        h1 {
            font-size: 1.8rem; /* Уменьшаем размер шрифта заголовка */
            margin-bottom: 20px;
        }

        .card img {
            height: 300px;
            width: 300px; /* Еще меньше изображение на маленьких экранах */
        }

        .card-title {
            font-size: 1rem; /* Уменьшаем размер текста */
        }

        .card-date {
            font-size: 0.8rem; /* Еще меньше размер текста для даты */
        }
    }
</style>

<Icon id="logo" left={false} />
<div class="background-container"></div>

<div class="container">
    <h1>Завершенные мероприятия</h1>
    <div class="grid">
        {#each events as event}
            <div class="card" on:click={() => handleEventClick(event.event_id)}>
                <img src={event.image} alt={event.event_name} />
                <div class="card-title">{event.event_name}</div>
                <div class="card-date">{event.date}</div>
            </div>
        {/each}
    </div>
</div>
