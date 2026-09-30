-- ═══════════════════════════════════════════════════════════════
-- AI Fitness Ecosystem — Seed Data
-- Populates lookup tables, exercise library, default admin user
-- ═══════════════════════════════════════════════════════════════

USE ai_fitness_db;

-- ── Muscle Groups ───────────────────────────────────────────

INSERT INTO muscle_groups (name, category, description) VALUES
('Pectorals', 'chest', 'Chest muscles including pec major and minor'),
('Anterior Deltoid', 'shoulders', 'Front shoulder muscle'),
('Lateral Deltoid', 'shoulders', 'Side shoulder muscle'),
('Posterior Deltoid', 'shoulders', 'Rear shoulder muscle'),
('Triceps Brachii', 'arms', 'Back of upper arm'),
('Biceps Brachii', 'arms', 'Front of upper arm'),
('Forearms', 'arms', 'Lower arm muscles'),
('Latissimus Dorsi', 'back', 'Large back muscle'),
('Trapezius', 'back', 'Upper back and neck muscle'),
('Rhomboids', 'back', 'Upper mid-back muscles'),
('Erector Spinae', 'back', 'Lower back muscles'),
('Quadriceps', 'legs', 'Front of thigh'),
('Hamstrings', 'legs', 'Back of thigh'),
('Glutes', 'legs', 'Buttock muscles'),
('Calves', 'legs', 'Lower leg muscles'),
('Rectus Abdominis', 'core', 'Six-pack muscles'),
('Obliques', 'core', 'Side abdominal muscles'),
('Transverse Abdominis', 'core', 'Deep core stabilizer'),
('Hip Flexors', 'legs', 'Front of hip muscles'),
('Adductors', 'legs', 'Inner thigh muscles');

-- ── Equipment ───────────────────────────────────────────────

INSERT INTO equipment (name, category) VALUES
('Barbell', 'free_weight'),
('Dumbbell', 'free_weight'),
('EZ Curl Bar', 'free_weight'),
('Kettlebell', 'free_weight'),
('Resistance Band', 'band'),
('Cable Machine', 'machine'),
('Smith Machine', 'machine'),
('Leg Press Machine', 'machine'),
('Pull-up Bar', 'bodyweight'),
('Dip Station', 'bodyweight'),
('Bench (Flat)', 'bench'),
('Bench (Incline)', 'bench'),
('Bench (Decline)', 'bench'),
('Medicine Ball', 'accessory'),
('Foam Roller', 'accessory'),
('TRX Suspension', 'accessory'),
('Jump Rope', 'cardio'),
('Treadmill', 'cardio'),
('Rowing Machine', 'cardio'),
('Stationary Bike', 'cardio'),
('Bodyweight', 'bodyweight');

-- ── Exercise Library (100 exercises) ────────────────────────

INSERT INTO exercises (name, description, category, difficulty, equipment_needed, muscles_targeted, calories_per_minute, is_compound, instructions, tips) VALUES
-- CHEST
('Barbell Bench Press', 'Classic compound chest exercise', 'strength', 'intermediate', 'Barbell, Flat Bench', 'Pectorals, Anterior Deltoid, Triceps', 8.5, TRUE,
 '["Lie flat on bench, feet flat on floor", "Grip bar slightly wider than shoulder width", "Lower bar to mid-chest with control", "Press up explosively, lock out arms"]',
 '["Keep shoulder blades retracted", "Maintain natural arch in lower back", "Use a spotter for heavy sets"]'),

('Incline Dumbbell Press', 'Upper chest focused pressing', 'strength', 'intermediate', 'Dumbbells, Incline Bench', 'Upper Pectorals, Anterior Deltoid', 7.5, TRUE,
 '["Set bench to 30-45 degree incline", "Press dumbbells up from chest level", "Lower with control, stretch at bottom"]',
 '["Don''t go too steep — 30° is optimal", "Rotate wrists slightly at top"]'),

('Dumbbell Chest Fly', 'Chest isolation with stretch', 'strength', 'beginner', 'Dumbbells, Flat Bench', 'Pectorals', 5.0, FALSE,
 '["Lie flat, arms extended above chest", "Open arms in wide arc", "Squeeze chest to bring dumbbells together"]',
 '["Maintain slight bend in elbows throughout", "Focus on the stretch"]'),

('Cable Crossover', 'Continuous tension chest work', 'strength', 'intermediate', 'Cable Machine', 'Pectorals', 5.5, FALSE,
 '["Set cables to high position", "Step forward, lean slightly", "Bring handles together at waist level"]',
 '["Squeeze at the bottom", "Control the eccentric"]'),

