WELCOME_MESSAGE = {
    'en': "Welcome! Please select your language.",
    'ru': "Добро пожаловать! Пожалуйста, выберите язык."
}

START_MESSAGE = {
    'en': "Welcome to Gym Bro Bot, {name}! 💪\n"
          "I'm here to help you track your workouts and make those gains! 🏋️‍♂️\n"
          "Use /help to see what I can do for you.\n"
          "Don't forget to set up your profile with /profile!",
    'ru': "Добро пожаловать в Gym Bro Bot, {name}! 💪\n"
          "Я здесь, чтобы помочь тебе отслеживать тренировки и набирать массу! 🏋️‍♂️\n"
          "Используй /help, чтобы узнать, что я могу для тебя сделать.\n"
          "Не забудь настроить свой профиль с помощью /profile!"
}

HELP_MESSAGE = {
    'en': ("Here's what I can do for you, bro:\n\n"
           "/start - Get pumped and start using the bot\n"
           "/help - Show this help message\n"
           "/profile - Set up or update your profile (height, weight, gender)\n"
           "/track_workout - Log your latest workout\n"
           "/view_progress - Check out your gains over time\n"
           "/motivation - Get a motivational quote to crush your workout\n"
           "/remind_legday - Set a reminder for leg day (never skip it!)\n"
           "/analytics_weights - View your weight progress over time\n\n"
           "Remember, every rep counts! Let's get those gains! 💪😤"),
    'ru': ("Вот что я могу для тебя сделать, бро:\n\n"
           "/start - Начать использование бота\n"
           "/help - Показать это сообщение помощи\n"
           "/profile - Настроить или обновить свой профиль (рост, вес, пол)\n"
           "/track_workout - Записать твою последнюю тренировку\n"
           "/view_progress - Проверить твой прогресс\n"
           "/motivation - Получить мотивирующую цитату для тренировки\n"
           "/remind_legday - Установить напоминание о дне ног (никогда не пропускай!)\n"
           "/analytics_weights - Просмотреть прогресс твоего веса со временем\n\n"
           "Помни, каждое повторение имеет значение! Давай набирать массу! 💪😤")
}

PROFILE_MESSAGES = {
    'en': {
        'gender_prompt': "Let's set up your profile! First, please select your gender:",
        'male': "Male",
        'female': "Female",
        'skip': "Skip",
        'height_prompt': "Great! Now, please enter your height in cm (or type 'skip' to skip):",
        'weight_prompt': "Almost done! Please enter your weight in kg (or type 'skip' to skip):",
        'invalid_height': "Oops! That doesn't look like a valid height. Please enter a number in cm.",
        'invalid_weight': "Oops! That doesn't look like a valid weight. Please enter a number in kg.",
        'profile_updated': "Awesome! Your profile has been updated. You're all set to start tracking your gains!",
        'cancelled': "Profile update cancelled. No worries, you can always update it later!",
        'update_prompt': "Let's update your profile! We'll start with your height and weight.",
        'update_weight_prompt': "Let's update your weight. Please enter your current weight in kg (or type 'skip' to skip):",
        'weight_skipped': "Weight update skipped. Your previous weight record remains unchanged.",
        'weight_updated': "Great! Your weight has been updated to {weight} kg.",
    },
    'ru': {
        'gender_prompt': "Давайте настроим ваш профиль! Для начала, пожалуйста, выберите ваш пол:",
        'male': "Мужской",
        'female': "Женский",
        'skip': "Пропустить",
        'height_prompt': "Отлично! Теперь, пожалуйста, введите ваш рост в см (или напишите 'пропустить'):",
        'weight_prompt': "Почти готово! Пожалуйста, введите ваш вес в кг (или напишите 'пропустить'):",
        'invalid_height': "Упс! Это не похоже на правильный рост. Пожалуйста, введите число в см.",
        'invalid_weight': "Упс! Это не похоже на правильный вес. Пожалуйста, введите число в кг.",
        'profile_updated': "Отлично! Ваш профиль обновлен. Вы готовы начать отслеживать свои достижения!",
        'cancelled': "Обновление профиля отменено. Не беспокойтесь, вы всегда можете обновить его позже!",
        'update_prompt': "Давайте обновим ваш профиль! Начнем с вашего роста и веса.",
        'update_weight_prompt': "Д��вайте обновим ваш вес. Пожалуйста, введите ваш текущий вес в кг (или напишите 'пропустить'):",
        'weight_skipped': "Обновление веса пропущено. Ваша предыдущая запись веса осталась без изменений.",
        'weight_updated': "Отлично! Ваш вес обновлен до {weight} кг.",
    }
}

ANALYTICS_MESSAGES = {
    'en': {
        'no_data': "You haven't set up your profile yet. Use /profile to get started!",
        'no_weight_data': "You haven't recorded any weight data yet. Use /profile to update your weight!",
        'weight_chart_title': "Your Weight History",
        'date_label': "Date",
        'weight_label': "Weight (kg)",
        'analysis_text': "Initial weight: {initial_weight:.1f} kg\n"
                         "Current weight: {current_weight:.1f} kg\n"
                         "You have {direction} {weight_change:.1f} kg since your first record.",
        'gained': "gained",
        'lost': "lost"
    },
    'ru': {
        'no_data': "Вы еще не настроили свой профиль. Используйте /profile, чтобы начать!",
        'no_weight_data': "Вы еще не записали данные о весе. Используйте /profile, чтобы обновить свой вес!",
        'weight_chart_title': "История вашего веса",
        'date_label': "Дата",
        'weight_label': "Вес (кг)",
        'analysis_text': "Начальный вес: {initial_weight:.1f} кг\n"
                         "Текущий вес: {current_weight:.1f} кг\n"
                         "Вы {direction} {weight_change:.1f} кг с момента первой записи.",
        'gained': "набрали",
        'lost': "потеряли"
    }
}
