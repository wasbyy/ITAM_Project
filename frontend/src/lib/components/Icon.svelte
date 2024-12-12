<script>
  import { goto } from '$app/navigation'; // Импортируем goto из $app/navigation (новый API)

  export let id; // ID иконки
  export let className = ""; // Класс для кастомизации стилей
  export let width = 100; // Ширина иконки
  export let height = 34; // Высота иконки
  export let left = true; // Позиция иконки (по умолчанию слева)

  function navigateHome() {
    goto('/'); // Перенаправляем пользователя на главную страницу
  }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<style>
  /* Общий контейнер для иконки */
  .icon-container {
    position: absolute;
    top: 35px; /* Отступ сверху */
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Позиция слева */
  .icon-container.left {
    left: 20px; /* Меньший отступ слева */
  }

  /* Позиция справа */
  .icon-container.right {
    right: 20px; /* Меньший отступ справа */
  }

  /* Стиль для svg */
  svg {
    fill: currentColor;
    cursor: pointer;
    transition: transform 0.3s ease-in-out; /* Анимация при наведении */
  }

  /* Эффект при наведении */
  svg:hover {
    transform: scale(1.1); /* Увеличение при наведении */
  }

  /* Адаптивность для мобильных устройств */
  @media (max-width: 768px) {
    .icon-container {
      top: 20px; /* Уменьшаем отступ сверху на мобильных устройствах */
    }

    svg {
      width: 80px; /* Меньшая ширина иконки на мобильных устройствах */
      height: 28px; /* Меньшая высота на мобильных устройствах */
    }
  }

  @media (max-width: 480px) {
    .icon-container {
      top: 15px; /* Еще меньший отступ сверху */
    }

    svg {
      width: 60px; /* Уменьшаем размер иконки для очень маленьких экранов */
      height: 20px;
    }
  }
</style>

<!-- Контейнер для иконки, с динамическим классом для выравнивания -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
  class="icon-container {left ? 'left' : 'right'}"
  on:click={navigateHome}
>
  <svg class={className} width={width} height={height}>
    <use href={`/images/icons.svg#${id}`} xlink:href={`/images/icons.svg#${id}`} />
  </svg>
</div>
