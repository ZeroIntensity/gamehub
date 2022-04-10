import makeRequest from "../makeRequest";
import { UserInputSchema } from "../schema";
import gql from "../_gql";

const query = gql`
    mutation CreateAccount($username: String!, $password: String!) {
        createAccount(credentials: { name: $username, password: $password })
    }
`;

export default async (
    credentials: UserInputSchema
): APIResponse<{ createAccount: string }> => {
    return makeRequest(query, {
        username: credentials.name,
        password: credentials.password,
    });
};