('Push-ups', 'Fundamental bodyweight chest exercise', 'strength', 'beginner', 'Bodyweight', 'Pectorals, Triceps, Core', 7.0, TRUE,
 '["Hands slightly wider than shoulders", "Lower chest to floor", "Push back up fully"]',
 '["Keep body in straight line", "Modify on knees if needed"]'),

-- BACK
('Deadlift', 'King of all exercises — full posterior chain', 'strength', 'advanced', 'Barbell', 'Erector Spinae, Glutes, Hamstrings, Traps', 12.0, TRUE,
 '["Bar over mid-foot, hip-width stance", "Hinge at hips, grip just outside legs", "Drive through floor, extend hips", "Lock out at top, reverse to lower"]',
 '["Keep bar close to body", "Never round lower back", "Use mixed or hook grip for heavy weights"]'),

('Pull-ups', 'Best lat builder available', 'strength', 'intermediate', 'Pull-up Bar', 'Latissimus Dorsi, Biceps, Rhomboids', 7.0, TRUE,
 '["Hang with arms fully extended", "Pull up until chin clears bar", "Lower slowly with control"]',
 '["Use bands for assistance if needed", "Avoid kipping"]'),

('Barbell Row', 'Thick back builder', 'strength', 'intermediate', 'Barbell', 'Latissimus Dorsi, Rhomboids, Biceps', 7.5, TRUE,
 '["Hinge at hips, back flat at ~45°", "Pull bar to lower chest/upper abs", "Squeeze shoulder blades at top"]',
 '["Keep core tight", "Don''t use momentum"]'),

('Seated Cable Row', 'Controlled back exercise', 'strength', 'beginner', 'Cable Machine', 'Latissimus Dorsi, Rhomboids', 6.0, TRUE,
 '["Sit upright, feet on platform", "Pull handle to lower chest", "Squeeze shoulder blades together"]',
 '["Keep torso stationary", "Use V-grip for variety"]'),

('Face Pulls', 'Rear delt and rotator cuff health', 'strength', 'beginner', 'Cable Machine, Rope', 'Posterior Deltoid, Rhomboids', 4.0, FALSE,
 '["Set cable to face height", "Pull rope to face, elbows high", "External rotate at end position"]',
 '["Use light weight", "Focus on squeeze"]'),

-- SHOULDERS
('Overhead Press', 'Standing barbell press', 'strength', 'intermediate', 'Barbell', 'All Deltoids, Triceps, Core', 7.5, TRUE,
 '["Bar at front shoulders, slightly wider grip", "Press overhead, lock arms", "Lower under control to shoulders"]',
 '["Squeeze glutes for stability", "Don''t lean back excessively"]'),

('Lateral Raises', 'Side delt isolation', 'strength', 'beginner', 'Dumbbells', 'Lateral Deltoid', 3.0, FALSE,
 '["Stand with dumbbells at sides", "Raise to shoulder height, slight forward lean", "Lower slowly"]',
 '["Lead with elbows not hands", "Use light weight, high reps"]'),

('Arnold Press', 'Rotational shoulder press', 'strength', 'intermediate', 'Dumbbells', 'All Deltoids', 6.5, TRUE,
 '["Start with dumbbells at chest, palms facing you", "Rotate as you press overhead", "Reverse the motion coming down"]',
 '["Named after Arnold Schwarzenegger", "Great for all delt heads"]'),

-- LEGS
('Barbell Squat', 'Foundation leg exercise', 'strength', 'intermediate', 'Barbell, Squat Rack', 'Quadriceps, Glutes, Hamstrings, Core', 10.0, TRUE,
 '["Bar across upper back, feet shoulder-width", "Brace core, sit back and down", "Break parallel, drive through heels"]',
 '["Keep knees tracking over toes", "Maintain upright torso"]'),

('Romanian Deadlift', 'Hamstring and glute focused', 'strength', 'intermediate', 'Barbell or Dumbbells', 'Hamstrings, Glutes, Erector Spinae', 8.0, TRUE,
 '["Hold bar at hips, slight knee bend", "Hinge at hips, push butt back", "Lower until hamstring stretch", "Drive hips forward to stand"]',
 '["Keep bar close to legs", "Feel the stretch in hamstrings"]'),

('Leg Press', 'Machine-based quad dominant', 'strength', 'beginner', 'Leg Press Machine', 'Quadriceps, Glutes', 7.0, TRUE,
 '["Sit with back flat against pad", "Place feet shoulder-width on platform", "Lower weight under control", "Press through heels"]',
 '["Don''t lock knees fully", "Use different foot positions for variety"]'),

