<script lang="ts">
    import Header from "$lib/components/Header.svelte";

    // Поля формы регистрации
    let fullName: string = '';
    let birthDate: string = '';
    let phoneNumber: string = '';
    let email: string = '';
    let studyGroup: string = '';
    let course: string = '';

    // Обработчик отправки формы
    const handleRegister = () => {
        if (fullName && birthDate && phoneNumber && email && studyGroup && course) {
            console.log('ФИО:', fullName);
            console.log('Дата рождения:', birthDate);
            console.log('Номер:', phoneNumber);
            console.log('Почта:', email);
            console.log('Учебная группа:', studyGroup);
            console.log('Курс:', course);
        } else {
            console.log('Заполните все поля!');
        }
    };
</script>

<style>
    /* Общий стиль для страницы */
    :global(body) {
        margin: 0;
        padding: 0;
        font-family: 'DM Sans', sans-serif;
        background-color: #1e1d1c; /* Темный фон */
        color: white; /* Белый текст */
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .login-container {
        position: relative;
        background: #1a1a1a;
        border-radius: 20px;
        padding: 2.5rem;
        width: 400px;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6); /* Более яркая тень */
    }

    /* Градиентная обводка */
    .login-container::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(135deg, #00ff00, #1db954, #00ff99, #2ecc71);
        background-size: 300% 300%;
        border-radius: 23px;
        z-index: -1;
        animation: greenGradient 3s ease infinite;
    }

    @keyframes greenGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .login-container h1 {
        font-size: 2rem;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
        color: #e0e0e0;
        font-weight: bold;
    }

    .login-container input {
        width: 100%;
        margin-bottom: 1.5rem;
        padding: 1rem;
        border-radius: 10px;
        border: none;
        outline: none;
        background: rgba(255, 255, 255, 0.1);
        color: #e0e0e0;
        font-size: 1rem;
        text-align: left;
        transition: background 0.3s ease;
    }

    .login-container input:focus {
        background: rgba(255, 255, 255, 0.2);
    }

    .btn {
        position: relative;
        background: linear-gradient(45deg, #00ff99, #1db954, #2ecc71, #00ff00);
        background-size: 300% 300%;
        padding: 1rem 1.5rem;
        color: white;
        border-radius: 20px;
        font-size: 1.1rem;
        border: none;
        width: 80%;
        animation: buttonGradient 2s linear infinite;
        transition: all 0.3s ease;
        font-family: "Pixelify Sans", serif;
        font-weight: 100;
        font-size: 20px;
    }

    @keyframes buttonGradient {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    .btn:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 255, 0, 0.5);
    }

    .btn:active {
        transform: scale(0.95);
        box-shadow: 0 4px 10px rgba(0, 255, 0, 0.3);
    }
</style>

<div class="login-container">
    <Header />
    <h1 class="title">Регистрация</h1>
    <input type="text" placeholder="ФИО" bind:value={fullName} />
    <input type="date" placeholder="Дата рождения" bind:value={birthDate} />
    <input type="tel" placeholder="Номер телефона" bind:value={phoneNumber} />
    <input type="email" placeholder="Почта" bind:value={email} />
    <input type="text" placeholder="Учебная группа" bind:value={studyGroup} />
    <input type="text" placeholder="Курс" bind:value={course} />
    <button class="btn" on:click={handleRegister}>Зарегистрироваться</button>
</div>
