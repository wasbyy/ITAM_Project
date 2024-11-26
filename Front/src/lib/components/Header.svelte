
  
  <header class="header-container">
      <div class="logo">
          <!-- Вставка изображения вместо текста -->
          <a href="http://localhost:5173/mainpage"> 
              <img src="/src/lib/components/itam_logo.png" alt="Logo" class="logo-img" />
          </a>
      </div>
  
      <div class="user-info">
          <button>Вход</button>
      </div>
  </header>
  
  <style>
      /* Применяем box-sizing ко всем элементам */
      * {
          box-sizing: border-box;
      }
  
      /* Основной стиль для шапки */
      .header-container {
          width: 100%;
          background: #2a2a2a;
          color: white;
          padding: 5px 1%;  /* Убираем лишние отступы и добавляем небольшие отступы слева и справа */
          display: flex;
          align-items: center;
          justify-content: space-between;  /* Распределяет элементы по краям */
          position: fixed;
          top: 0;
          left: 0;
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
          
      }
  
      /* Логотип */
      .logo img {
          height: 50px;
          max-width: 100%; /* Ограничиваем ширину изображения, чтобы оно не выходило за пределы */
      }
  
      /* Стиль кнопки */
      .user-info button {
          background: #444;
          border: none;
          padding: 0.6rem 1rem;
          color: white;
          cursor: pointer;
          font-family: 'DM Sans', sans-serif;
          font-weight: bold;
          border-radius: 10px;
          transition: background-color 0.3s ease;
          white-space: nowrap; /* Останавливает перенос текста внутри кнопки */
          
      }
  
      .user-info button:hover {
          background-color: #5900ff;
      }
  </style>
  