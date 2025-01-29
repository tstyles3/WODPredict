// import { type ClientSchema, a, defineData } from '@aws-amplify/backend';

// /*== STEP 1 ===============================================================
// The section below creates a Todo database table with a "content" field. Try
// adding a new "isDone" field as a boolean. The authorization rule below
// specifies that any unauthenticated user can "create", "read", "update", 
// and "delete" any "Todo" records.
// =========================================================================*/
// const schema = a.schema({
//   Todo: a
//     .model({
//       content: a.string(),
//     })
//     .authorization((allow) => [allow.guest()]),
// });

// export type Schema = ClientSchema<typeof schema>;

// export const data = defineData({
//   schema,
//   authorizationModes: {
//     defaultAuthorizationMode: 'iam',
//   },
// });

// /*== STEP 2 ===============================================================
// Go to your frontend source code. From your client-side code, generate a
// Data client to make CRUDL requests to your table. (THIS SNIPPET WILL ONLY
// WORK IN THE FRONTEND CODE FILE.)

// Using JavaScript or Next.js React Server Components, Middleware, Server 
// Actions or Pages Router? Review how to generate Data clients for those use
// cases: https://docs.amplify.aws/gen2/build-a-backend/data/connect-to-API/
// =========================================================================*/

// /*
// "use client"
// import { generateClient } from "aws-amplify/data";
// import type { Schema } from "@/amplify/data/resource";

// const client = generateClient<Schema>() // use this Data client for CRUDL requests
// */

// /*== STEP 3 ===============================================================
// Fetch records from the database and use them in your frontend component.
// (THIS SNIPPET WILL ONLY WORK IN THE FRONTEND CODE FILE.)
// =========================================================================*/

// /* For example, in a React component, you can use this snippet in your
//   function's RETURN statement */
// // const { data: todos } = await client.models.Todo.list()

// // return <ul>{todos.map(todo => <li key={todo.id}>{todo.content}</li>)}</ul>

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
    defaultAuthorizationMode: "iam",
  },
});
