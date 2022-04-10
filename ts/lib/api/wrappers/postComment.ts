import gql from "../_gql";
import makeRequest from "../makeRequest";

const query = gql`
    mutation postComment($gameName: String!, $content: String!) {
        createComment(name: $gameName, content: $content) {
            author
            content
            epoch
            id
        }
    }
`;

export default async (
    gameName: string,
    content: string
): APIResponse<{
    createComment: {
        author: string;
        content: string;
        epoch: number;
        id: string;
    };
}> => {
    return makeRequest(query, { gameName, content });
};
