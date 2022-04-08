import gql from "../_gql";
import makeRequest from "../makeRequest";

const query = gql`
    mutation login($username: String!, $password: String!) {
        login(credentials: { name: $username, password: $password })
    }
`;

export default async (
    username: string,
    password: string
): APIResponse<{ login: string }> => {
    return makeRequest(query, {
        username,
        password,
    });
};

export async function logout(): APIResponse<{ logout: string }> {
    return makeRequest(gql`
        mutation logout {
            logout
        }
    `);
}
