<script lang="ts">
    import { onMount } from "svelte";
    import Icon from "$lib/components/Icon.svelte";

    // Определяем интерфейс для события
    interface Event {
        id: number; // ID события
        title: string; // Название события
        image: string; // URL изображения
        date: string; // Дата события
    }

    // Типизируем массив мероприятий
    let events: Event[] = [];

    // Функция для загрузки завершенных мероприятий пользователя
    async function loadCompletedEvents(): Promise<void> {
        try {
            const token = localStorage.getItem('auth_token');
            if (!token) {
                console.error("Токен отсутствует. Пользователь не авторизован.");
                return;
            }

            // Получаем user_id из токена или другого хранилища
            const userId = token; // Пример использования токена в качестве user_id
            const response = await fetch(`/user_completed_events/${userId}`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`, // Заголовок авторизации
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                const data: Array<{
                    event_id: number;
                    event_name: string;
                    date: string;
                }> = await response.json();

                // Преобразуем данные в формат, который ожидается для отображения
                events = data.map(event => ({
                    id: event.event_id,
                    title: event.event_name,
                    image: "https://via.placeholder.com/150", // Если есть изображение, можно заменить
                    date: new Date(event.date).toLocaleDateString(), // Форматируем дату
                    description: "", // Поскольку данные не содержат описания, оставляем пустую строку
                    place: "", // Место проведения оставляем пустым
                    tags: [] // Теги оставляем пустым массивом
                }));
            } else {
                console.error("Ошибка при получении данных:", response.status);
            }
        } catch (error) {
            console.error("Ошибка при запросе данных:", error);
        }
    }

    // Загружаем завершенные события при монтировании компонента
    onMount(() => {
        loadCompletedEvents();
    });
</script>

<style>
    /* Ваши стили остаются без изменений */
    * {
        font-family: "Inter", sans-serif;
    }

    .background-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: #1d1d1d;
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
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        padding: 10px;
        width: 265px;
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
        font-size: 32px;
        color: white;
        text-align: center;
    }

    .card-description {
        color: white;
        text-align: center;
    }
</style>

<Icon id="logo" left={false}/>
<div class="background-container"></div>

<div class="container">
    <h1>Завершенные мероприятия</h1>
    <div class="grid">
        {#each events as event}
            <div class="card">
                <img src={event.image} alt={event.title} />
                <div class="card-title">{event.title}</div>
                <div class="card-date">{event.date}</div>
            </div>
        {/each}
    </div>
</div>
