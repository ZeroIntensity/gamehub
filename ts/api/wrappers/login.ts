import gql from "../_gql";
import makeRequest from "../makeRequest";

const query = gql`
    mutation login($username: String!, $password: String!) {
        login(credentials: { name: $username, password: $password })
    }
`;

export default async (username: string, password: string): Promise<string> => {
    return makeRequest(query, {
        username,
        password,
    });
};