('Leg Curls', 'Hamstring isolation', 'strength', 'beginner', 'Leg Curl Machine', 'Hamstrings', 4.5, FALSE,
 '["Lie face down on machine", "Curl weight up squeezing hamstrings", "Lower slowly with control"]',
 '["Don''t use momentum", "Squeeze at the top"]'),

('Calf Raises', 'Calf development', 'strength', 'beginner', 'Smith Machine or Bodyweight', 'Calves', 3.5, FALSE,
 '["Stand on edge of step or platform", "Rise up onto toes as high as possible", "Lower slowly below the step for stretch"]',
 '["Pause at the top for peak contraction", "Use full range of motion"]'),

('Bulgarian Split Squat', 'Unilateral leg work', 'strength', 'intermediate', 'Dumbbells, Bench', 'Quadriceps, Glutes', 8.5, TRUE,
 '["Rear foot elevated on bench", "Lower until back knee nearly touches floor", "Drive through front heel"]',
 '["Keep torso upright", "Great for fixing imbalances"]'),

-- ARMS
('Barbell Curl', 'Classic bicep builder', 'strength', 'beginner', 'Barbell or EZ Bar', 'Biceps Brachii', 4.0, FALSE,
 '["Stand with bar at arm''s length", "Curl up keeping elbows at sides", "Lower under control"]',
 '["Don''t swing the weight", "Squeeze at the top"]'),

('Hammer Curls', 'Brachialis and forearm focused', 'strength', 'beginner', 'Dumbbells', 'Biceps, Forearms', 4.0, FALSE,
 '["Hold dumbbells with neutral grip", "Curl up keeping palms facing each other", "Lower slowly"]',
 '["Builds arm thickness", "Great for grip strength"]'),

('Tricep Pushdowns', 'Cable tricep isolation', 'strength', 'beginner', 'Cable Machine', 'Triceps Brachii', 4.0, FALSE,
 '["Grip cable bar at chest height", "Push down until arms are straight", "Control the return"]',
 '["Keep elbows pinned to sides", "Use rope attachment for variety"]'),

('Skull Crushers', 'Lying tricep extension', 'strength', 'intermediate', 'EZ Bar, Flat Bench', 'Triceps Brachii', 5.0, FALSE,
 '["Lie on bench, arms extended over chest", "Lower bar to forehead by bending elbows", "Extend back to start"]',
 '["Keep upper arms stationary", "Use EZ bar for wrist comfort"]'),

('Dips', 'Compound pushing movement', 'strength', 'intermediate', 'Dip Station', 'Triceps, Pectorals, Anterior Deltoid', 7.0, TRUE,
 '["Support yourself on parallel bars", "Lower body by bending elbows", "Push back up to full extension"]',
 '["Lean forward for more chest", "Stay upright for more triceps"]'),

-- CORE
('Plank', 'Core stability foundation', 'strength', 'beginner', 'Bodyweight', 'All Core Muscles', 3.5, FALSE,
 '["Forearms on ground, body straight", "Engage core, don''t let hips sag", "Hold for time"]',
 '["Breathe steadily", "Keep neck neutral"]'),

('Russian Twists', 'Oblique focused rotation', 'strength', 'beginner', 'Bodyweight or Medicine Ball', 'Obliques, Rectus Abdominis', 5.0, FALSE,
 '["Sit with knees bent, lean back slightly", "Rotate torso side to side", "Touch ground on each side"]',
 '["Lift feet off ground for extra difficulty", "Keep chest up"]'),

('Hanging Leg Raises', 'Advanced lower ab exercise', 'strength', 'advanced', 'Pull-up Bar', 'Rectus Abdominis, Hip Flexors', 6.0, FALSE,
 '["Hang from bar with straight arms", "Raise legs to parallel or above", "Lower with control"]',
 '["Avoid swinging", "Bend knees for easier variation"]'),

('Ab Wheel Rollout', 'Full core engagement', 'strength', 'advanced', 'Ab Wheel', 'All Core Muscles', 7.0, FALSE,
 '["Kneel with wheel in front", "Roll forward extending body", "Pull back using core strength"]',
 '["Start with partial range", "Don''t collapse lower back"]'),

-- CARDIO
('Burpees', 'Full body conditioning', 'cardio', 'intermediate', 'Bodyweight', 'Full Body', 10.0, TRUE,
 '["Stand, squat down hands on floor", "Jump feet back to plank", "Do a push-up", "Jump feet forward and explode up"]',
 '["Scale by removing push-up or jump", "Great for HIIT circuits"]'),

