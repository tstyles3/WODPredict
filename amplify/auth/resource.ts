import { defineAuth } from "@aws-amplify/backend";

export const auth = defineAuth({
  loginWith: {
    email: true,
  },
  userAttributes: {
    givenName: { required: true, mutable: true }, // First name
    familyName: { required: true, mutable: true }, // Last name
    email: { required: true, mutable: true }, // Email
  },
});
