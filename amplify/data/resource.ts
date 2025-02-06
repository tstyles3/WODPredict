import { type ClientSchema, a, defineData } from "@aws-amplify/backend";

const schema = a.schema({
  WorkoutData: a
    .model({
      id: a.id(), // Unique entry ID
      userId: a.string(), // User ID
      date: a.string(), // Date of workout
      sections: a.string(), //json data needs to be formatted as a string
      score: a.string(), // Score (e.g., total reps completed)
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
