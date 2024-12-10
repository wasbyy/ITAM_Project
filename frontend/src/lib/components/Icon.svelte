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

<style>
  .icon-container {
    position: absolute;
    top: 35px;
    z-index: 100;
  }

  .icon-container.left {
    left: 35px; /* Если слева */
  }

  .icon-container.right {
    right: 35px; /* Если справа */
  }

  svg {
    fill: currentColor;
    cursor: pointer;
  }
</style>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class="icon-container {left ? 'left' : 'right'}"
  on:click={navigateHome}
>
  <svg class={className} width={width} height={height}>
    <use href={`/images/icons.svg#${id}`} xlink:href={`/images/icons.svg#${id}`} />
  </svg>
</div>
