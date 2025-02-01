import { type ClientSchema, a, defineData } from "@aws-amplify/backend";

const schema = a.schema({
  WorkoutData: a
    .model({
      id: a.id(), // Unique entry ID
      userId: a.string(), // User ID
      date: a.date(), // Date of workout
      workoutType: a.string(), // AMRAP, Rounds, etc.
      movements: a.string().array(), // List of movements
      reps: a.integer().array(), // Reps per movement
      weights: a.float().array(), // Weights per movement
      score: a.float(), // Score (e.g., total reps completed)
    })
    .authorization((allow) => [allow.owner()]), // Restrict data access to the user
});

export type Schema = ClientSchema<typeof schema>;

export const data = defineData({
  schema,
  authorizationModes: {
    defaultAuthorizationMode: "userPool"
  },
});
