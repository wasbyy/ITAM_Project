<script>
    import EventPanel from './EventPanel.svelte';
  
    const events = [
      {
        title: "Концерт",
        description: "Уникальное музыкальное событие.",
        date: "12/12/2024",
        time: "19:00",
        location: "Москва, Арена",
        tag: "Музыка",
        imageUrl: "/concert.jpg"
      },
      {
        title: "Выставка",
        description: "Искусство в современном мире.",
        date: "15/12/2024",
        time: "10:00",
        location: "СПб, Лофт",
        tag: "Арт",
        imageUrl: "/art.jpg"
      },
      // Добавьте больше мероприятий...
    ];
  </script>
  
  <style>
    .events-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      overflow-y: auto;
      height: calc(100vh - 200px); /* Учитываем отступы */
      padding: 20px 0;
    }
  </style>
  
  <div class="container">
    <!-- Заголовок -->
    <div class="title">Мероприятия</div>
  
    <!-- Список мероприятий -->
    <div class="events-container">
      {#each events as event}
        <EventPanel {...event} />
      {/each}
    </div>
  </div>
  