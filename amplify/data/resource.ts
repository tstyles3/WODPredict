// import { type ClientSchema, a, defineData } from "@aws-amplify/backend";

// const schema = a.schema({
//   WorkoutData: a
//     .model({
//       id: a.id(), // Unique entry ID
//       userId: a.string(), // User ID
//       date: a.string(), // Date of workout
//       sections: a.string(), //json data needs to be formatted as a string
//       score: a.string(), // Score (e.g., total reps completed)
//     })
//     .authorization((allow) => [allow.owner()]), // Restrict data access to the user
// });

// export type Schema = ClientSchema<typeof schema>;

// export const data = defineData({
//   schema,
//   authorizationModes: {
//     defaultAuthorizationMode: "userPool"
//   },
// });


import { type ClientSchema, a, defineData } from "@aws-amplify/backend"
// import { predictWorkoutScore } from "../functions/predict-workout-score/resource"

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

  // predictWorkoutScore: a
  //   .query()
  //   .arguments({
  //     workout: a.string(), // Store the workout as a JSON string
  //     score: a.string()
  //   })
  //   .returns(a.string()) // Return a JSON string instead of an object
  //   .handler(a.handler.function(predictWorkoutScore)),

  PersonalRecords: a
    .model({
      id: a.id(), // Unique entry ID
      deadlift: a.integer(),
      bench_press: a.integer(),
      back_squat: a.integer(),
      front_squat: a.integer(),
      squat_clean: a.integer(),
      power_clean: a.integer(),
      thruster: a.integer(),
      clean_and_jerk: a.integer(),
      squat_snatch: a.integer(),
      power_snatch: a.integer(),
      overhead_squat: a.integer(),
      strict_press: a.integer(),
      push_press: a.integer(),
      push_jerk: a.integer(),
      split_jerk: a.integer(),
      pull_ups: a.integer(),
      bar_muscle_ups: a.integer(),
      ring_muscle_ups: a.integer(),
      toes_to_bar: a.integer(),
      double_unders: a.integer(),
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

