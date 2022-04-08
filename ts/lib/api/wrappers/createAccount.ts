import makeRequest from "../makeRequest";
import gql from "../_gql";

const query = gql`
    mutation CreateAccount($username: String!, $password: String!) {
        createAccount(credentials: { name: $username, password: $password })
    }
`;

export default async (
    credentials: UserInput
): APIResponse<{ createAccount: string }> => {
    return makeRequest(query, {
        username: credentials.name,
        password: credentials.password,
    });
};
