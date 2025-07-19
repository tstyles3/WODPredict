import { type ClientSchema, a, defineData } from "@aws-amplify/backend"

const schema = a.schema({
  WorkoutData: a
    .model({
      id: a.id(), // Unique entry ID
      userId: a.string(), // User ID
      date: a.string(), // Date of workout
      sections: a.string(), //json data needs to be formatted as a string
      score: a.string(), // Score (e.g., total reps completed)
      prediction: a.string(),
      time: a.boolean(), // indicator between time or reps
      multiplier: a.string(), // multiplier to adjust scores based on trained data
    })
    .authorization((allow) => [allow.owner()]), // Restrict data access to the user

  Movement: a
    .model({
      id: a.id(),
      label: a.string(),
      value: a.string(),
      fields: (a.string()),
    })
    .authorization((allow) => [
      allow.authenticated().to(["read"]), // Public can ONLY read
      // allow.owner().to(['create', 'read', 'delete', 'update'])
    ]),

  PersonalRecords: a
    .model({
      id: a.id(), // Unique entry ID
      deadlift: a.integer(),
      deadlift_timestamp: a.string(), // Timestamp for deadlift
      bench_press: a.integer(),
      bench_press_timestamp: a.string(), // Timestamp for bench press
      back_squat: a.integer(),
      back_squat_timestamp: a.string(), // Timestamp for back squat
      front_squat: a.integer(),
      front_squat_timestamp: a.string(), // Timestamp for front squat
      squat_clean: a.integer(),
      squat_clean_timestamp: a.string(), // Timestamp for squat clean
      power_clean: a.integer(),
      power_clean_timestamp: a.string(), // Timestamp for power clean
      thruster: a.integer(),
      thruster_timestamp: a.string(), // Timestamp for thruster
      clean_and_jerk: a.integer(),
      clean_and_jerk_timestamp: a.string(), // Timestamp for clean and jerk
      squat_snatch: a.integer(),
      squat_snatch_timestamp: a.string(), // Timestamp for squat snatch
      power_snatch: a.integer(),
      power_snatch_timestamp: a.string(), // Timestamp for power snatch
      overhead_squat: a.integer(),
      overhead_squat_timestamp: a.string(), // Timestamp for overhead squat
      strict_press: a.integer(),
      strict_press_timestamp: a.string(), // Timestamp for strict press
      push_press: a.integer(),
      push_press_timestamp: a.string(), // Timestamp for push press
      push_jerk: a.integer(),
      push_jerk_timestamp: a.string(), // Timestamp for push jerk
      split_jerk: a.integer(),
      split_jerk_timestamp: a.string(), // Timestamp for split jerk
      pull_ups: a.integer(),
      pull_ups_timestamp: a.string(), // Timestamp for pull ups
      bar_muscle_ups: a.integer(),
      bar_muscle_ups_timestamp: a.string(), // Timestamp for bar muscle ups
      ring_muscle_ups: a.integer(),
      ring_muscle_ups_timestamp: a.string(), // Timestamp for ring muscle ups
      toes_to_bar: a.integer(),
      toes_to_bar_timestamp: a.string(), // Timestamp for toes to bar
      double_unders: a.integer(),
      double_unders_timestamp: a.string(), // Timestamp for double unders
    })
    .authorization((allow) => [allow.owner()]), // Restrict data access to the user
})

export type Schema = ClientSchema<typeof schema>

export const data = defineData({
  schema,
  authorizationModes: {
    defaultAuthorizationMode: "userPool",
    apiKeyAuthorizationMode: { expiresInDays: 30 }, // Ensure API key exists for public read
  },
})

