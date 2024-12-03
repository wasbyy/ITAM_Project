<script>
   import { goto } from '$app/navigation'; // Импортируем goto из $app/navigation (новый API)

   export let id;          // ID иконки
   export let className = ""; // Класс для кастомизации стилей
   export let width = 100;   // Ширина иконки
   export let height = 34;  // Высота иконки

   function navigateHome() {
       goto('http://localhost:5173/mainpage'); // Перенаправляем пользователя на главную страницу
   }
</script>

<style>
   .icon-container {
     position: absolute;
     top: 35px;
     left: 35px;
     z-index: 100;
   }

   svg {
     fill: currentColor;
     cursor: pointer;
   }
</style>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="icon-container" on:click={navigateHome}>
   <svg class={className} width={width} height={height}>
     <use href={`/images/icons.svg#${id}`} xlink:href={`/images/icons.svg#${id}`} />
   </svg>
</div>
