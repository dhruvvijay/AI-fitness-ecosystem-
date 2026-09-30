-- ═══════════════════════════════════════════════════════════════
-- AI Fitness Ecosystem — Complete MySQL Schema
-- Version: 1.0.0
-- ═══════════════════════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS ai_fitness_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ai_fitness_db;

-- ── Users & Authentication ─────────────────────────────────────

CREATE TABLE users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255),
    full_name       VARCHAR(255) NOT NULL,
    role            ENUM('admin','trainer','user') NOT NULL DEFAULT 'user',
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified     BOOLEAN NOT NULL DEFAULT FALSE,
    auth_provider   ENUM('email','google') NOT NULL DEFAULT 'email',
    google_id       VARCHAR(255) UNIQUE,
    avatar_url      VARCHAR(500),
    last_login      VARCHAR(50),
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_role (role)
) ENGINE=InnoDB;

CREATE TABLE user_profiles (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL UNIQUE,
    date_of_birth       DATE,
    gender              ENUM('male','female','other'),
    height_cm           FLOAT,
    weight_kg           FLOAT,
    target_weight_kg    FLOAT,
    activity_level      ENUM('sedentary','light','moderate','active','very_active') DEFAULT 'moderate',
    fitness_goal        ENUM('lose_weight','maintain','gain_muscle','improve_fitness') DEFAULT 'maintain',
    diet_preference     ENUM('none','vegetarian','vegan','keto','high_protein','indian') DEFAULT 'none',
    body_fat_percentage FLOAT,
    daily_calorie_target INT,
    daily_protein_target INT,
    daily_water_target_ml INT DEFAULT 2500,
    daily_step_target    INT DEFAULT 10000,
    workout_days_per_week INT DEFAULT 4,
    timezone            VARCHAR(50) DEFAULT 'Asia/Kolkata',
    bio                 TEXT,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE user_settings (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    user_id                 INT NOT NULL UNIQUE,
    theme                   ENUM('dark','light','system') DEFAULT 'system',
    language                VARCHAR(10) DEFAULT 'en',
    units                   ENUM('metric','imperial') DEFAULT 'metric',
    notifications_enabled   BOOLEAN DEFAULT TRUE,
    email_notifications     BOOLEAN DEFAULT TRUE,
    push_notifications      BOOLEAN DEFAULT TRUE,
    workout_reminders       BOOLEAN DEFAULT TRUE,
    meal_reminders          BOOLEAN DEFAULT TRUE,
    water_reminders         BOOLEAN DEFAULT TRUE,
    privacy_profile_public  BOOLEAN DEFAULT FALSE,
    privacy_show_on_leaderboard BOOLEAN DEFAULT TRUE,
    created_at              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE auth_tokens (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    token_hash  VARCHAR(512) NOT NULL,
    token_type  VARCHAR(20) NOT NULL,
    expires_at  DATETIME NOT NULL,
    is_revoked  BOOLEAN NOT NULL DEFAULT FALSE,
    device_info VARCHAR(500),
    ip_address  VARCHAR(45),
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_auth_tokens_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE otp_codes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    code        VARCHAR(10) NOT NULL,
    purpose     VARCHAR(50) NOT NULL,
    expires_at  DATETIME NOT NULL,
    is_used     BOOLEAN NOT NULL DEFAULT FALSE,
    attempts    INT NOT NULL DEFAULT 0,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_otp_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE password_resets (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    token       VARCHAR(255) NOT NULL UNIQUE,
    expires_at  DATETIME NOT NULL,
    is_used     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_reset_token (token),
    INDEX idx_reset_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Fitness Tracking ───────────────────────────────────────────

CREATE TABLE steps_daily (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    date            DATE NOT NULL,
    total_steps     INT NOT NULL DEFAULT 0,
    distance_km     FLOAT DEFAULT 0.0,
    calories_burned FLOAT DEFAULT 0.0,
    walking_minutes INT DEFAULT 0,
    running_minutes INT DEFAULT 0,
    goal_steps      INT DEFAULT 10000,
    goal_completed  BOOLEAN DEFAULT FALSE,
    source          VARCHAR(50) DEFAULT 'manual',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_steps_user_date (user_id, date),
    INDEX idx_steps_user (user_id),
    INDEX idx_steps_date (date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE steps_hourly (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    date            DATE NOT NULL,
    hour            INT NOT NULL,
    steps           INT NOT NULL DEFAULT 0,
    distance_km     FLOAT DEFAULT 0.0,
    calories_burned FLOAT DEFAULT 0.0,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_steps_hourly (user_id, date, hour),
    INDEX idx_steps_hourly_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE calorie_logs (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    date        DATE NOT NULL,
    log_type    VARCHAR(20) NOT NULL,
    amount      FLOAT NOT NULL,
    source      VARCHAR(100),
    source_id   INT,
    notes       TEXT,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_calorie_user_date (user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE water_logs (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    date        DATE NOT NULL,
    amount_ml   INT NOT NULL,
    time_logged DATETIME,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_water_user_date (user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE bmi_records (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL,
    date                DATE NOT NULL,
    weight_kg           FLOAT NOT NULL,
    height_cm           FLOAT NOT NULL,
    bmi                 FLOAT NOT NULL,
    body_fat_percentage FLOAT,
    lean_body_mass      FLOAT,
    bmr                 FLOAT,
    tdee                FLOAT,
    category            VARCHAR(50),
    notes               TEXT,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_bmi_user_date (user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE body_measurements (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL,
    date                DATE NOT NULL,
    weight_kg           FLOAT,
    chest_cm            FLOAT,
    waist_cm            FLOAT,
    hips_cm             FLOAT,
    bicep_left_cm       FLOAT,
    bicep_right_cm      FLOAT,
    thigh_left_cm       FLOAT,
    thigh_right_cm      FLOAT,
    calf_left_cm        FLOAT,
    calf_right_cm       FLOAT,
    neck_cm             FLOAT,
    forearm_cm          FLOAT,
    shoulder_cm         FLOAT,
    body_fat_percentage FLOAT,
    notes               TEXT,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_measurements_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE progress_photos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    date        DATE NOT NULL,
    photo_url   VARCHAR(500) NOT NULL,
    photo_type  VARCHAR(20) DEFAULT 'front',
    weight_kg   FLOAT,
    notes       TEXT,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_photos_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Nutrition ──────────────────────────────────────────────────

CREATE TABLE foods (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    name              VARCHAR(255) NOT NULL,
    category          VARCHAR(100),
    serving_size      VARCHAR(100),
    serving_weight_g  FLOAT,
    calories          FLOAT NOT NULL,
    protein_g         FLOAT DEFAULT 0.0,
    carbs_g           FLOAT DEFAULT 0.0,
    fat_g             FLOAT DEFAULT 0.0,
    fiber_g           FLOAT DEFAULT 0.0,
    sugar_g           FLOAT DEFAULT 0.0,
    sodium_mg         FLOAT DEFAULT 0.0,
    calcium_mg        FLOAT DEFAULT 0.0,
    iron_mg           FLOAT DEFAULT 0.0,
    potassium_mg      FLOAT DEFAULT 0.0,
    vitamin_a_mcg     FLOAT DEFAULT 0.0,
    vitamin_c_mg      FLOAT DEFAULT 0.0,
    vitamin_d_mcg     FLOAT DEFAULT 0.0,
    magnesium_mg      FLOAT DEFAULT 0.0,
    water_g           FLOAT DEFAULT 0.0,
    is_verified       BOOLEAN DEFAULT FALSE,
    barcode           VARCHAR(50),
    brand             VARCHAR(255),
    image_url         VARCHAR(500),
    is_custom         BOOLEAN DEFAULT FALSE,
    created_by        INT,
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_foods_name (name),
    INDEX idx_foods_category (category),
    INDEX idx_foods_barcode (barcode),
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE food_images (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    food_id          INT NOT NULL,
    image_url        VARCHAR(500) NOT NULL,
    thumbnail_url    VARCHAR(500),
    confidence_score FLOAT,
    detected_items   JSON,
    ai_provider      VARCHAR(50),
    uploaded_by      INT,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_food_images_food (food_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE nutrition_data (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    food_id              INT NOT NULL,
    healthy_rating       FLOAT,
    processed_level      VARCHAR(20),
    diet_compatibility   JSON,
    weight_loss_score    FLOAT,
    muscle_gain_score    FLOAT,
    recommendation       VARCHAR(20),
    healthy_alternatives JSON,
    best_time_to_eat     VARCHAR(100),
    ai_analysis          TEXT,
    created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nutrition_food (food_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE meals (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    date            DATE NOT NULL,
    meal_type       ENUM('breakfast','lunch','dinner','snack') NOT NULL,
    name            VARCHAR(255),
    total_calories  FLOAT DEFAULT 0.0,
    total_protein   FLOAT DEFAULT 0.0,
    total_carbs     FLOAT DEFAULT 0.0,
    total_fat       FLOAT DEFAULT 0.0,
    total_fiber     FLOAT DEFAULT 0.0,
    notes           TEXT,
    image_url       VARCHAR(500),
    is_ai_generated BOOLEAN DEFAULT FALSE,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_meals_user_date (user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE meal_items (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    meal_id         INT NOT NULL,
    food_id         INT NOT NULL,
    servings        FLOAT NOT NULL DEFAULT 1.0,
    custom_weight_g FLOAT,
    calories        FLOAT NOT NULL,
    protein_g       FLOAT DEFAULT 0.0,
    carbs_g         FLOAT DEFAULT 0.0,
    fat_g           FLOAT DEFAULT 0.0,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_meal_items_meal (meal_id),
    FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id)
) ENGINE=InnoDB;

-- ── Exercises & Workouts ───────────────────────────────────────

CREATE TABLE exercises (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(255) NOT NULL,
    description         TEXT,
    category            VARCHAR(50) NOT NULL,
    difficulty          ENUM('beginner','intermediate','advanced') NOT NULL,
    equipment           VARCHAR(255),
    primary_muscle      VARCHAR(100) NOT NULL,
    secondary_muscles   JSON,
    instructions        JSON,
    tips                JSON,
    common_mistakes     JSON,
    calories_per_minute FLOAT DEFAULT 5.0,
    image_url           VARCHAR(500),
    animation_url       VARCHAR(500),
    default_sets        INT DEFAULT 3,
    default_reps        INT DEFAULT 10,
    default_rest_seconds INT DEFAULT 60,
    is_compound         BOOLEAN DEFAULT FALSE,
    met_value           FLOAT DEFAULT 5.0,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_exercises_name (name),
    INDEX idx_exercises_category (category),
    INDEX idx_exercises_muscle (primary_muscle)
) ENGINE=InnoDB;

CREATE TABLE exercise_videos (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    exercise_id      INT NOT NULL,
    youtube_id       VARCHAR(20) NOT NULL,
    title            VARCHAR(500) NOT NULL,
    thumbnail_url    VARCHAR(500),
    duration_seconds INT,
    is_primary       BOOLEAN DEFAULT FALSE,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_exercise_videos (exercise_id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE exercise_muscles (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    exercise_id INT NOT NULL,
    muscle_name VARCHAR(100) NOT NULL,
    involvement ENUM('primary','secondary','stabilizer') NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_exercise_muscles (exercise_id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE workout_plans (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    plan_type       VARCHAR(50) NOT NULL,
    goal            VARCHAR(50) NOT NULL,
    difficulty      ENUM('beginner','intermediate','advanced') NOT NULL,
    location        ENUM('home','gym','outdoor') DEFAULT 'gym',
    days_per_week   INT DEFAULT 4,
    duration_weeks  INT DEFAULT 8,
    is_ai_generated BOOLEAN DEFAULT FALSE,
    is_active       BOOLEAN DEFAULT TRUE,
    schedule        JSON,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_plans_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE workout_plan_exercises (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    plan_id         INT NOT NULL,
    exercise_id     INT NOT NULL,
    day             VARCHAR(20) NOT NULL,
    order_index     INT DEFAULT 0,
    sets            INT DEFAULT 3,
    reps            VARCHAR(20) DEFAULT '8-12',
    rest_seconds    INT DEFAULT 60,
    weight_kg       FLOAT,
    notes           TEXT,
    superset_group  INT,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_plan_exercises (plan_id),
    FOREIGN KEY (plan_id) REFERENCES workout_plans(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
) ENGINE=InnoDB;

CREATE TABLE workout_sessions (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    user_id              INT NOT NULL,
    plan_id              INT,
    date                 DATE NOT NULL,
    name                 VARCHAR(255),
    workout_type         VARCHAR(50),
    duration_minutes     INT DEFAULT 0,
    total_calories_burned FLOAT DEFAULT 0.0,
    total_volume_kg      FLOAT DEFAULT 0.0,
    avg_heart_rate       INT,
    max_heart_rate       INT,
    notes                TEXT,
    rating               INT,
    is_completed         BOOLEAN DEFAULT FALSE,
    started_at           DATETIME,
    ended_at             DATETIME,
    created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sessions_user_date (user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES workout_plans(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE workout_session_exercises (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    session_id      INT NOT NULL,
    exercise_id     INT NOT NULL,
    order_index     INT DEFAULT 0,
    sets_data       JSON,
    total_sets      INT DEFAULT 0,
    total_reps      INT DEFAULT 0,
    total_weight_kg FLOAT DEFAULT 0.0,
    calories_burned FLOAT DEFAULT 0.0,
    notes           TEXT,
    is_completed    BOOLEAN DEFAULT FALSE,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_session_exercises (session_id),
    FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
) ENGINE=InnoDB;

-- ── Social & Gamification ──────────────────────────────────────

CREATE TABLE achievements (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(255) NOT NULL UNIQUE,
    description      TEXT,
    category         VARCHAR(50) NOT NULL,
    icon             VARCHAR(100),
    badge_color      VARCHAR(20),
    requirement_type VARCHAR(50) NOT NULL,
    requirement_value FLOAT NOT NULL,
    requirement_unit VARCHAR(50),
    xp_reward        INT DEFAULT 100,
    is_active        BOOLEAN DEFAULT TRUE,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE user_achievements (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT NOT NULL,
    achievement_id INT NOT NULL,
    earned_at      DATETIME NOT NULL,
    progress       FLOAT DEFAULT 0.0,
    is_completed   BOOLEAN DEFAULT FALSE,
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_achievements (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE challenges (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(255) NOT NULL,
    description    TEXT,
    challenge_type ENUM('daily','weekly','monthly') NOT NULL,
    category       VARCHAR(50) NOT NULL,
    target_value   FLOAT NOT NULL,
    target_unit    VARCHAR(50) NOT NULL,
    start_date     DATE NOT NULL,
    end_date       DATE NOT NULL,
    xp_reward      INT DEFAULT 50,
    is_active      BOOLEAN DEFAULT TRUE,
    icon           VARCHAR(100),
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE user_challenges (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    challenge_id INT NOT NULL,
    progress     FLOAT DEFAULT 0.0,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at DATETIME,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_challenges (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE notifications (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    user_id           INT NOT NULL,
    title             VARCHAR(255) NOT NULL,
    message           TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    is_read           BOOLEAN DEFAULT FALSE,
    action_url        VARCHAR(500),
    data              JSON,
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_notifications_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Devices & Bluetooth ────────────────────────────────────────

CREATE TABLE devices (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT NOT NULL,
    device_name      VARCHAR(255) NOT NULL,
    device_type      VARCHAR(50) NOT NULL,
    bluetooth_id     VARCHAR(255),
    is_connected     BOOLEAN DEFAULT FALSE,
    last_sync_at     DATETIME,
    battery_level    INT,
    firmware_version VARCHAR(50),
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_devices_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE device_sync_data (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    device_id   INT NOT NULL,
    sync_type   VARCHAR(50) NOT NULL,
    value       FLOAT NOT NULL,
    unit        VARCHAR(20),
    recorded_at DATETIME NOT NULL,
    raw_data    JSON,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sync_device (device_id),
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── AI & Analytics ─────────────────────────────────────────────

CREATE TABLE ai_predictions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    prediction_type VARCHAR(50) NOT NULL,
    prediction_data JSON NOT NULL,
    confidence      FLOAT,
    model_used      VARCHAR(100),
    input_data      JSON,
    valid_until     DATETIME,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_predictions_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE ai_chat_history (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    session_id   VARCHAR(100) NOT NULL,
    role         VARCHAR(20) NOT NULL,
    content      TEXT NOT NULL,
    tokens_used  INT,
    model_used   VARCHAR(100),
    context_data JSON,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_chat_user (user_id),
    INDEX idx_chat_session (session_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Admin & Audit ──────────────────────────────────────────────

CREATE TABLE admin_logs (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    admin_id      INT NOT NULL,
    action        VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id   INT,
    details       JSON,
    ip_address    VARCHAR(45),
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_admin_logs (admin_id),
    FOREIGN KEY (admin_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE audit_logs (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT,
    action      VARCHAR(100) NOT NULL,
    table_name  VARCHAR(100) NOT NULL,
    record_id   INT,
    old_values  JSON,
    new_values  JSON,
    ip_address  VARCHAR(45),
    user_agent  VARCHAR(500),
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_table (table_name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;