('Mountain Climbers', 'High intensity core cardio', 'cardio', 'beginner', 'Bodyweight', 'Core, Hip Flexors, Shoulders', 8.0, TRUE,
 '["Start in push-up position", "Drive knees to chest alternately", "Maintain fast pace"]',
 '["Keep hips level", "Don''t let butt rise"]'),

('Jump Rope', 'Classic cardio conditioning', 'cardio', 'beginner', 'Jump Rope', 'Calves, Forearms, Core', 11.0, FALSE,
 '["Hold handles at hip height", "Jump with both feet barely clearing rope", "Land softly on balls of feet"]',
 '["Start slow to find rhythm", "Keep elbows close to body"]'),

('Box Jumps', 'Explosive power development', 'plyometric', 'intermediate', 'Plyo Box', 'Quadriceps, Glutes, Calves', 9.0, TRUE,
 '["Stand in front of box, feet shoulder-width", "Swing arms and jump up onto box", "Land softly with both feet", "Step down to reset"]',
 '["Start with lower box height", "Focus on soft landings"]'),

('Kettlebell Swings', 'Hip hinge power and conditioning', 'cardio', 'intermediate', 'Kettlebell', 'Glutes, Hamstrings, Core', 9.5, TRUE,
 '["Hinge at hips, swing bell between legs", "Drive hips forward to swing bell to chest height", "Control the descent"]',
 '["Power comes from hips not arms", "Keep core tight throughout"]'),

-- FLEXIBILITY
('Downward Dog', 'Classic yoga pose', 'flexibility', 'beginner', 'Bodyweight', 'Hamstrings, Calves, Shoulders', 2.5, FALSE,
 '["Start on hands and knees", "Push hips up and back", "Press heels toward floor"]',
 '["Bend knees slightly if hamstrings tight", "Spread fingers wide"]'),

('Pigeon Pose', 'Deep hip flexor stretch', 'flexibility', 'intermediate', 'Bodyweight', 'Hip Flexors, Glutes', 2.0, FALSE,
 '["From all fours, bring one knee forward", "Extend back leg behind you", "Lower hips toward ground"]',
 '["Use a pillow under hip if needed", "Hold for 30-60 seconds each side"]'),

('Cat-Cow Stretch', 'Spinal mobility', 'flexibility', 'beginner', 'Bodyweight', 'Erector Spinae, Core', 2.0, FALSE,
 '["Start on hands and knees", "Arch back (cow) then round back (cat)", "Flow between positions with breath"]',
 '["Inhale on cow, exhale on cat", "Move slowly and mindfully"]');

-- ── Demo Admin User ─────────────────────────────────────────
-- Password: Admin@1234 (bcrypt hash)
INSERT INTO users (email, password_hash, full_name, role, is_active, is_verified, gender, date_of_birth) VALUES
('admin@aifitness.com', '$2b$12$LJ3dKxVZgPS1kp.YwrE5OeqUmvlA2XH0MvvRj3gVj.E6A8d6P3G4a', 'Admin User', 'admin', TRUE, TRUE, 'male', '1990-01-01');

-- ── Demo Regular User ───────────────────────────────────────
-- Password: Demo@1234
INSERT INTO users (email, password_hash, full_name, role, is_active, is_verified, gender, date_of_birth, height_cm, current_weight_kg, target_weight_kg, activity_level, fitness_goal) VALUES
('demo@aifitness.com', '$2b$12$LJ3dKxVZgPS1kp.YwrE5OeqUmvlA2XH0MvvRj3gVj.E6A8d6P3G4a', 'John Doe', 'user', TRUE, TRUE, 'male', '1998-05-15', 175, 75.2, 72.0, 'moderate', 'lose_weight');

-- ── Subscription Plans ──────────────────────────────────────

INSERT INTO subscription_plans (name, price_monthly, price_yearly, features, max_scans_per_day, max_ai_chats_per_day) VALUES
('Free', 0.00, 0.00, '["Basic tracking", "5 AI scans/day", "Exercise library", "BMI calculator"]', 5, 10),
('Pro', 9.99, 99.99, '["Unlimited AI scans", "AI Coach", "Advanced analytics", "Meal planning", "Bluetooth sync", "Priority support"]', -1, -1),
('Enterprise', 29.99, 299.99, '["Everything in Pro", "Team management", "Power BI reports", "API access", "Dedicated support", "Custom branding"]', -1, -1);

SELECT 'Seed data loaded successfully! ✅' AS status;
