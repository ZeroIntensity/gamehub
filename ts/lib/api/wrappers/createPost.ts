import gql from "../_gql";
import makeRequest from "../makeRequest";

const query = gql`
    mutation createPost($content: String!, $title: String!) {
        createPost(data: { title: $title, content: $content }) {
            id
        }
    }
`;

export default async (
    content: string,
    title: string
): APIResponse<{ createPost: { id: string } }> => {
    return makeRequest(query, { content, title });
};
